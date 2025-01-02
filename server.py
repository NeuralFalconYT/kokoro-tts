from fastapi import FastAPI
from fastapi.responses import FileResponse
from pydantic import BaseModel
import os
import uvicorn
from models import build_model
from utils import tts, tts_file_name
import torch

# Initialize FastAPI app
app = FastAPI(title="Kokoro TTS API", description="Text-to-Speech API using FastAPI", version="1.0")

# Load TTS model
device = 'cuda' if torch.cuda.is_available() else 'cpu'
print(f'Using device: {device}')
MODEL = build_model('kokoro-v0_19.pth', device)
print("Model loaded successfully.")

# Load available voices
voice_list = []
for file in os.listdir("./voices"):
    if file.endswith(".pt"):
        voice_list.append(file.replace(".pt", ""))

class TTSRequest(BaseModel):
    text: str
    voice_name: str = "af_bella"
    speed: float = 1.0
    trim: float = 0.0
    pad_between_segments: float = 0.0
    remove_silence: bool = False
    minimum_silence: float = 0.05

def tts_maker(text, voice_name="af_bella", speed=0.8, trim=0, pad_between=0, save_path="temp.wav", remove_silence=False, minimum_silence=50):
    audio_path = tts(MODEL, device, text, voice_name, speed=speed, trim=trim, pad_between_segments=pad_between, output_file=save_path, remove_silence=remove_silence, minimum_silence=minimum_silence)
    return audio_path

@app.get("/voices", summary="Get available voices")
async def get_voices():
    """Returns a list of available voices."""
    return {"voices": voice_list}

@app.post("/tts", summary="Generate TTS audio")
async def generate_tts(request: TTSRequest):
    """Generates speech audio from the provided text."""
    # Generate file name based on the input text
    save_at = tts_file_name(request.text)
    keep_silence = int(request.minimum_silence * 1000)

    # Generate the audio
    audio_path = tts_maker(
        request.text,
        request.voice_name,
        request.speed,
        request.trim,
        request.pad_between_segments,
        save_at,
        request.remove_silence,
        keep_silence
    )

    # Return the audio file
    return FileResponse(audio_path, media_type="audio/wav", filename=os.path.basename(audio_path))

if __name__ == "__main__":
    print("Open This address: http://127.0.0.1:8082/docs")
    uvicorn.run(app, host="127.0.0.1", port=8082)
    ## ifconfig to get your laptop ip address
    # laptop_ip_address = "192.168.0.30"
    # uvicorn.run(app, host=laptop_ip_address, port=8080)


   
# #For client side
# import requests
# import json
# import os 

# def tts(
#     text, 
#     voice_name="af_bella", 
#     speed=1, 
#     trim=0, 
#     pad_between_segments=0, 
#     remove_silence=True, 
#     minimum_silence=0.05,
#     folder_path="."
# ):
#     # Preprocess the text
#     text = text.strip().replace('\n', ' ')

#     # API request payload
#     payload = {
#         "text": text,
#         "voice_name": voice_name,
#         "speed": speed,
#         "trim": trim,
#         "pad_between_segments": pad_between_segments,
#         "remove_silence": remove_silence,
#         "minimum_silence": minimum_silence
#     }

#     try:
#         # Send POST request to TTS API
#         response = requests.post(
#             url="http://127.0.0.1:8082/tts",
#             headers={"accept": "application/json", "Content-Type": "application/json"},
#             data=json.dumps(payload)
#         )

#         # Check for successful response
#         response.raise_for_status()
#         #get file name
#         data=dict(response.headers)
#         f_name=data['content-disposition'].replace("attachment; filename=","").replace('"','')
#         print(f_name)
#         tts_save_path=f"{folder_path}/{f_name}"
#         with open(tts_save_path, "wb") as audio_file:
#             audio_file.write(response.content)

#         print(f"Audio saved to {tts_save_path}")
#         return tts_save_path
#     except requests.exceptions.RequestException as e:
#         print(f"Error making TTS request: {e}")
#         return None
    
# os.makedirs("./temp_audio",exist_ok=True)
# ttspath=tts("I love Kokoro TTS",folder_path="./temp_audio")
# print(ttspath)
