from models import build_model
from utils import tts,play_audio
import torch
import os
from rich.console import Console
console = Console()

console.print("Loading model...", style="bold red")
device = 'cuda' if torch.cuda.is_available() else 'cpu'
# print(f'Using device: {device}')
console.print(f"Using device: [bold green]{device}[/bold green]")

MODEL = build_model('kokoro-v0_19.pth', device)
console.print("Model loaded successfully.", style="bold red")


#For testing
def tts_maker(text,voice_name="af_bella",speed = 0.8,trim=0,pad_between=0,save_path="temp.wav",remove_silence=False,minimum_silence=50):
    # global voice_list
    # voice_name=voice_list[1]
    audio_path=tts(MODEL,device,text,voice_name,speed=speed,trim=trim,pad_between_segments=pad_between,output_file=save_path,remove_silence=remove_silence,minimum_silence=minimum_silence)
    return audio_path



voice_dict = {
    1: 'af',  # Default voice is a 50-50 mix of af_bella & af_sarah
    2: 'af_bella',
    3: 'af_sarah',
    4: 'am_adam',
    5: 'am_michael',
    6: 'bf_emma',
    7: 'bf_isabella',
    8: 'bm_george',
    9: 'bm_lewis',
}


def clear_screen():
    # Clear the terminal screen based on the operating system
    os.system('cls' if os.name == 'nt' else 'clear')

while True:
    console.print("Pick a voice from the following list:", style="bold green")
    
    # Display the voice options with color
    for key, voice in voice_dict.items():
        console.print(f"{key}: {voice}", style="cyan")

    try:
        # Get user input with styled text prompt
        voice_choice = int(input("Enter the number of the voice you want to use: "))
        if voice_choice not in voice_dict:
            console.print("Invalid choice. Please try again.", style="bold red")
            continue
        voice_name = voice_dict[voice_choice]
    except ValueError:
        console.print("Invalid input. Please enter a valid number.", style="bold red")
        continue

    console.print(f"You selected: {voice_name}", style="bold yellow")

    while True:
        text = input("\nEnter Text ('c' to Change voice, 'e' to quit): ")
        
        # Check for input commands to change voice or exit
        if text.lower() == "c":
            break  # Exit to select a new voice
        elif text.lower() == "e":
            console.print("Exiting program.", style="bold red")
            exit()  # Exit the entire program
        else:
            # Clear terminal screen before showing the next message
            clear_screen()

            # Use rich styling for the input text before generating audio
            console.print(f"Generating audio for: [bold magenta]{text}[/bold magenta]", style="bold green")
            
            audio_path = tts_maker(text, voice_name=voice_name)  # Replace with your function
            play_audio(audio_path)  # Replace with your function
