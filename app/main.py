import os
from fastapi import FastAPI, File, UploadFile
from fastapi.responses import JSONResponse
from pydub import AudioSegment
import speech_recognition as sr
from dotenv import load_dotenv
import google.generativeai as genai

# Load environment variables
load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Use the correct model name
model = genai.GenerativeModel("models/gemini-1.5-flash-latest")

app = FastAPI()

@app.post("/correct-audio/")
async def correct_audio(file: UploadFile = File(...)):
    try:
        # Save the uploaded file
        file_path = f"temp_{file.filename}"
        with open(file_path, "wb") as f:
            f.write(await file.read())

        # Convert to wav if not already
        audio = AudioSegment.from_file(file_path)
        wav_path = file_path.rsplit(".", 1)[0] + ".wav"
        audio.export(wav_path, format="wav")

        # Transcribe the audio
        recognizer = sr.Recognizer()
        with sr.AudioFile(wav_path) as source:
            audio_data = recognizer.record(source)
            original_text = recognizer.recognize_google(audio_data)

        # Correct the grammar using Gemini
        prompt = f"Correct the grammar of this sentence: \"{original_text}\""
        response = model.generate_content(prompt)
        corrected_text = response.text.strip()

        # Clean up temp files
        os.remove(file_path)
        os.remove(wav_path)

        return {
            "original_text": original_text,
            "corrected_text": corrected_text
        }

    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"error": str(e)}
        )
