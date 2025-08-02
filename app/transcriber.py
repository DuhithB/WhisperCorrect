import os
import uuid
import whisper
import ffmpeg

# Load the Whisper model once
model = whisper.load_model("base")

def transcribe_audio(upload_file) -> str:
    # Save the uploaded file
    temp_dir = "temp_audio"
    os.makedirs(temp_dir, exist_ok=True)
    raw_path = os.path.join(temp_dir, f"{uuid.uuid4()}_{upload_file.filename}")

    with open(raw_path, "wb") as f:
        f.write(upload_file.file.read())

    # Convert to WAV if needed
    wav_path = raw_path.rsplit(".", 1)[0] + ".wav"
    try:
        ffmpeg.input(raw_path).output(wav_path).run(quiet=True, overwrite_output=True)
    except Exception as e:
        raise RuntimeError(f"FFmpeg conversion failed: {e}")

    # Transcribe using Whisper
    result = model.transcribe(wav_path)
    return result["text"]
