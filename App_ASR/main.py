#! /usr/bin/env python
import asyncio
import argparse
import pyaudio
import numpy as np
import webrtcvad
from concurrent.futures import ThreadPoolExecutor
from typing import List, NamedTuple, Optional
from faster_whisper import WhisperModel
from utilities import *
from AudioTranscriber import AudioTranscriber

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-s",
        "--model_size",
        type=str,
        default="medium.en",  #large-v2
        choices=model_sizes,
        help="Model size.",
    )
    parser.add_argument(
        "-p",
        "--precision",
        type=str,
        default="float16",  #int8_float16
        choices=precision_choices,
        help="Precision.",
    )
    parser.add_argument(
        "-l",
        "--language",
        type=str,
        default="en",
        choices=langs,
        help="Precision.",
    )
    args = parser.parse_args()

    model_size: str = args.model_size
    precision: str = args.precision
    language: str = args.language

    p = pyaudio.PyAudio()
    info = p.get_host_api_info_by_index(0)
    num_devices = info.get("deviceCount", 0)
    for i in range(num_devices):
        device_info = p.get_device_info_by_host_api_device_index(0, i)
        if device_info.get("maxInputChannels") > 0:
            print(f"Input Device ID {i}, - {device_info.get('name')}")
    device_index: int = int(input("Please input your microphone Device ID: "))
    transcriber = AudioTranscriber(model_size=model_size, precision=precision, language=language)
    transcriber.start_transcription(device_index)


if __name__ == '__main__':
    main()
