#!/usr/bin/env python3

from aiohttp import web
import asyncio
import time

routes = web.RouteTableDef()

@routes.get('/')
async def hello(request):
    return web.Response(text="Hello, world")

async def test_thread(app):
    try:
        while True:
            print("test")
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
