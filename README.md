# kokoro-tts
[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/NeuralFalconYT/kokoro-tts/blob/main/kokoro_TTS.ipynb) <br>

### Windows Installation
```
git lfs install
```
```
git clone https://huggingface.co/hexgrad/Kokoro-82M
```
```
git clone https://github.com/NeuralFalconYT/kokoro-tts.git
```
```
robocopy "kokoro-tts" "Kokoro-82M" /e /r:0
```
```
cd Kokoro-82M
```

```
python -m venv myenv
```
```
myenv\Scripts\activate
```

```
nvcc --version
```
Visit https://pytorch.org/get-started/locally/ and install torch accoding to your cuda version for example
```
pip install torch --index-url https://download.pytorch.org/whl/cu118
```
```
pip install -r requirements.txt
```
```
python make_bat.py
```
```
https://github.com/espeak-ng/espeak-ng/releases/tag/1.51
```
```
Download and install espeak-ng-X64.msi
```
```
ESPEAK_PATH: C:\Program Files\eSpeak NG
ESPEAK_LIBRARY: C:\Program Files\eSpeak NG\libespeak-ng.dll
```
```
espeak-ng --version
```

To run the gradio app click on 
```
run_app.bat
```
To run on command line click on 
```
run_cli.bat
```
or,
```
myenv\Scripts\activate
python cli.py
python app.py
```
#### Credit:
[Kokoro HuggingFace](https://huggingface.co/hexgrad/Kokoro-82M)
