from huggingface_hub import list_repo_files, hf_hub_download
import os

# Ensure the 'voices' directory exists
os.makedirs('./voices', exist_ok=True)

# Replace with the repository ID
repo_id = "hexgrad/Kokoro-82M"

# Get the list of all files
files = list_repo_files(repo_id)

# Filter files for the 'voices/' folder
voice_files = [file.replace("voices/", "") for file in files if file.startswith("voices/")]

# Get current files in the 'voices' folder
current_voice = os.listdir('./voices')

# Identify files that need to be downloaded
download_voice = [file for file in voice_files if file not in current_voice]
print(f"Files to download: {download_voice}")
import shutil
# Download each missing file
for file in download_voice:
    file_path = hf_hub_download(repo_id=repo_id, filename=f"voices/{file}")
    target_path = f"./voices/{file}"
    shutil.copy(file_path, target_path)
    print(f"Downloaded: {file} to {target_path}")
