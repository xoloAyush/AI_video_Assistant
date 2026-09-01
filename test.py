from utils.audio_processing import process_input
from core.transcriber import transcribe_all
from pathlib import Path


url = "https://www.youtube.com/watch?v=2ZU3j4GQ4K8"

# 1. Download + process + chunk
chunks = process_input(url)

print(chunks)

# 2. Transcribe
text = transcribe_all(chunks, translate=True)

print("Transcription completed")


# 3. Create transcription folder
transcription_dir = Path("transcriptions")
transcription_dir.mkdir(parents=True, exist_ok=True)


# 4. Extract YouTube video ID
video_id = url.split("v=")[-1]

# 5. Save transcript
transcription_file = transcription_dir / f"transcript_{video_id}.txt"

with open(transcription_file, "w", encoding="utf-8") as file:
    file.write(text)


print(f"Transcription saved to: {transcription_file}")