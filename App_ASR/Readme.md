## Local Speech to text using Faster-whisper

1.
Build a local docker with faster-whisper package

```
./build.sh --name=voiceai faster-whisper jupyterlab
./run.sh --volume /agxorin_ssd/jetson-containers/apps/:/home $(./autotag voiceai)
```
2.
Copy App_ASR under jetson-containers/apps.
Install dependencies:

```
./installaud.sh
```

3.
Run two terminals with ws_server on one and main ASR app on the other.

```
python3 main.py
```

The websocket server is running on ws://localhost:8766

4. 
Note that there may be an initial delay.

On the VadWrapper you can change SILENT_CHUNKS_THRESHOLD and setting (1-3)
