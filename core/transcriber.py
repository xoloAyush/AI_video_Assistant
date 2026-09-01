import os
import whisper

WHISPER_MODEL = os.getenv("WHISPER_MODEL", "small")

_model = None

def load_model():
    
    global _model

    if _model is None:
        print(f"Loading Whisper ({WHISPER_MODEL})...")
        _model = whisper.load_model(WHISPER_MODEL)
        print("whisper model loaded successfully.")

    return _model

def transcribe(chunk: str, translate: bool) -> str:

    model = load_model()

    task = "translate" if translate else "transcribe"

    result = model.transcribe(chunk, task=task)

    return result["text"]


def transcribe_all(chunks: list, translate: bool) -> str:

    full_transcript = ""

    for i , chunk in enumerate(chunks):
        print(f"transcribing chunk {i+1}")

        text = transcribe(chunk, translate)

        full_transcript += text + " "
        print("Transcription completed")

    return full_transcript