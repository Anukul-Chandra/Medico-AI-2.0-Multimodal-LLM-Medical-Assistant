"""
Voice Input Module
===================

Handles:
- Audio recording from microphone (sounddevice)
- Speech-to-Text conversion using Groq Whisper

Dependencies: sounddevice, scipy, pydub, groq
"""

# Audio recording setup (sounddevice - no PyAudio needed)
import logging
import os

try:
    import sounddevice as sd
    from scipy.io.wavfile import write
    from pydub import AudioSegment
    import numpy as np
    AUDIO_AVAILABLE = True
except OSError:
    AUDIO_AVAILABLE = False
    sd = None
    write = None
    AudioSegment = None
    np = None

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def record_audio(file_path, timeout=20, phrase_time_limit=None, fs=44100):
    """
    Record audio using microphone and save as MP3.

    Args:
        file_path (str): Output file path
        timeout (int): max wait time (simulate start delay)
        phrase_time_limit (int): recording duration (seconds)
    """
    if not AUDIO_AVAILABLE:
        logging.warning("Audio recording not available. Please use text input instead.")
        return None

    try:
        logging.info("Adjusting for ambient noise...")
        logging.info("Start speaking now...")

        duration = phrase_time_limit if phrase_time_limit else 5

        recording = sd.rec(int(duration * fs), samplerate=fs, channels=1, dtype='int16')
        sd.wait()

        logging.info("Recording complete.")

        if np.max(np.abs(recording)) < 100:
            logging.warning("Microphone seems silent! Check your microphone.")
            return None

        temp_wav = "temp.wav"
        write(temp_wav, fs, recording)

        audio_segment = AudioSegment.from_wav(temp_wav)
        audio_segment.export(file_path, format="mp3", bitrate="128k")

        logging.info(f"Audio saved to {file_path}")

        return temp_wav

    except Exception as e:
        logging.error(f"An error occurred: {e}")
        return None


# Step2: Setup Speech to Text (STT) - Groq Whisper
from groq import Groq

GROQ_API_KEY = os.environ.get("GROQ_API_KEY")
stt_model = "whisper-large-v3"

def transcribe_with_groq(stt_model, audio_filepath, GROQ_API_KEY):
    client = Groq(api_key=GROQ_API_KEY)

    audio_file = open(audio_filepath, "rb")
    transcription = client.audio.transcriptions.create(
        model=stt_model,
        file=audio_file,
        language="en"
    )
    return transcription.text


# # RUN (commented - used by app.py)
# audio_filepath = "patient_voice_test_for_patient.mp3"

# # 👉 Now supports timeout + phrase_time_limit
# wav_file = record_audio(
#     file_path=audio_filepath,
#     timeout=20,
#     phrase_time_limit=5
# )

# if wav_file:
#     text = transcribe_with_groq(stt_model, audio_filepath, GROQ_API_KEY)
#     print("\n✅ Final Output:", text)
# else:
#     print("\n❌ Recording failed")