#Step1: Setup Audio Recorder (ffmpeg & portaudio)

import logging
import speech_recognition as sr
from pydub import AudioSegment
from io import BytesIO

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s'  )

def record_audio(file_path, timeout =20,phrase_time_limit =None):
    """
   Simplified function to record audio from the microphone and save it as a MP3 file.
    Args:
        file_path (str): The path where the recorded audio will be saved.
        timeout (int): Maximum time to wait for a phrase to start (in seconds).
        phrase_time_limit (int): Maximum duration of a phrase (in seconds). If None, it will record until silence is detected.

    """

    recognizer = sr.Recognizer()
    try:
        with sr.Microphone() as source:
            logging.info("Adjusting for ambient noise...")
            recognizer.adjust_for_ambient_noise(source,duration=1)
            logging.info("Start speaking Now...")

            # Record  te Audio
            audio = recognizer.listen(source, timeout=timeout, phrase_time_limit=phrase_time_limit)
            logging.info("Recording complete, processing audio...")

            #convert the audio to MP3 format

            wav_data = audio.get_wav_data()
            audio_segment = AudioSegment.from_wav(BytesIO(wav_data))
            audio_segment.export(file_path, format="mp3",bitrate="128k")
            logging.info(f"Audio saved successfully at {file_path}")

    except Exception as e:
        logging.error(f"An error occurred while recording audio: {e}")


record_audio(file_path="pateient_audio.mp3")


#Step2 : Setup Speech to text-STT-model for transcraption


