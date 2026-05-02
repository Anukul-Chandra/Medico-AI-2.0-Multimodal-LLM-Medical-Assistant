import os
from gtts import gTTS
from elevenlabs.client import ElevenLabs
from elevenlabs import save
import subprocess
import platform

# Step1 : Setup Text to Speech (TTS) - Google TTS.
def text_to_speech_withgTTS_old(text, output_filepath):
    audioobj = gTTS(text=text, lang='en', slow=False)
    audioobj.save(output_filepath)


input_text = "Hello, this is a Anukul Chandra."


# Step2 : Setup Text to Speech (TTS) - ElevenLabs
ELEVENLABS_API_KEY = os.environ.get("ELEVENLABS_API_KEY")

def text_to_speech_with_elevenlabs_old(input_text, output_filepath):
    client = ElevenLabs(api_key=ELEVENLABS_API_KEY)

    audio = client.text_to_speech.convert(
        voice_id="gO4tmn4tkX14KFrOZ6qq",
        model_id="eleven_turbo_v2",
        text=input_text
    )

    save(audio, output_filepath)   # ✅ FIXED


# Step3 : Use Models for Text Output to Voice
input_text = "Hello, this is a Anukul Chandra."

# text_to_speech_withgTTS_old(input_text, "gtts_testing.mp3")
# text_to_speech_with_elevenlabs_old(input_text, "elevenlabs_testing.mp3")


def text_to_speech_withgTTS(text, output_filepath):
    audioobj = gTTS(text=text, lang='en', slow=False)
    audioobj.save(output_filepath)

    os_name = platform.system()

    try:
        if os_name == "Darwin":  # macOS
            subprocess.run(['afplay', output_filepath])

        elif os_name == "Windows":  # ✅ FIXED (MP3 support)
            subprocess.run(['start', output_filepath], shell=True)

        elif os_name == "Linux":
            subprocess.run(['aplay', output_filepath])

        else:
            raise OSError("Unsupported operating system")

    except Exception as e:
        print(f"An error occurred while trying to play the audio: {e}")


input_text = "Hello, this is a Anukul Chandra. Autoplay Testing"


def text_to_speech_with_elevenlabs(input_text, output_filepath):
    client = ElevenLabs(api_key=ELEVENLABS_API_KEY)

    audio = client.text_to_speech.convert(
        voice_id="gO4tmn4tkX14KFrOZ6qq",
        model_id="eleven_turbo_v2",
        text=input_text
    )

    save(audio, output_filepath)   # ✅ FIXED

    os_name = platform.system()

    try:
        if os_name == "Darwin":
            subprocess.run(['afplay', output_filepath])

        elif os_name == "Windows":  # ✅ FIXED (MP3 support)
            subprocess.run(['start', output_filepath], shell=True)

        elif os_name == "Linux":
            subprocess.run(['aplay', output_filepath])

        else:
            raise OSError("Unsupported operating system")

    except Exception as e:
        print(f"An error occurred while trying to play the audio: {e}")


# 🔥 RUN (recommended)
#text_to_speech_withgTTS(input_text, "gtts_testing_autoplay.mp3")
#text_to_speech_with_elevenlabs(input_text, "elevenlabs_testing_autoplay.mp3")

# ⚠️ Only if ElevenLabs paid plan
# text_to_speech_with_elevenlabs(input_text, "elevenlabs_testing.mp3")