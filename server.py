#!/usr/bin/env python3.7

import asyncio
import websockets
import datetime
import logging

from aiohttp import web

WEBSOCKET_HOST = '144.76.100.208'
WEBSOCKET_PORT = 9000
HTTP_HOST = 'localhost'
HTTP_PORT = 8080
AUTH_TOKEN = 'Rg4P1gQeMy'
COMMANDS = ['open', 'enable', 'disable']

logging.basicConfig(level=logging.INFO)
cmd_queue = asyncio.Queue(maxsize=1)


async def serve_client(websocket, path):
    logging.info('Device is connected')

    try:
        auth_token = await asyncio.wait_for(websocket.recv(), timeout=20)
        if auth_token != AUTH_TOKEN:
            logging.info('Device uses invalid auth token')
            return
        else:
            logging.info('Device is successfully authorized')
            await asyncio.wait_for(websocket.send('authorized'), timeout=5)
    except asyncio.TimeoutError:
        return

    while True:
        try:
            response = await asyncio.wait_for(websocket.recv(), timeout=0.5)
            logging.info(f'Received "{response}" from device')
        except asyncio.TimeoutError:
            pass
        except websockets.exceptions.ConnectionClosed:
            logging.info('Device disconnected')
            return

        try:
            data = await asyncio.wait_for(cmd_queue.get(), timeout=0.5)
            if data and data['expired'] > datetime.datetime.utcnow():
                cmd = data['command']
                logging.info(f'Sent "{cmd}" command to device')
                await asyncio.wait_for(websocket.send(cmd), timeout=5)
        except asyncio.TimeoutError:
            pass

logging.info(f'Started websockets server at ws://{WEBSOCKET_HOST}:{WEBSOCKET_PORT}')

asyncio.get_event_loop().run_until_complete(websockets.serve(serve_client, WEBSOCKET_HOST, WEBSOCKET_PORT))


async def handle(request):
    if request.headers.get('Authorization') == AUTH_TOKEN:
        body = await request.json()

        if not body or not 'command' in body or not body['command'] in COMMANDS:
            logging.info('Received request with wrong or missing command')
            return web.json_response({'status': 'error', 'message': 'Wrong or missing command'}, status=400)

        cmd = body['command']

        logging.info(f'Received request with "{cmd}" command')

        if not cmd_queue.empty():
            await asyncio.wait_for(cmd_queue.get(), timeout=5)

        data = {
            'command': cmd,
            'expired': datetime.datetime.utcnow() + datetime.timedelta(seconds=10),
        }

        await asyncio.wait_for(cmd_queue.put(data), timeout=5)
        return web.json_response({'status': 'ok', 'message': 'command sent'})
    else:
        logging.info('Wrong or missing authorization token')
        return web.json_response({'status': 'error', 'message': 'Wrong or missing authorization token'}, status=401)

app = web.Application()
app.add_routes([
    web.post('/', handle),
])

logging.info(f'Started HTTP server at http://{HTTP_HOST}:{HTTP_PORT}')

web.run_app(app, port=HTTP_PORT)
