#! /usr/bin/env python
import asyncio
import argparse
import pyaudio
import numpy as np
import webrtcvad
from concurrent.futures import ThreadPoolExecutor
from typing import List, NamedTuple, Optional
from faster_whisper import WhisperModel

class VadWrapper:
    def __init__(self):
        self.vad = webrtcvad.Vad(3)
        self.RATE = 16000
        self.SILENT_CHUNKS_THRESHOLD = 10

    def is_speech(self, in_data):
        return self.vad.is_speech(in_data, self.RATE)
