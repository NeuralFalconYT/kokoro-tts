# Kokoro-TTS 
**Note:** This is not the official repository. This tutorial explains how to run [Kokoro-82M](https://huggingface.co/hexgrad/Kokoro-82M) on Windows and Google Colab. You may encounter some bugs while running the Gradio app.<br>
It's a little bit messy, but you can visit [Hugging Face discussions](https://huggingface.co/hexgrad/Kokoro-82M/discussions) for an easy installation guide, even with ONNX Runtime.<br><br>
[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/NeuralFalconYT/kokoro-tts/blob/main/kokoro_TTS.ipynb) <br>
[![hfspace](https://img.shields.io/badge/🤗-Space%20demo-yellow)](https://huggingface.co/spaces/hexgrad/Kokoro-TTS) <br>
### Windows Installation
My Python Version is 3.10.9
1. **Install Git LFS:**
   ```
   git lfs install
   ```
   This command installs Git Large File Storage, required for managing large model files.

2. **Clone the Kokoro Model and Repository:**
   ```
   git clone https://huggingface.co/Remsky/kokoro-82m-mirror
   git clone https://github.com/NeuralFalconYT/kokoro-tts.git
   ```
   These commands clone the necessary model files and the TTS repository to your local machine.

3. **Copy the TTS Files to the Model Directory:**
   ```
   ren "kokoro-82m-mirror" "Kokoro-82M"
   ```

   ```
   robocopy "kokoro-tts" "Kokoro-82M" /e /r:0
   ```
   This command copies the content from the `kokoro-tts` directory to the `Kokoro-82M` directory.

5. **Navigate to the Model Directory:**
   ```
   cd Kokoro-82M
   ```
   This changes the working directory to the model directory.

6. **Run `make_bat.py` to Generate Batch Files:**
   ```
   python make_bat.py
   ```
   This script automatically creates the necessary `.bat` files (`run_app.bat`, `run_cli.bat`,`run_echo_bot.bat`,`get_new_voice.bat`) to simplify the process of running the application.

7. **Create a Python Virtual Environment:**
   ```
   python -m venv myenv
   ```
   This command creates a new Python virtual environment named `myenv` for isolating dependencies.

8. **Activate the Virtual Environment:**
   ```
   myenv\Scripts\activate
   ```
   This activates the virtual environment, enabling you to install and run dependencies in an isolated environment.

9. **Check CUDA Version:**
   ```
   nvcc --version
   ```
   This checks the installed version of CUDA to ensure compatibility with PyTorch.

10. **Install PyTorch:**
   Visit [PyTorch Get Started](https://pytorch.org/get-started/locally/) and install the version compatible with your CUDA setup. For example:
   ```
   pip install torch --index-url https://download.pytorch.org/whl/cu118
   ```

11. **Install Required Dependencies:**
    ```
    pip install -r requirements.txt
    ```
    This installs all the required Python libraries listed in the `requirements.txt` file.

12. **Install eSpeak NG:**<br>
      https://huggingface.co/hexgrad/Kokoro-82M/discussions/12#67742594fdeebf74f001ecfc
    - Download and install [eSpeak NG](https://github.com/espeak-ng/espeak-ng/releases/tag/1.51).
    - Download espeak-ng-X64.msi and install in default windows location
    - Make sure you install the eSpeak NG in ```C:\Program Files\eSpeak NG``` folder , or later, you will need to set it the path manually in ```kokoro_copy.py```
    - Set the following environment variables under System variables:
      ```
      ESPEAK_PATH: C:\Program Files\eSpeak NG
      ESPEAK_LIBRARY: C:\Program Files\eSpeak NG\libespeak-ng.dll
      ```
      This ensures that the TTS system can access eSpeak NG for speech synthesis.

13. **Verify eSpeak NG Installation:**
    ```
    espeak-ng --version
    ```
    This command verifies the installation of eSpeak NG.

### Running the Application

 **Run the Gradio App:**
   ```
   run_app.bat
   ```
   Clicking on `run_app.bat` starts the Gradio interface for interacting with the TTS system.

 **Use Kokoro TTS in Command Line:**
   ```
   run_cli.bat
   ```
  Clicking on `run_cli.bat` you can play with kokoro tts voicepack.
  
 **Use Kokoro TTS as a Echo Bot (Say Something and it will repeat that sentence):**
   ```
   run_echo_bot.bat
   ```
  Clicking on `run_echo_bot.bat` it will repeat what you said.

 **Download Latest VoicePack:**
   ```
   get_new_voice.bat
   ```
 **Use FastAPI server:**
   ```
   run_server.bat
   ```
   Then Open this url
   ```
   http://127.0.0.1:8082/docs
   ```
**Or, manually running the following commands:**
 ```
 myenv\Scripts\activate
 python app.py #for gradio app
 python cli.py #run in terminal
 python echo_bot.py #Say Something and it will repeat that sentence
 python test.py # Understand the funtion
 python server.py #To Use as a server
 ```

[Click to Download Kokoro Sample TTS audio](https://huggingface.co/hexgrad/Kokoro-82M/resolve/main/demo/HEARME.wav) <br>



https://github.com/user-attachments/assets/1f4d8713-c59d-4b4d-aec4-e88e08c6dbe0



https://github.com/user-attachments/assets/04047ed9-b2e6-4b2d-9dd2-0c4c87cec267




#### Credit:  
[Kokoro HuggingFace](https://huggingface.co/hexgrad/Kokoro-82M)

