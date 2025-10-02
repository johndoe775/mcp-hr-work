import asyncio
from fastmcp import Client

client = Client("http://localhost:8000/mcp")


async def call_tool(name: str):
    async with client:
        tools = await client.list_tools()
        print(tools)


asyncio.run(call_tool("Dinesh"))
# fastmcp run my_server.py:mcp --transport http --port 8000
