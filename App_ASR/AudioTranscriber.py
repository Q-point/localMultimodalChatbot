#! /usr/bin/env python
import asyncio
import argparse
import pyaudio
import queue
import numpy as np
import webrtcvad
from concurrent.futures import ThreadPoolExecutor
from typing import List, NamedTuple, Optional
from faster_whisper import WhisperModel
from whisper import WhisperModelWrapper
from utilities import *
from vad import VadWrapper
import websockets


def create_audio_stream(selected_device_index, callback):
    RATE = 16000
    CHUNK = 480
    FORMAT = pyaudio.paInt16
    CHANNELS = 1

    audio = pyaudio.PyAudio()
    stream = audio.open(
        format=FORMAT,
        channels=CHANNELS,
        rate=RATE,
        input=True,
        input_device_index=selected_device_index,
        frames_per_buffer=CHUNK,
        stream_callback=callback,
    )

    return stream

class AudioTranscriber:
    def __init__(self, model_size="medium.en", precision="float16", language="en"):
        self.model_wrapper = WhisperModelWrapper(model_size=model_size, precision=precision, language=language)
        self.vad_wrapper = VadWrapper()
        self.silent_chunks = 0
        self.speech_buffer = []
        self.audio_queue = queue.Queue()
        self.websocket_uri = "ws://localhost:8766"  # Change this to your WebSocket server URI


    async def send_to_websocket(self, message):
        try:
            async with websockets.connect(self.websocket_uri) as websocket:
                await websocket.send(message.encode())
                #print("Message sent to WebSocket server:", message)
        except Exception as e:
            print("Error while sending message to WebSocket server:", e)


        
    async def transcribe_audio(self):
        with ThreadPoolExecutor() as executor:
            while True:
                audio_data_np = await asyncio.get_event_loop().run_in_executor(
                    executor, self.audio_queue.get
                )
                segments = await asyncio.get_event_loop().run_in_executor(
                    executor, self.model_wrapper.transcribe, audio_data_np
                )   
                for segment in segments:
                    print(Color.YELLOW + segment.text + Color.RESET)
                    await self.send_to_websocket(segment.text)


    def process_audio(self, in_data, frame_count, time_info, status):
        is_speech = self.vad_wrapper.is_speech(in_data)

        if is_speech:
            self.silent_chunks = 0
            audio_data = np.frombuffer(in_data, dtype=np.int16)
            self.speech_buffer.append(audio_data)
        else:
            self.silent_chunks += 1

        if (
            not is_speech
            and self.silent_chunks > self.vad_wrapper.SILENT_CHUNKS_THRESHOLD
        ):
            if len(self.speech_buffer) > 10:
                audio_data_np = np.concatenate(self.speech_buffer)
                self.speech_buffer.clear()
                self.audio_queue.put(audio_data_np)
            else:
                # noise clear
                self.speech_buffer.clear()

        return (in_data, pyaudio.paContinue)

    def start_transcription(self, selected_device_index):
        stream = create_audio_stream(selected_device_index, self.process_audio)
        print("Speak now!")
        asyncio.run(self.transcribe_audio())
        stream.start_stream()
        try:
            while True:
                key = input("Press Enter to exit.\n")
                if not key:
                    break
        except KeyboardInterrupt:
            print("Interrupted.")
        finally:
            stream.stop_stream()
            stream.close()

