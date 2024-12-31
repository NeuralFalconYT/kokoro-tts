# kokoro-tts

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
