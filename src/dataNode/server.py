import asyncio
from filetransfer.servicer import grpcServer
from services.auth import login
from dotenv import load_dotenv


load_dotenv()

async def main():
    # print(login())

    await asyncio.gather(
        grpcServer(),
    )


if __name__ == "__main__":
    asyncio.run(main())

"""
{
    "/": {
        "children": {
            "hobar": 
                "children": {
                    shakira.mp3: { 
                        "blockId": ["/hobar/shakira.mp3/part001, /hobar/shakira.mp3/part002, /hobar/shakira.mp3/part003"],
                    }
                }
        }
    }
} 


"""