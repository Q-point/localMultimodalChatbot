# localMultimodalJetsonChatbot
A multimodal local chatbot with agentic capabilities running on Jetson AGX Orin


1. Start Ollama server
```
sudo ollama serve
```

2.

Build Docker container with fasterwhisper:

```
./build.sh --name=voiceai faster-whisper jupyterlab
```

Create /apps folder with App_ASR

Start Docker container:


```
./run.sh --volume /agxorin_ssd/jetson-containers/apps/:/home $(./autotag voiceai)
```

Install any required packages:

```
installaud.sh
```

If required modify :

a) Model 
b) Beam size
c) number format

3.
On a seperate terminal activate conda with python 3.10
and start either simple pipline or
CrewAI pipeline with contextual vision information.

```
python3 mainApp_ttsollama.python

```
