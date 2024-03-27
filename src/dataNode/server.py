import asyncio
from filetransfer.servicer import grpcServer
from services.auth import login
from api import heartbeat as heartbeat_app
import uvicorn
from dotenv import load_dotenv
import os

load_dotenv()

async def run_uvicorn():
    config = uvicorn.Config(heartbeat_app.app, host="0.0.0.0", port=int(os.getenv("HEARTBEAT_PORT")), loop="asyncio")
    server = uvicorn.Server(config)
    await server.serve()

async def main():
    print(login())
    await asyncio.gather(
        run_uvicorn(),
        grpcServer(),
    )

if __name__ == "__main__":
    asyncio.run(main())