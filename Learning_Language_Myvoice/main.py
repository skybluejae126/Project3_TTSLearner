# main.py
from fastapi import FastAPI, HTTPException, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from starlette.responses import FileResponse, JSONResponse
import os
import shutil
import base64

from services.tts_service import generate_tts
from services.rvc_service import convert_voice_rvc
from services.similarity_service import calculate_similarity

# =======================================
# 디렉토리 설정
# =======================================
MODELS_DIR = "models"
VOX_OUTPUT_DIR = "VOX_output"
RVC_OUTPUT_DIR = "RVC_output"
USER_VOICE_DIR = "User_voice"
PLOTS_DIR = "plots"

os.makedirs(MODELS_DIR, exist_ok=True)
os.makedirs(VOX_OUTPUT_DIR, exist_ok=True)
os.makedirs(RVC_OUTPUT_DIR, exist_ok=True)
os.makedirs(USER_VOICE_DIR, exist_ok=True)
os.makedirs(PLOTS_DIR, exist_ok=True)


app = FastAPI(
    title="TTS Language Learner API",
    description="API for generating TTS audio, converting voice, and comparing pronunciation with visualization.",
    version="1.3.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# =======================================
# Helper Functions
# =======================================
def encode_image_to_base64(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')

# =======================================
# 요청 모델
# =======================================
class SynthesizeRequest(BaseModel):
    text: str
    speaker: int = 11
    speed: float = 1.0

class SynthesizeUserVoiceRequest(BaseModel):
    text: str
    model_name: str
    speaker: int = 11
    speed: float = 0.7

# =======================================
# API 엔드포인트
# =======================================
@app.post("/upload-voice-model")
async def upload_voice_model(file: UploadFile = File(...)):
    model_path = os.path.join(MODELS_DIR, file.filename)
    try:
        with open(model_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        return {"status": "success", "model_name": file.filename}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to upload model: {str(e)}")

@app.post("/synthesize-user-voice", response_class=FileResponse)
async def synthesize_user_voice(request: SynthesizeUserVoiceRequest):
    try:
        tts_output_path = os.path.join(VOX_OUTPUT_DIR, f"tts_output_{request.speaker}.wav")
        generate_tts(text=request.text, speaker=request.speaker, speed=request.speed, output_path=tts_output_path)

        rvc_output_filename = f"rvc_output_{os.path.splitext(request.model_name)[0]}.wav"
        rvc_output_path = os.path.join(RVC_OUTPUT_DIR, rvc_output_filename)
        model_path = os.path.join(MODELS_DIR, request.model_name)

        if not os.path.exists(model_path):
            raise HTTPException(status_code=404, detail=f"Model '{request.model_name}' not found.")

        convert_voice_rvc(input_wav=tts_output_path, output_wav=rvc_output_path, model_path=model_path)

        return FileResponse(rvc_output_path, media_type="audio/wav")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/compare-voice", response_class=JSONResponse)
async def compare_voice(reference_tts_id: str = Form(...), user_recording: UploadFile = File(...)):
    try:
        user_voice_filename = f"user_{user_recording.filename}"
        user_voice_path = os.path.join(USER_VOICE_DIR, user_voice_filename)
        with open(user_voice_path, "wb") as buffer:
            shutil.copyfileobj(user_recording.file, buffer)

        reference_filename = f"rvc_output_{os.path.splitext(reference_tts_id)[0]}.wav"
        reference_path = os.path.join(RVC_OUTPUT_DIR, reference_filename)

        if not os.path.exists(reference_path):
            raise HTTPException(status_code=404, detail=f"Reference TTS '{reference_tts_id}' not found.")

        score, waveform_path, spectrogram_path = calculate_similarity(reference_path, user_voice_path)

        waveform_b64 = encode_image_to_base64(waveform_path)
        spectrogram_b64 = encode_image_to_base64(spectrogram_path)

        return {
            "similarity_score": score,
            "waveform_plot": waveform_b64,
            "spectrogram_plot": spectrogram_b64
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/synthesize", response_class=FileResponse)
async def synthesize_speech(request: SynthesizeRequest):
    if request.speaker not in [1, 11]:
        raise HTTPException(status_code=400, detail="Invalid speaker ID. Allowed values are 1 (female) or 11 (male).")
    if not (0.5 <= request.speed <= 2.0):
        raise HTTPException(status_code=400, detail="Invalid speed value. Allowed range is 0.5 to 2.0.")
    try:
        output_path = os.path.join(VOX_OUTPUT_DIR, f"tts_output_{request.speaker}.wav")
        generate_tts(text=request.text, speaker=request.speaker, speed=request.speed, output_path=output_path)
        return FileResponse(output_path, media_type="audio/wav")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/")
def read_root():
    return {"message": "Welcome to the TTS Language Learner API. Go to /docs for API documentation."}
