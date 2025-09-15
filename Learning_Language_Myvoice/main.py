# main.py
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from starlette.responses import StreamingResponse
import io

from services.tts_service import generate_tts

app = FastAPI(
    title="TTS Language Learner API",
    description="API for generating TTS audio using Voicevox.",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

class SynthesizeRequest(BaseModel):
    text: str
    speaker: int = 11
    speed: float = 0.7

@app.post("/synthesize", response_class=StreamingResponse)
async def synthesize_speech(request: SynthesizeRequest):
    """
    Synthesizes speech from text and returns the audio as a WAV file stream.
    """
    try:
        audio_data = generate_tts(
            text=request.text,
            speaker=request.speaker,
            speed=request.speed
        )
        
        # Return the audio data as a streaming response
        return StreamingResponse(io.BytesIO(audio_data), media_type="audio/wav")

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/")
def read_root():
    return {"message": "Welcome to the TTS Language Learner API. Go to /docs for API documentation."}

# To run this app:
# uvicorn main:app --reload
