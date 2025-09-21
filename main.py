from src.mcp_client_anthropic import MCPClient
import asyncio
import sys
from dotenv import load_dotenv

load_dotenv()  # Load environment variables from .env file


async def client_loop(server_script_path: str):
    client = MCPClient()
    try:
        await client.connect_to_server(server_script_path)
        await client.chat_loop()
    finally:
        await client.cleanup()


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python client.py <path_to_server_script>")
        sys.exit(1)
    asyncio.run(client_loop(sys.argv[1]))
