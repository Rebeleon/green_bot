#!/usr/bin/env python3.7

import asyncio
import websockets
import datetime
import logging

from aiohttp import web

WEBSOCKET_HOST = 'localhost'
WEBSOCKET_PORT = 9000
HTTP_HOST = 'localhost'
HTTP_PORT = 8080
AUTH_TOKEN = 'Rg4P1gQeMy'

logging.basicConfig(level=logging.INFO)
queue_open_door = asyncio.Queue(maxsize=1)


async def serve_client(websocket, path):
    logging.info('Websocket client connected')

    # authentication
    try:
        auth_token = await asyncio.wait_for(websocket.recv(), timeout=20)
        if auth_token != AUTH_TOKEN:
            logging.info(f'Invalid auth token')
            return
        else:
            logging.info('Successfully authorized')
            await asyncio.wait_for(websocket.send('authorized'), timeout=0.5)
    except asyncio.TimeoutError:
        return

    while True:
        try:
            action = await asyncio.wait_for(websocket.recv(), timeout=0.5)
            if action == 'opened':
                logging.info('Received opened')
        except asyncio.TimeoutError:
            pass
        except websockets.exceptions.ConnectionClosed:
            logging.info('Websocket client disconnected')
            return

        try:
            data = await asyncio.wait_for(queue_open_door.get(), timeout=0.5)
            if data and data['action'] == 'door' and data['expired'] > datetime.datetime.utcnow():
                # ODOR! - https://knowyourmeme.com/memes/hold-the-door
                logging.info('Sent open door command to device')
                await asyncio.wait_for(websocket.send('ODOR!'), timeout=0.5)
        except asyncio.TimeoutError:
            pass

logging.info(f'Started websockets server at ws://{WEBSOCKET_HOST}:{WEBSOCKET_PORT}')

asyncio.get_event_loop().run_until_complete(websockets.serve(serve_client, WEBSOCKET_HOST, WEBSOCKET_PORT))


async def handle(request):
    if request.headers.get('Authorization') == AUTH_TOKEN:
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
        logging.info('Open door request error: No auth token')

        return web.json_response({'status': 'error'})

app = web.Application()
app.add_routes([
    web.post('/', handle),
])

logging.info(f'Started HTTP server at http://{HTTP_HOST}:{HTTP_PORT}')

web.run_app(app, port=HTTP_PORT)
