import os
import base64
import tempfile
from fastapi import FastAPI, UploadFile, File, Form
from fastapi.responses import JSONResponse, FileResponse
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

from brain import encode_img, analyze_image_with_query
from voice_input import record_audio, transcribe_with_groq
from voice_output import text_to_speech_withgTTS, text_to_speech_with_elevenlabs

app = FastAPI(title="Medico AI API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
ELEVENLABS_API_KEY = os.getenv("ELEVENLABS_API_KEY")

# ================================
# Models
# ================================
class ChatRequest(BaseModel):
    message: str
    history: list = []

class ImageAnalysisResponse(BaseModel):
    result: str

# ================================
# Health Check
# ================================
@app.get("/")
def root():
    return {"message": "Medico AI API is running!", "status": "healthy"}

@app.get("/health")
def health():
    return {"status": "ok", "api": "Medico AI"}

# ================================
# Image Analysis Endpoint
# ================================
@app.post("/analyze-image", response_model=ImageAnalysisResponse)
async def analyze_image_endpoint(file: UploadFile = File(...)):
    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".jpg") as tmp:
            content = await file.read()
            tmp.write(content)
            tmp.close()
            
            result = analyze_image_with_query(
                "meta-llama/llama-4-scout-17b-16e-instruct",
                "You are a medical expert. Analyze this image and give detailed diagnosis.",
                encode_img(tmp.name)
            )
            
            try:
                os.unlink(tmp.name)
            except:
                pass
            
            return {"result": result}
    except Exception as e:
        return JSONResponse({"error": str(e)}, status_code=500)

# ================================
# Voice STT Endpoint
# ================================
@app.post("/transcribe")
async def transcribe_endpoint(file: UploadFile = File(...)):
    try:
        import io
        from pydub import AudioSegment
        
        content = await file.read()
        
        # Convert to WAV first
        audio = AudioSegment.from_file(io.BytesIO(content))
        
        tmp_wav = tempfile.NamedTemporaryFile(delete=False, suffix=".wav")
        audio.export(tmp_wav.name, format="wav")
        
        text = transcribe_with_groq("whisper-large-v3", tmp_wav.name, GROQ_API_KEY)
        
        try:
            os.unlink(tmp_wav.name)
        except:
            pass
        
        return {"text": text or "No speech detected"}
    except Exception as e:
        return JSONResponse({"error": str(e)}, status_code=500)

# ================================
# Text-to-Speech Endpoint
# ================================
@app.post("/speak")
async def speak_endpoint(text: str = Form(...)):
    try:
        out = tempfile.NamedTemporaryFile(delete=False, suffix=".mp3")
        out.close()
        
        try:
            text_to_speech_with_elevenlabs(text, out.name)
        except:
            text_to_speech_withgTTS(text, out.name)
        
        return FileResponse(out.name, media_type="audio/mpeg", filename="response.mp3")
    except Exception as e:
        return JSONResponse({"error": str(e)}, status_code=500)

# ================================
# Chat Endpoint
# ================================
@app.post("/chat")
def chat_endpoint(request: ChatRequest):
    try:
        client = Groq(api_key=GROQ_API_KEY)
        
        messages = [
            {"role": "system", "content": "You are Medico, a professional medical AI assistant. Provide accurate medical information. Always recommend consulting a doctor."}
        ]
        
        for h in request.history:
            messages.append({"role": "user", "content": h[0]})
            messages.append({"role": "assistant", "content": h[1]})
        
        messages.append({"role": "user", "content": request.message})
        
        response = client.chat.completions.create(
            model="meta-llama/llama-4-scout-17b-16e-instruct",
            messages=messages,
            max_tokens=1024
        )
        
        return {"response": response.choices[0].message.content}
    except Exception as e:
        return JSONResponse({"error": str(e)}, status_code=500)

# ================================
# Record Voice (for client to call)
# ================================
@app.post("/record-voice")
def record_voice_endpoint():
    try:
        tmp = tempfile.NamedTemporaryFile(delete=False, suffix=".mp3")
        wav = record_audio(file_path=tmp.name, phrase_time_limit=5)
        
        if wav:
            text = transcribe_with_groq("whisper-large-v3", tmp.name, GROQ_API_KEY)
            return {"text": text or "No speech detected"}
        return {"error": "Recording failed"}
    except Exception as e:
        return JSONResponse({"error": str(e)}, status_code=500)

# ================================
# Run with: uvicorn main:app --reload
# ================================
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)