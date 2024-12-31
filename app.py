from models import build_model
from utils import tts,tts_file_name
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


def text_to_speech(text, voice_name, speed, trim, pad_between_segments, remove_silence, minimum_silence):
    if not minimum_silence:
        minimum_silence=0.05
    keep_silence=int(minimum_silence * 1000)
    save_at=tts_file_name(text)
    audio_path = tts_maker(text, voice_name, speed, trim, pad_between_segments,save_at, remove_silence, keep_silence)
    return audio_path



import gradio as gr

# voice_list = [
#     'af',  # Default voice is a 50-50 mix of af_bella & af_sarah
#     'af_bella', 'af_sarah', 'am_adam', 'am_michael',
#     'bf_emma', 'bf_isabella', 'bm_george', 'bm_lewis',
# ]

import os
voice_list=[]
for i in os.listdir("./voices"):
    voice_list.append(i.replace(".pt",""))   
# print(voice_list)     

def toggle_autoplay(autoplay):
    return gr.Audio(interactive=False, label='Output Audio', autoplay=autoplay)

with gr.Blocks() as demo:
    gr.Markdown("<h1 style='text-align:center;'>Kokoro TTS</h1>")
    with gr.Row():
        with gr.Column():
            text = gr.Textbox(
                label='Enter Text',
                lines=3,
                placeholder="Type your text here..."
            )
            with gr.Row():
                voice = gr.Dropdown(
                    voice_list, 
                    value='af_bella', 
                    allow_custom_value=False, 
                    label='Voice', 
                    info='Starred voices are more stable'
                )
            with gr.Row():
                generate_btn = gr.Button('Generate', variant='primary')
            with gr.Accordion('Audio Settings', open=False):
                remove_silence = gr.Checkbox(value=False, label='✂️ Remove Silence From TTS')
                minimum_silence = gr.Number(
                    label="Keep Silence Upto (In seconds)", 
                    value=0.05
                )
                speed = gr.Slider(
                    minimum=0.25, maximum=2, value=1, step=0.1, 
                    label='⚡️Speed', info='Adjust the speaking speed'
                )
                trim = gr.Slider(
                    minimum=0, maximum=1, value=0, step=0.1, 
                    label='🔪 Trim', info='How much to cut from both ends of each segment'
                )   
                pad_between = gr.Slider(
                    minimum=0, maximum=2, value=0, step=0.1, 
                    label='🔇 Pad Between', info='Silent Duration between segments [For Large Text]'
                )
                
        with gr.Column():
            audio = gr.Audio(interactive=False, label='Output Audio', autoplay=True)
            with gr.Accordion('Enable Autoplay', open=False):
                autoplay = gr.Checkbox(value=True, label='Autoplay')
                autoplay.change(toggle_autoplay, inputs=[autoplay], outputs=[audio])

    text.submit(
        text_to_speech, 
        inputs=[text, voice, speed, trim, pad_between, remove_silence, minimum_silence], 
        outputs=[audio]
    )
    generate_btn.click(
        text_to_speech, 
        inputs=[text, voice, speed, trim, pad_between, remove_silence, minimum_silence], 
        outputs=[audio]
    )



import click
@click.command()
@click.option("--debug", is_flag=True, default=False, help="Enable debug mode.")
@click.option("--share", is_flag=True, default=False, help="Enable sharing of the interface.")
def main(debug, share):
    demo.queue().launch(debug=debug, share=share)
if __name__ == "__main__":
    main()    
