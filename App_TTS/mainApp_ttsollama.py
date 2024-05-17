#! /usr/bin/env python

import piperengine as engine
import shutil
import asyncio
import argparse
import ollama
import websockets
import signal
import sys
import logging  # Import the logging module
import string 

logging.basicConfig(level=logging.ERROR)  # Set the logging level to ERROR

client = ollama.AsyncClient(host='http://localhost:11434')
engine.load('en_GB-alba-medium.onnx')

PUNCTUATION = [".", "?", "!", ":", ";", "*", "-", "**"]

async def play_audio_on_device(text, device_index=0):
    engine.say(text)

async def speak(content, device_index=0):
    await play_audio_on_device(content, device_index)

async def handle(websocket, path):
    messages = []
    selected_device_index = 0  # Set your desired device index here

    try:
        async for received_message in websocket:
            print(f"Received message: {received_message}")               
            if received_message is not None:
                # Filter out punctuation marks from the received message
                # cleaned_message = ''.join(char for char in received_message if char not in string.punctuation)
                messages.append({'role': 'user', 'content': received_message.decode()})

                content_out = ''
                try:
                    async for response in await client.chat(model='mistral', messages=messages, stream=True):
                        if response['done']:
                            messages.append({'role': 'assistant', 'content': content_out})
                            content_out = ''

                        content = response['message']['content']
                        print(content, end='', flush=True)

                        content_out += content
                        if content in PUNCTUATION:
                            await speak(content_out, selected_device_index)
                            content_out = ''
      
                except RuntimeError as e:
                                logging.error(f"RuntimeError occurred during message processing: {e}")
          
    except RuntimeError as e:
        logging.error(f"RuntimeError occurred: {e}")
        pass  
        

async def main():
    selected_device_index = 0  # Set your desired device index here
    messages = []
    
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
