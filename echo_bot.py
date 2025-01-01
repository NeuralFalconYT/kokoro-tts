# STS -> Speak To Speech
# This is for fun
from models import build_model
from utils import tts, play_audio
import torch
import os
from rich.console import Console
import speech_recognition as sr

console = Console()
recognizer = sr.Recognizer()
recognizer.energy_threshold = 2000
recognizer.pause_threshold = 1
recognizer.phrase_threshold = 0.1
recognizer.dynamic_energy_threshold = True
calibration_duration = 1
timeout = 10
phrase_time_limit = None

console.print("[bold magenta]Loading model...[/bold magenta]")
device = 'cuda' if torch.cuda.is_available() else 'cpu'
console.print(f"[bold cyan]Using device:[/bold cyan] [bold green]{device}[/bold green]")

MODEL = build_model('kokoro-v0_19.pth', device)
console.print("[bold magenta]Model loaded successfully.[/bold magenta]")

# For testing
def tts_maker(text, voice_name="af_bella", speed=1.0, trim=0, pad_between=0, save_path="temp.wav", remove_silence=False, minimum_silence=50):
    audio_path = tts(MODEL, device, text, voice_name, speed=speed, trim=trim, pad_between_segments=pad_between, output_file=save_path, remove_silence=remove_silence, minimum_silence=minimum_silence)
    return audio_path

# Load voice options
voice_dict = {}
for index, file in enumerate(os.listdir('./voices')):
    voice_dict[index + 1] = file.replace('.pt', '')

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def select_voice():
    while True:
        console.print("[bold blue]Pick a voice from the following list:[/bold blue]")
        for key, voice in voice_dict.items():
            console.print(f"[bold yellow]{key}[/bold yellow]: [bold green]{voice}[/bold green]")

        try:
            voice_choice = int(input("Enter the number of the voice you want to use:"))
            if voice_choice in voice_dict:
                return voice_dict[voice_choice]
            else:
                console.print("[bold red]Invalid choice. Please try again.[/bold red]")
        except ValueError:
            console.print("[bold red]Invalid input. Please enter a valid number.[/bold red]")

voice_name = select_voice()

while True:
    try:
        clear_screen()
        console.print(f"[bold blue]Currently using voice:[/bold blue] [bold green]{voice_name}[/bold green]")
        console.print("[bold magenta]Say 'change voice' to change the voice or say 'exit' to quit.[/bold magenta]")
        with sr.Microphone() as source:
            recognizer.adjust_for_ambient_noise(source, duration=calibration_duration)
            console.print("[bold cyan]Listening...[/bold cyan]")
            audio_data = recognizer.listen(source, timeout=timeout, phrase_time_limit=phrase_time_limit)

            # Recognize speech
            text = recognizer.recognize_google(audio_data, language="en")
            console.print(f"[bold yellow]Recognized:[/bold yellow] [bold white]{text}[/bold white]")

            if "change voice" in text.lower():
                console.print("[bold cyan]Changing voice...[/bold cyan]")
                voice_name = select_voice()
            elif "exit" in text.lower():
                console.print("[bold red]Exiting...[/bold red]")
                break
            else:
                # Generate TTS output
                audio_path = tts_maker(text, voice_name=voice_name)
                play_audio(audio_path)

    except sr.UnknownValueError:
        console.print("[bold red]Could not understand the audio. Please try again.[/bold red]")
    except sr.RequestError as e:
        console.print(f"[bold red]API error:[/bold red] [bold white]{e}[/bold white]")
    except Exception as e:
        console.print(f"[bold red]Error:[/bold red] [bold white]{e}[/bold white]")
