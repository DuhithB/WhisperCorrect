import whisper

model = whisper.load_model("base")  # Or 'small'/'medium' if you have GPU

def transcribe_audio(file_path: str) -> str:
    print(f"🎧 Transcribing: {file_path}")
    result = model.transcribe(file_path)
    return result["text"]
