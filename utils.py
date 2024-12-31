from kokoro_copy import normalize_text,phonemize,generate
import re
import librosa
import os
import uuid
from pydub.silence import split_on_silence
from pydub import AudioSegment
import wave
import numpy as np
import torch
debug=False
def resplit_strings(arr):
    # Handle edge cases
    if not arr:
        return '', ''
    if len(arr) == 1:
        return arr[0], ''
    # Try each possible split point
    min_diff = float('inf')
    best_split = 0
    # Calculate lengths when joined with spaces
    lengths = [len(s) for s in arr]
    spaces = len(arr) - 1  # Total spaces needed
    # Try each split point
    left_len = 0
    right_len = sum(lengths) + spaces
    for i in range(1, len(arr)):
        # Add current word and space to left side
        left_len += lengths[i-1] + (1 if i > 1 else 0)
        # Remove current word and space from right side
        right_len -= lengths[i-1] + 1
        diff = abs(left_len - right_len)
        if diff < min_diff:
            min_diff = diff
            best_split = i
    # Join the strings with the best split point
    return ' '.join(arr[:best_split]), ' '.join(arr[best_split:])

def recursive_split(text, voice):
    if not text:
        return []
    tokens = phonemize(text, voice, norm=False)
    if len(tokens) < 511:
        return [(text, tokens, len(tokens))] if tokens else []
    if ' ' not in text:
        return []
    for punctuation in ['!.?…', ':;', ',—']:
        splits = re.split(f'(?:(?<=[{punctuation}])|(?<=[{punctuation}]["\'»])|(?<=[{punctuation}]["\'»]["\'»])) ', text)
        if len(splits) > 1:
            break
        else:
            splits = None
    splits = splits or text.split(' ')
    a, b = resplit_strings(splits)
    return recursive_split(a, voice) + recursive_split(b, voice)

def segment_and_tokenize(text, voice, skip_square_brackets=True, newline_split=2):    
    if skip_square_brackets:
        text = re.sub(r'\[.*?\]', '', text)
    texts = [t.strip() for t in re.split('\n{'+str(newline_split)+',}', normalize_text(text))] if newline_split > 0 else [normalize_text(text)]
    segments = [row for t in texts for row in recursive_split(t, voice)]
    return [(i, *row) for i, row in enumerate(segments)]


def large_text(text,VOICE_NAME):
    if len(text) <= 500:
        return [(0, text, len(text))]
    else:
        result=segment_and_tokenize(text, VOICE_NAME[0])
        filtered_result = [(row[0], row[1], row[3]) for row in result]
        return filtered_result
    

def clamp_speed(speed):
    if not isinstance(speed, float) and not isinstance(speed, int):
        return 1
    elif speed < 0.5:
        return 0.5
    elif speed > 2:
        return 2
    return speed

def clamp_trim(trim):
    if not isinstance(trim, float) and not isinstance(trim, int):
        return 0.5
    elif trim <= 0:
        return 0
    elif trim > 1:
        return 0.5
    return trim

def trim_if_needed(out, trim):
    if not trim:
        return out
    a, b = librosa.effects.trim(out, top_db=30)[1]
    a = int(a*trim)
    b = int(len(out)-(len(out)-b)*trim)
    return out[a:b]    


def get_random_file_name(output_file, temp_folder="./kokoro_audio"):
    if output_file=="":
        random_id = str(uuid.uuid4())[:8]
        output_file = f"{temp_folder}/{random_id}.wav"
        return output_file
    # Ensure temp_folder exists 
    if not os.path.exists(output_file):
        return output_file   
    try:
        if output_file and os.path.exists(output_file):
            os.remove(output_file)  # Try to remove the file if it exists
            return output_file      # Return the same name if the file was successfully removed
    except Exception as e:
        # print(f"Error removing file {output_file}: {e}")
        random_id = str(uuid.uuid4())[:8]
        output_file = f"{temp_folder}/{random_id}.wav"
        return output_file
    

def remove_silence_function(file_path,minimum_silence=50):
    # Extract file name and format from the provided path
    output_path = file_path.replace(".wav", "_no_silence.wav")
    audio_format = "wav"
    # Reading and splitting the audio file into chunks
    sound = AudioSegment.from_file(file_path, format=audio_format)
    audio_chunks = split_on_silence(sound,
                                    min_silence_len=100,
                                    silence_thresh=-45,
                                    keep_silence=minimum_silence) 
    # Putting the file back together
    combined = AudioSegment.empty()
    for chunk in audio_chunks:
        combined += chunk
    combined.export(output_path, format=audio_format)
    return output_path

import simpleaudio as sa
def play_audio(filename):
    wave_obj = sa.WaveObject.from_wave_file(filename)
    play_obj = wave_obj.play()
    play_obj.wait_done()




def tts(MODEL,device,text, voice_name, speed=1.0, trim=0.5, pad_between_segments=0.5, output_file="",remove_silence=True,minimum_silence=50):
    segments = large_text(text, voice_name)
    VOICEPACK = torch.load(f'voices/{voice_name}.pt', weights_only=True).to(device)
    speed = clamp_speed(speed)
    trim = clamp_trim(trim)
    silence_duration = clamp_trim(pad_between_segments)
    output_file=get_random_file_name(output_file)
    if debug:
        print(f'Loaded voice: {voice_name}')
        print(f"Speed: {speed}")
        print(f"Trim: {trim}")
        print(f"Silence duration: {silence_duration}")
    sample_rate = 24000  # Sample rate of the audio

    # Create a silent audio segment in float32
    silence = np.zeros(int(sample_rate * silence_duration), dtype=np.float32)

    # Open a WAV file for writing
    with wave.open(output_file, 'wb') as wav_file:
        wav_file.setnchannels(1)  # Mono
        wav_file.setsampwidth(2)  # 16-bit audio
        wav_file.setframerate(sample_rate)

        for i in segments:
            id = i[0]
            text = i[1]
            if debug:
                print(i)
            audio, out_ps = generate(MODEL, text, VOICEPACK, lang=voice_name[0], speed=speed)
            audio = trim_if_needed(audio, trim)

            # Scale audio from float32 to int16
            audio = (audio * 32767).astype(np.int16)

            # Write the audio segment to the WAV file
            wav_file.writeframes(audio.tobytes())
            
            # Add silence between segments, except after the last segment
            if id != len(segments) - 1:
                wav_file.writeframes((silence * 32767).astype(np.int16).tobytes())
    if remove_silence:
        output_file=remove_silence_function(output_file,minimum_silence=minimum_silence)
    return output_file



def tts_file_name(text, temp_folder="./kokoro_audio"):
    # Remove all non-alphabetic characters and convert to lowercase
    text = re.sub(r'[^a-zA-Z\s]', '', text)  # Retain only alphabets and spaces
    text = text.lower().strip()             # Convert to lowercase and strip leading/trailing spaces
    text = text.replace(" ", "_")           # Replace spaces with underscores
    
    # Truncate or handle empty text
    truncated_text = text[:25] if len(text) > 25 else text if len(text) > 0 else "empty"
    
    # Generate a random string for uniqueness
    random_string = uuid.uuid4().hex[:8].upper()
    
    # Construct the file name
    file_name = f"{temp_folder}/{truncated_text}_{random_string}.wav"
    return file_name
