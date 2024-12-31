# kokoro-tts
```
python -m venv myenv
```
On Windows:
```
myenv\Scripts\activate
```
```
git clone https://huggingface.co/hexgrad/Kokoro-82M
```
```
https://github.com/NeuralFalconYT/kokoro-tts.git
```
```
robocopy "kokoro-tts" "Kokoro-82M" /e /r:0
```
```
cd Kokoro-82M
```
```
nvcc --version
```
Visit https://pytorch.org/get-started/locally/ and install torch accoding to your cuda version for example
```
pip install torch --index-url https://download.pytorch.org/whl/cu118
```
```
https://github.com/espeak-ng/espeak-ng/releases/tag/1.51
```
```
Download and install espeak-ng-X64.msi
```
```
PHONEMIZER_ESPEAK_PATH: c:\Program Files\eSpeak NG
PHONEMIZER_ESPEAK_LIBRARY: c:\Program Files\eSpeak NG\libespeak-ng.dll
```
