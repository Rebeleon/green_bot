#!/usr/bin/env python

import asyncio
import websockets
import datetime
import logging

from aiohttp import web


import coloredlogs
coloredlogs.install(level='INFO')


queue_open_door = asyncio.Queue(maxsize=1)

TOKEN = 'Rg4P1gQeMy'


async def serve_client(websocket, path):
    logging.info(f'Connected {websocket}')

    # authentication
    try:
        auth = await asyncio.wait_for(websocket.recv(), timeout=20)
        if auth != TOKEN:
            logging.info(f'Bad auth {auth}')
            return
    except asyncio.TimeoutError:
        return

    latest_ping = None
    latest_pong = None
    while True:
        if not latest_ping or latest_ping < datetime.datetime.utcnow() - datetime.timedelta(seconds=20):
            latest_ping = datetime.datetime.utcnow()
            logging.info('Send ping')
            await websocket.send('ping')
        
        try:
            action = await asyncio.wait_for(websocket.recv(), timeout=0.5)
            if action == 'pong':
                latest_pong = datetime.datetime.utcnow()
                logging.info('Received pong')
            elif action == 'opened':
                logging.info('Received opened')
        except asyncio.TimeoutError:
            pass

        # do not try to open door, if connection is idle
        threshold = datetime.datetime.utcnow() - datetime.timedelta(minutes=2)
        if latest_pong and latest_ping and latest_pong > threshold:
            try:
                data = await asyncio.wait_for(queue_open_door.get(), timeout=0.5)
                if data and data['action'] == 'door' and data['expired'] > datetime.datetime.utcnow():
                    logging.info('Send open door to device')
                    await websocket.send('door')
            except asyncio.TimeoutError:
                pass
            

start_server = websockets.serve(serve_client, '195.201.172.78', 9000)
asyncio.get_event_loop().run_until_complete(start_server)


async def handle(request):
    if request.headers.get('Authorization') == TOKEN:
        logging.info('Request to open door')

        if not queue_open_door.empty():
            await queue_open_door.get()
    
        data = {
            'action': 'door',
            'expired': datetime.datetime.utcnow() + datetime.timedelta(seconds=10),
        }
        await queue_open_door.put(data)
        return web.json_response({'status': 'ok'})
    else:
        logging.info('Error request to open door. No token')

        return web.json_response({'status': 'error'})


app = web.Application()
app.add_routes([
    web.post('/', handle),
])
web.run_app(app, port=8080)
