# Kokoro-TTS 
**Note:** This is not the official repository. This tutorial explains how to run [Kokoro-TTS](https://huggingface.co/hexgrad/Kokoro-82M) on Windows and Google Colab.<br><br>
[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/NeuralFalconYT/kokoro-tts/blob/main/kokoro_TTS.ipynb) <br>
[![hfspace](https://img.shields.io/badge/🤗-Space%20demo-yellow)](https://huggingface.co/spaces/hexgrad/Kokoro-TTS) <br>
### Windows Installation

1. **Install Git LFS:**
   ```
   git lfs install
   ```
   This command installs Git Large File Storage, required for managing large model files.

2. **Clone the Kokoro Model and Repository:**
   ```
   git clone https://huggingface.co/hexgrad/Kokoro-82M
   git clone https://github.com/NeuralFalconYT/kokoro-tts.git
   ```
   These commands clone the necessary model files and the TTS repository to your local machine.

3. **Copy the TTS Files to the Model Directory:**
   ```
   robocopy "kokoro-tts" "Kokoro-82M" /e /r:0
   ```
   This command copies the content from the `kokoro-tts` directory to the `Kokoro-82M` directory.

4. **Navigate to the Model Directory:**
   ```
   cd Kokoro-82M
   ```
   This changes the working directory to the model directory.

5. **Run `make_bat.py` to Generate Batch Files:**
   ```
   python make_bat.py
   ```
   This script automatically creates the necessary `.bat` files (`run_app.bat`, `run_cli.bat`) to simplify the process of running the application.

6. **Create a Python Virtual Environment:**
   ```
   python -m venv myenv
   ```
   This command creates a new Python virtual environment named `myenv` for isolating dependencies.

7. **Activate the Virtual Environment:**
   ```
   myenv\Scripts\activate
   ```
   This activates the virtual environment, enabling you to install and run dependencies in an isolated environment.

8. **Check CUDA Version:**
   ```
   nvcc --version
   ```
   This checks the installed version of CUDA to ensure compatibility with PyTorch.

9. **Install PyTorch:**
   Visit [PyTorch Get Started](https://pytorch.org/get-started/locally/) and install the version compatible with your CUDA setup. For example:
   ```
   pip install torch --index-url https://download.pytorch.org/whl/cu118
   ```

10. **Install Required Dependencies:**
    ```
    pip install -r requirements.txt
    ```
    This installs all the required Python libraries listed in the `requirements.txt` file.

11. **Install eSpeak NG:**
    - Download and install [eSpeak NG](https://github.com/espeak-ng/espeak-ng/releases/tag/1.51).
    - Download espeak-ng-X64.msi and install in default windows location
    - Make sure you install the eSpeak NG in ```C:\Program Files\eSpeak NG``` folder , or later, you will need to set it the path manually in ```kokoro_copy.py```
    - Set the following environment variables under System variables:
      ```
      ESPEAK_PATH: C:\Program Files\eSpeak NG
      ESPEAK_LIBRARY: C:\Program Files\eSpeak NG\libespeak-ng.dll
      ```
      This ensures that the TTS system can access eSpeak NG for speech synthesis.

12. **Verify eSpeak NG Installation:**
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
**Or, manually running the following commands:**
 ```
 myenv\Scripts\activate
 python app.py
 python cli.py
 ```

#### Credit:  
[Kokoro HuggingFace](https://huggingface.co/hexgrad/Kokoro-82M)

