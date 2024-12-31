from models import build_model
from utils import tts,play_audio
import torch

print("Loading model...")
device = 'cuda' if torch.cuda.is_available() else 'cpu'
print(f'Using device: {device}')
MODEL = build_model('kokoro-v0_19.pth', device)
print("Model loaded successfully.")



# import os
# available_voices=[]
# for i in os.listdir("./voices"):
#     available_voices.append(i.replace(".pt",""))  
#  print(available_voices)   

available_voices= [
    'af', # Default voice is a 50-50 mix of Bella & Sarah
    'af_bella', 'af_sarah', 'am_adam', 'am_michael',
    'bf_emma', 'bf_isabella', 'bm_george', 'bm_lewis',
    'af_nicole', # ASMR voice
]
# for use
text="Hello, I am a text-to-speech model. I can generate audio from text."
voice_name="af_bella"
speed=0.8
trim=0
pad_between=0
save_path="temp.wav"
remove_silence=False
minimum_silence=50
audio_path=tts(MODEL,device,text,voice_name,speed=speed,trim=trim,pad_between_segments=pad_between,output_file=save_path,remove_silence=remove_silence,minimum_silence=minimum_silence)
play_audio(audio_path)
