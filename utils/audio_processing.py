import yt_dlp
from pydub import AudioSegment

from pathlib import Path
import os

DOWNLOAD_DIR = "downloads"

def download_youtube_audio(url :str) ->str:
    output_path = os.path.join(DOWNLOAD_DIR, "%(title)s.%(ext)s")
    ydl_opts = {
        "format": "bestaudio/best",
        "outtmpl": output_path,
        "postprocessors": [
            {
                "key": "FFmpegExtractAudio",
                "preferredcodec": "wav",
                "preferredquality": "192",
            }
        ],
        "quiet": True,
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=True)
        filename = ydl.prepare_filename(info).replace(".webm", ".wav").replace(".m4a", ".wav")
    return filename

# data = "https://www.youtube.com/watch?v=pddCCgt-NVQ"
# audio_path = download_youtube_audio(data)
# print(audio_path)


def convert_to_wav(input_path: str) -> str:

    audio = AudioSegment.from_file(input_path)
    output_path = os.path.splitext(input_path)[0] + "_converted.wav"
    audio = audio.set_channels(1).set_frame_rate(16000) # mono, 16 khz
    audio.export(output_path, format="wav")
    return output_path

# .venv\Scripts\Activate.ps1

# print(convert_to_wav(audio_path))

# wav_data = convert_to_wav(audio_path)

def chunk_audio(wav_path: str, chunk_minutes: int = 10) ->list:
    audio = AudioSegment.from_wav(wav_path)
    chunk_ms = chunk_minutes * 60 * 1000 # milliseconds
    chunks = []

    for i, start in enumerate(range(0, len(audio), chunk_ms)):

        chunk = audio[start: start + chunk_ms]
        chunk_path = f"{wav_path}_chunk_{i}.wav"

        chunk.export(chunk_path, format="wav")
        chunks.append(chunk_path)

    return chunks

# print(chunk_audio(wav_data))

def process_input(source: str)->str:

    if source.startswith("https://") or source.startswith("http://"):

        print("Detected YT URL")
        wav_path = download_youtube_audio(source)
    else:
        print("Detected local file")
        wav_path = convert_to_wav(source)

    print("Chunking audio...")
    chunks = chunk_audio(wav_path)

    print(f"Audio ready - #{len(chunks)} chunks created.")

    return chunks