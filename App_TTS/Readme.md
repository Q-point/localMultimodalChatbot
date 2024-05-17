## LLM with text to speech.

Activate conda

```
conda activate aibase

```

Install Piper, websockets 

```
sudo apt update 
sudo apt install espeak ffmpeg libespeak1
sudo apt-get install alsa-utils
pip install piper-tts

```

To test open 2 terminals and issue:

```
python mainApp_ttsollama.py
python text2websocket_client.py
```