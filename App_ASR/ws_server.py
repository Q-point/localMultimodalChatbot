import asyncio
import websockets
import signal

async def handle(websocket, path):
    messages = []
    selected_device_index = 0  # Set your desired device index here

    async for message in websocket:
        decoded_message = message.decode()  # Decode bytes to string
        print(f"Received message: {decoded_message}")
        messages.append({'role': 'user', 'content': decoded_message})

        # Add your message processing logic here

async def main():
    server = await websockets.serve(handle, 'localhost', 8766)
    print('Websocket server started at ws://localhost:8766')

    shutdown_event = asyncio.Event()

    async def shutdown(signal):
        print(f"Received {signal}. Shutting down gracefully.")
        server.close()
        await server.wait_closed()
        shutdown_event.set()

    loop = asyncio.get_event_loop()
    loop.add_signal_handler(signal.SIGINT, lambda: asyncio.create_task(shutdown("SIGINT")))
    loop.add_signal_handler(signal.SIGTERM, lambda: asyncio.create_task(shutdown("SIGTERM")))

    try:
        await asyncio.gather(server.wait_closed(), shutdown_event.wait())
    except asyncio.CancelledError:
        pass

if __name__ == "__main__":
    asyncio.run(main())
