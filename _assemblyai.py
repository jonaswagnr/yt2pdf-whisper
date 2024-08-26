import os
from pytube import YouTube
from pytube.cli import on_progress
import ffmpeg
import assemblyai as aai
from tqdm import tqdm

# Replace with your AssemblyAI API key
aai.settings.api_key = "719fe7ef5c4d438092b4a80903cbe7a1"

# YouTube video URL
VIDEO_URL = "https://www.youtube.com/watch?v=18sz2kApMlo"

# Initialize YouTube object with custom on_progress_callback
yt = YouTube(VIDEO_URL, on_progress_callback=on_progress)

# Get the best audio stream
audio_stream = yt.streams.get_audio_only()

# Construct the filename
file_title = yt.title.replace(" ", "_")
file_name = file_title + ".mp3"
# Create a directory for the audio file and transcript
output_dir = f"./output/{file_title}"
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# Construct the full file path
file_path = os.path.join(output_dir, file_name)

# Download the audio file
print("Downloading audio file...")
audio_stream.download(filename=file_path)
print("Download completed.")

# AssemblyAI configuration
config = aai.TranscriptionConfig(speaker_labels=True, language_detection=True)
transcriber = aai.Transcriber()

# Transcribe the audio file
transcript = transcriber.transcribe(file_path, config=config)

# Construct the transcript filename
transcript_filename = os.path.join(output_dir, f"{file_title}.txt")

# Save the transcript to a file
with open(transcript_filename, "w") as transcript_file:
    for utterance in transcript.utterances:
        transcript_file.write(f"Speaker {utterance.speaker}: {utterance.text}\n")

print(f"Transcript and audio saved in {output_dir}")


