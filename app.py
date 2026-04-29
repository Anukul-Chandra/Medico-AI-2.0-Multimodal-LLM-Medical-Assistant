# Step 1: Setup Gradio Interface
import os
import gradio as gr
from brain import encode_img, analyze_image_with_query
from voice_input import record_audio, transcribe_with_groq
from voice_output import text_to_speech_withgTTS, text_to_speech_with_elevenlabs
import tempfile

# API Key
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

if not GROQ_API_KEY:
    raise ValueError("❌ GROQ_API_KEY not found in environment variables")


# ================================
# Chat Response
# ================================
def get_chat_response(user_message, history):
    from groq import Groq
    client = Groq(api_key=GROQ_API_KEY)

    try:
        messages = [
            {
                "role": "system",
                "content": "You are a professional medical AI assistant. Provide helpful and accurate medical information. Always recommend consulting a healthcare professional."
            }
        ]

        for msg in history:
            messages.append({"role": "user", "content": msg[0]})
            messages.append({"role": "assistant", "content": msg[1]})

        messages.append({"role": "user", "content": user_message})

        response = client.chat.completions.create(
            model="meta-llama/llama-4-scout-17b-16e-instruct",
            messages=messages,
            max_tokens=1024,
        )

        return response.choices[0].message.content

    except Exception as e:
        return f"Error: {str(e)}"


# ================================
# Image Analysis
# ================================
def analyze_image(image):
    if image is None:
        return "Please upload a medical image for analysis."

    temp_path = None

    try:
        temp_path = tempfile.NamedTemporaryFile(delete=False, suffix=".jpg")
        temp_path.close()   # 🔥 FIX

        image.save(temp_path.name)

        model = "meta-llama/llama-4-scout-17b-16e-instruct"
        query = "Analyze this medical image and provide diagnosis."

        result = analyze_image_with_query(
            model,
            query,
            encode_img(temp_path.name)
        )

        return result

    except Exception as e:
        return f"Error: {str(e)}"

    finally:
        try:
            if temp_path and os.path.exists(temp_path.name):
                os.remove(temp_path.name)
        except:
            pass

# ================================
# Voice Recording + STT
# ================================
def record_voice_fn():
    try:
        audio_filepath = tempfile.NamedTemporaryFile(delete=False, suffix=".mp3").name

        wav_file = record_audio(
            file_path=audio_filepath,
            timeout=20,
            phrase_time_limit=5
        )

        if wav_file:
            text = transcribe_with_groq(
                "whisper-large-v3",
                audio_filepath,
                GROQ_API_KEY
            )

            if os.path.exists(audio_filepath):
                os.unlink(audio_filepath)

            return text

        return "Recording failed. Please try again."

    except Exception as e:
        return f"Error: {str(e)}"


# ================================
# Text → Speech
# ================================
def speak_response(text):
    if not text or not text.strip():
        return None

    try:
        output_path = tempfile.NamedTemporaryFile(delete=False, suffix=".mp3").name

        # Try ElevenLabs first
        try:
            text_to_speech_with_elevenlabs(text, output_path)
        except Exception:
            # fallback to gTTS
            text_to_speech_withgTTS(text, output_path)

        return output_path

    except Exception:
        return None


# ================================
# UI DESIGN
# ================================
with gr.Blocks(theme=gr.themes.Soft()) as demo:

    gr.Markdown("# 🏥 Medico AI")
    gr.Markdown("### AI-powered Medical Assistant")

    with gr.Tabs():

        # -------- Image Diagnosis --------
        with gr.TabItem("🔬 Image Diagnosis"):
            image_input = gr.Image(type="pil")
            analyze_btn = gr.Button("Analyze Image")
            diagnosis_output = gr.Markdown()

            analyze_btn.click(
                fn=analyze_image,
                inputs=image_input,
                outputs=diagnosis_output
            )

        # -------- Voice Assistant --------
        with gr.TabItem("🎤 Voice Assistant"):
            record_btn = gr.Button("🎤 Record Voice (5s)")
            voice_text = gr.Textbox(label="Your Speech")

            voice_output = gr.Textbox(label="AI Response")
            play_voice_btn = gr.Button("🔊 Play Response")
            audio_player = gr.Audio()

            record_btn.click(
                fn=record_voice_fn,
                inputs=[],
                outputs=voice_text
            )

            play_voice_btn.click(
                fn=speak_response,
                inputs=voice_output,
                outputs=audio_player
            )

        # -------- Chat --------
        with gr.TabItem("💬 Chat"):
            chatbot = gr.Chatbot()
            msg_input = gr.Textbox()
            send_btn = gr.Button("Send")

            def respond(message, history):
                if not message.strip():
                    return "", history

                try:
                    response = get_chat_response(message, history)
                except Exception as e:
                    response = f"Error: {str(e)}"

                history.append((message, response))
                return "", history

            send_btn.click(
                fn=respond,
                inputs=[msg_input, chatbot],
                outputs=[msg_input, chatbot]
            )


# ================================
# RUN
# ================================
if __name__ == "__main__":
    demo.launch(share=True)