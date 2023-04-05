import hashlib
import pytest
from aiohttp import web


@pytest.fixture
async def aiohttp_server(aiohttp_server_factory):
    async def server(app):
        return await aiohttp_server_factory(app, ssl=None)
    return server


@pytest.fixture
async def aiohttp_client(aiohttp_client):
    return aiohttp_client


@pytest.mark.asyncio
async def test_download_and_hash(aiohttp_client, aiohttp_server):
    path = '/test'
    content = b'test content'
    expected_result = hashlib.md5(content).hexdigest()
    app = web.Application()
    app.router.add_get(path, lambda request: web.Response(body=content))
    async with aiohttp_server(app) as server:
        async with aiohttp_client(server) as client:
            response = await client.get(path)
            assert response.status == 200
            assert response.read() == content
            assert response.headers['Content-Type'] == 'application/octet-stream'
            assert hashlib.md5(await response.read()).hexdigest() == expected_result




