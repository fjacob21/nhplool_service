#!/usr/bin/env python3

from aiohttp import web
import asyncio
import time
from stores import get_debug
from data.pooldata import PoolData

store = get_debug()
pool_data = PoolData(store)
pool_data.players.add("test", "test@tes.com", "test")
pool_data.players.import_player("af1cda448a10ccb6f57431902ed6f610e260a2fc4649806bb0b5acc8fcbc3683", "fred", "fjacob21@hotmail.com", "b2770147708c83a52d0494bf769238c27edb4ff99d8e342259aad4838fcbe097")
routes = web.RouteTableDef()

@routes.get('/')
async def hello(request):
    return web.Response(text="Hello, world")

@routes.get('/player')
async def get_players(request):
    return web.json_response(pool_data.players.serialize())

@routes.post('/player')
async def add_player(request):
    data = await request.json()
    player = pool_data.players.add(data["name"], data["email"], data["password"])
    return web.json_response(player.serialize())

@routes.post('/player/import')
async def import_player(request):
    data = await request.json()
    player = pool_data.players.import_player(data["id"], data["name"], data["email"], data["password"], data["admin"])
    return web.json_response(player.serialize())

@routes.get('/player/{name}')
async def get_player(request):
    name = request.match_info['name']
    return web.json_response(pool_data.players.get_name(name).serialize())

@routes.post('/player/{name}/login')
async def login_player(request):
    data = await request.json()
    name = request.match_info['name']
    player = pool_data.players.get_name(name)
    password = data["password"]
    return web.Response(text=str(player.login(password)))

@routes.delete('/player/{name}')
async def delete_player(request):
    name = request.match_info['name']
    player = pool_data.players.get_name(name)
    pool_data.players.delete(player.id)
    return web.Response(text="True")

async def test_thread(app):
    try:
        while True:
            print("demo")
            await asyncio.sleep(1)
    except asyncio.CancelledError:
        pass


async def start_background_tasks(app):
    app['redis_listener'] = asyncio.create_task(test_thread(app))


async def cleanup_background_tasks(app):
    app['redis_listener'].cancel()
    await app['redis_listener']


app = web.Application()
app.add_routes(routes)
app.on_startup.append(start_background_tasks)
app.on_cleanup.append(cleanup_background_tasks)
web.run_app(app)

if __name__ == "__main__":
    print("Super test")
