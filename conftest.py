import asyncio
import pytest
from aiohttp import web
from aiohttp.test_utils import TestServer


@pytest.fixture
def loop():
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture
async def aiohttp_server_factory(loop, aiohttp_unused_port):
    servers = []

    async def create_server(app: web.Application):
        server = TestServer(app, port=aiohttp_unused_port)
        await server.start_server()
        servers.append(server)
        return server

    yield create_server

    for server in servers:
        await server.close()
