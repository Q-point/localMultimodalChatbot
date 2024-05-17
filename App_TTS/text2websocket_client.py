#! /usr/bin/env python

import asyncio
import websockets

async def send_message(message):
    uri = "ws://localhost:8765"
    try:
        async with websockets.connect(uri) as websocket:
            await websocket.send(message)
    except (websockets.ConnectionClosedError, ConnectionRefusedError) as e:
        print(f"Error: {e}. Unable to connect to the server.")

if __name__ == "__main__":
    loop = asyncio.get_event_loop()

    try:
        while True:
            content_in = input(">>> ")
            if not content_in:
                continue

            if content_in.lower() in ('exit', 'quit', 'q'):
                break

            loop.run_until_complete(send_message(content_in))
    except KeyboardInterrupt:
        pass
    finally:
        loop.close()
