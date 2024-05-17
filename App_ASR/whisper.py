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

class WhisperModelWrapper:
    def __init__(self, model_size="medium.en", precision="float16", language="en"):
        self.model_size_or_path = model_size
        self.language = language
        if precision == "float16":
            # Run on GPU with FP16
            self.model = WhisperModel(
                self.model_size_or_path, device="cuda", compute_type="float16"
            )
        elif precision == "int8_float16":
            # Run on GPU with INT8
            self.model = WhisperModel(
                self.model_size_or_path, device="cuda", compute_type="int8_float16"
            )

    def transcribe(self, audio):
        segments, _ = self.model.transcribe(
            audio=audio, beam_size=7, language=self.language, without_timestamps=True
        )
        return segments
