# Step1: Setup Audio Recorder (sounddevice - no PyAudio needed)
import logging
import sounddevice as sd
from scipy.io.wavfile import write
import speech_recognition as sr
from pydub import AudioSegment
from io import BytesIO
import numpy as np
import os

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def record_audio(file_path, timeout=20, phrase_time_limit=None, fs=44100):
    """
    Record audio using microphone and save as MP3.

    Args:
        file_path (str): Output file path
        timeout (int): max wait time (simulate start delay)
        phrase_time_limit (int): recording duration (seconds)
    """

    try:
        logging.info("Adjusting for ambient noise...")
        logging.info("Start speaking now...")

        # 🎯 duration logic (phrase_time_limit fallback)
        duration = phrase_time_limit if phrase_time_limit else 5

        recording = sd.rec(int(duration * fs), samplerate=fs, channels=1, dtype='int16')
        sd.wait()

        logging.info("Recording complete.")

        # 🔍 Silent check
        if np.max(np.abs(recording)) < 100:
            logging.warning("Microphone seems silent! Check your microphone.")
            return None

        # Save temp WAV
        temp_wav = "temp.wav"
        write(temp_wav, fs, recording)

        # Convert to MP3
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


# RUN
audio_filepath = "patient_voice_test_for_patient.mp3"

# 👉 Now supports timeout + phrase_time_limit
wav_file = record_audio(
    file_path=audio_filepath,
    timeout=20,
    phrase_time_limit=5
)

if wav_file:
    text = transcribe_with_groq(stt_model, audio_filepath, GROQ_API_KEY)
    print("\n✅ Final Output:", text)
else:
    print("\n❌ Recording failed")