#!/usr/bin/env python

import asyncio
import websockets
import datetime
import logging

from aiohttp import web


queue_open_door = asyncio.Queue(maxsize=1)


async def serve_client(websocket, path):
    logging.warning(f'Connected {websocket}')

    latest_ping = None
    latest_pong = None
    while True:
        if not latest_ping or latest_ping < datetime.datetime.utcnow() - datetime.timedelta(seconds=20):
            latest_ping = datetime.datetime.utcnow()
            await websocket.send('ping')
        
        try:
            action = await asyncio.wait_for(websocket.recv(), timeout=0.5)
            if action == 'pong':
                latest_pong = datetime.datetime.utcnow()
                logging.warning('Received pong')
            elif action == 'opened':
                logging.warning('Received opened')
        except asyncio.TimeoutError:
            pass

        try:
            data = await asyncio.wait_for(queue_open_door.get(), timeout=0.5)
            if data and data['action'] == 'door' and data['expired'] > datetime.datetime.utcnow():
                await websocket.send('door')
        except asyncio.TimeoutError:
            pass
            

start_server = websockets.serve(serve_client, '195.201.172.78', 9000)
asyncio.get_event_loop().run_until_complete(start_server)


async def handle(request):
    if request.headers.get('Authorization') == '8VfY8XdnBmEoES2UuH4Zvnhh6oKqMbN48FHYpZpn':
        logging.warning('Request to open door')

        if not queue_open_door.empty():
            await queue_open_door.get()
    
        data = {
            'action': 'door',
            'expired': datetime.datetime.utcnow() + datetime.timedelta(seconds=10),
        }
        await queue_open_door.put(data)
        return web.json_response({'status': 'ok'})
    else:
        logging.warning('Error request to open door. No token')

        return web.json_response({'status': 'error'})


app = web.Application()
app.add_routes([
    web.get('/', handle),
])
web.run_app(app, port=8080)
