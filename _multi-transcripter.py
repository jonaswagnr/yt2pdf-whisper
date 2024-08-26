import os
import sys
import tqdm
import whisper
from pytube import YouTube
from moviepy.editor import *

# Custom ProgressBar for Whisper Transcription
class _CustomProgressBar(tqdm.tqdm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._current = self.n

    def update(self, n):
        super().update(n)
        self._current += n
        progress_percentage = (self._current / self.total) * 100
        print(f"Progress: {progress_percentage:.2f}%", end="\r")

# Injecting CustomProgressBar into Whisper's tqdm
import whisper.transcribe 
transcribe_module = sys.modules['whisper.transcribe']
transcribe_module.tqdm.tqdm = _CustomProgressBar

# Function to download audio from YouTube
def download_audio(youtube_url, output_dir):
    yt = YouTube(youtube_url)
    title = yt.title
    valid_filename = "".join(char for char in title if char.isalnum() or char in [" ", "_"]).rstrip()
    
    target_dir = os.path.join(output_dir, valid_filename)
    if not os.path.exists(target_dir):
        os.makedirs(target_dir)

    video = yt.streams.filter(only_audio=True).first()
    out_file = video.download(output_path=target_dir, filename=valid_filename)
    new_file = os.path.join(target_dir, valid_filename + ".mp3")
    clip = AudioFileClip(out_file)
    clip.write_audiofile(new_file)
    clip.close()
    os.remove(out_file)
    return new_file, valid_filename

# Function to transcribe audio using Whisper
def transcribe_audio(file_path):
    model = whisper.load_model("base")
    result = model.transcribe(file_path)
    return result["text"]

# Function to save the transcription
def save_transcription(transcription, output_filename):
    with open(output_filename, "w") as file:
        file.write(transcription)

# Main script execution
if __name__ == "__main__":
    youtube_urls = [
        "https://www.youtube.com/watch?v=qKhpGqIQKog"
        # Add more YouTube URLs here
    ]

    output_dir = "output"
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    for url in youtube_urls:
        try:
            print(f"Processing {url}...")
            audio_file, filename = download_audio(url, output_dir)
            transcription = transcribe_audio(audio_file)
            save_transcription(transcription, os.path.join(output_dir, filename, filename + ".txt"))
            print(f"Completed processing for {url}")
        except Exception as e:
            print(f"Error processing {url}: {e}")

