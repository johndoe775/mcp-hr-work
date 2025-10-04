import asyncio
from fastmcp import Client

client = Client("http://localhost:8000/mcp")


async def call_tool():
    async with client:
        for i in await client.list_tools():
            print(i)


asyncio.run(call_tool())
# fastmcp run my_server.py:mcp --transport http --port 8000
