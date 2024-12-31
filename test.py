from models import build_model
from utils import tts,play_audio
import torch

print("Loading model...")
device = 'cuda' if torch.cuda.is_available() else 'cpu'
print(f'Using device: {device}')
MODEL = build_model('kokoro-v0_19.pth', device)
print("Model loaded successfully.")


voice_list = [
    'af', # Default voice is a 50-50 mix of af_bella & af_sarah
    'af_bella', 'af_sarah', 'am_adam', 'am_michael',
    'bf_emma', 'bf_isabella', 'bm_george', 'bm_lewis',
]
    
def tts_maker(text,voice_name="af_bella",speed = 0.8,trim=0,pad_between=0,save_path="temp.wav",remove_silence=False,minimum_silence=50):
    # global voice_list
    # voice_name=voice_list[1]
    audio_path=tts(MODEL,device,text,voice_name,speed=speed,trim=trim,pad_between_segments=pad_between,output_file=save_path,remove_silence=remove_silence,minimum_silence=minimum_silence)
    return audio_path

while True:
    text = input("Enter text to convert to speech: ")
    if text == "exit":
        break
    audio_path=tts_maker(text)
    play_audio(audio_path)