#!/usr/bin/env python

# WS server example

import asyncio
import websockets
import datetime

from aiohttp import web


queue_open_door = asyncio.Queue(maxsize=1)


async def serve_client(websocket, path):
    latest_ping = None
    latest_pong = None
    while True:
        if not latest_ping or latest_ping < datetime.datetime.utcnow() - datetime.timedelta(minutes=1):
            latest_ping = datetime.datetime.utcnow()
            await websocket.send('ping')
        
        try:
            action = await asyncio.wait_for(websocket.recv(), timeout=0.5)
            if action == 'pong':
                latest_pong = datetime.datetime.utcnow()
                print('Received pong')
        except asyncio.TimeoutError:
            pass

        try:
            data = await asyncio.wait_for(queue_open_door.get(), timeout=0.5)
            if data and data['action'] == 'door' and data['expired'] > datetime.datetime.utcnow():
                await websocket.send('door')
        except asyncio.TimeoutError:
            pass
            

start_server = websockets.serve(serve_client, 'localhost', 9000)
asyncio.get_event_loop().run_until_complete(start_server)


async def handle(request):
    if not queue_open_door.empty():
        await queue_open_door.get()

    data = {
        'action': 'door',
        'expired': datetime.datetime.utcnow() + datetime.timedelta(seconds=10),
    }
    await queue_open_door.put(data)
    return web.json_response({'status': 'ok'})


app = web.Application()
app.add_routes([
    web.get('/', handle),
])
web.run_app(app, port=8080)
