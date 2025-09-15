# services/tts_service.py
import requests
from config import VOICEVOX_API_URL

def generate_tts(text: str, speaker: int = 11, speed: float = 0.7) -> bytes:
    """
    Generates TTS audio using the Voicevox engine.

    Args:
        text (str): The text to synthesize.
        speaker (int, optional): The speaker ID. Defaults to 11.
        speed (float, optional): The speech speed. Defaults to 0.7.

    Returns:
        bytes: The raw WAV audio data.
    """
    params = {"text": text, "speaker": speaker}
    res1 = requests.post(f"{VOICEVOX_API_URL}/audio_query", params=params)
    res1.raise_for_status()
    
    audio_query = res1.json()
    audio_query["speedScale"] = speed

    res2 = requests.post(
        f"{VOICEVOX_API_URL}/synthesis",
        params={"speaker": speaker},
        json=audio_query
    )
    res2.raise_for_status()
    
    return res2.content
