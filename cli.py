from models import build_model
from utils import tts,play_audio
import torch

print("Loading model...")
device = 'cuda' if torch.cuda.is_available() else 'cpu'
print(f'Using device: {device}')
MODEL = build_model('kokoro-v0_19.pth', device)
print("Model loaded successfully.")


def tts_maker(text,voice_name="af_bella",speed = 0.8,trim=0,pad_between=0,save_path="temp.wav",remove_silence=False,minimum_silence=50):
    # global voice_list
    # voice_name=voice_list[1]
    audio_path=tts(MODEL,device,text,voice_name,speed=speed,trim=trim,pad_between_segments=pad_between,output_file=save_path,remove_silence=remove_silence,minimum_silence=minimum_silence)
    return audio_path

voice_dict = {
    1: 'af',# Default voice is a 50-50 mix of af_bella & af_sarah
    2: 'af_bella',
    3: 'af_sarah',
    4: 'am_adam',
    5: 'am_michael',
    6: 'bf_emma',
    7: 'bf_isabella',
    8: 'bm_george',
    9: 'bm_lewis',
}

print("Pick a voice from the following list:")
for key in voice_dict:
    print(f"{key}: {voice_dict[key]}")
voice_choice = int(input("Enter the number of the voice you want to use: "))
voice_name = voice_dict[voice_choice]
while True:
    text = input("Enter text to generate audio: ")
    if text == "exit":
        break
    audio_path=tts_maker(text)
    play_audio(audio_path)
