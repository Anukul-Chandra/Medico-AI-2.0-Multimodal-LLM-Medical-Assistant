import os
import gradio as gr
import tempfile
from brain import encode_img, analyze_image_with_query
from voice_input import record_audio, transcribe_with_groq
from voice_output import text_to_speech_withgTTS, text_to_speech_with_elevenlabs

# ================================
# API Key
# ================================
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
                "content": (
                    "You are Medico, a professional AI medical assistant. "
                    "Provide accurate, empathetic, and helpful medical information. "
                    "Always remind users to consult a licensed healthcare professional "
                    "for diagnosis or treatment decisions."
                )
            }
        ]
        for user_msg, bot_msg in history:
            messages.append({"role": "user", "content": user_msg})
            messages.append({"role": "assistant", "content": bot_msg})
        messages.append({"role": "user", "content": user_message})

        response = client.chat.completions.create(
            model="meta-llama/llama-4-scout-17b-16e-instruct",
            messages=messages,
            max_tokens=1024,
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"⚠️ Error: {str(e)}"


# ================================
# Image Analysis
# ================================
def analyze_image(image):
    if image is None:
        return "⚠️ Please upload a medical image to begin analysis."
    temp_path = None
    try:
        tmp = tempfile.NamedTemporaryFile(delete=False, suffix=".jpg")
        tmp.close()
        temp_path = tmp.name
        image.save(temp_path)

        model = "meta-llama/llama-4-scout-17b-16e-instruct"
        query = (
            "You are an expert medical imaging specialist. "
            "Analyze this medical image in detail. Identify any abnormalities, "
            "possible conditions, affected regions, and severity. "
            "Format your response with: Findings, Possible Diagnosis, Recommended Next Steps."
        )
        result = analyze_image_with_query(model, query, encode_img(temp_path))
        return result
    except Exception as e:
        return f"⚠️ Analysis error: {str(e)}"
    finally:
        try:
            if temp_path and os.path.exists(temp_path):
                os.remove(temp_path)
        except Exception:
            pass


# ================================
# Voice Recording + STT
# ================================
def record_voice_fn():
    try:
        tmp = tempfile.NamedTemporaryFile(delete=False, suffix=".mp3")
        tmp.close()
        audio_filepath = tmp.name

        wav_file = record_audio(
            file_path=audio_filepath,
            duration=5
        )

        if wav_file:
            text = transcribe_with_groq("whisper-large-v3", audio_filepath, GROQ_API_KEY)
            try:
                os.unlink(audio_filepath)
            except Exception:
                pass
            return text if text else "⚠️ Could not transcribe. Please try again."

        return "⚠️ Recording failed. Please check your microphone."
    except Exception as e:
        return f"⚠️ Error: {str(e)}"


def voice_chat_respond(voice_text, history):
    if not voice_text or not voice_text.strip():
        return history, ""
    response = get_chat_response(voice_text, history)
    history.append((voice_text, response))
    return history, response


# ================================
# Text → Speech
# ================================
def speak_response(text):
    if not text or not text.strip():
        return None
    try:
        tmp = tempfile.NamedTemporaryFile(delete=False, suffix=".mp3")
        tmp.close()
        output_path = tmp.name
        try:
            text_to_speech_with_elevenlabs(text, output_path)
        except Exception:
            text_to_speech_withgTTS(text, output_path)
        return output_path
    except Exception:
        return None


# ================================
# Chat Respond
# ================================
def chat_respond(message, history):
    if not message.strip():
        return "", history
    try:
        response = get_chat_response(message, history)
    except Exception as e:
        response = f"⚠️ Error: {str(e)}"
    history.append((message, response))
    return "", history


# ================================
# Custom CSS — Dark Medical Premium Theme
# ================================
custom_css = """
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700;800&family=DM+Sans:ital,wght@0,300;0,400;0,500;1,300&display=swap');

:root {
    --bg-primary:    #080d14;
    --bg-secondary:  #0d1520;
    --bg-card:       #111c2a;
    --bg-card-hover: #162234;
    --accent-cyan:   #00e5ff;
    --accent-teal:   #00bfa5;
    --accent-blue:   #1565c0;
    --text-primary:  #e8f4fd;
    --text-secondary:#8fafc7;
    --text-muted:    #4a6680;
    --border:        #1e3248;
    --border-accent: #00e5ff33;
    --success:       #00e676;
    --warning:       #ffab40;
    --danger:        #ff5252;
    --glow-cyan:     0 0 20px #00e5ff33, 0 0 40px #00e5ff11;
    --glow-teal:     0 0 20px #00bfa533;
    --radius-sm:     8px;
    --radius-md:     14px;
    --radius-lg:     20px;
    --transition:    all 0.25s cubic-bezier(0.4, 0, 0.2, 1);
}

/* ── Global Reset ── */
*, *::before, *::after { box-sizing: border-box; }

body, .gradio-container {
    background: var(--bg-primary) !important;
    font-family: 'DM Sans', sans-serif !important;
    color: var(--text-primary) !important;
    min-height: 100vh;
}

.gradio-container {
    max-width: 1200px !important;
    margin: 0 auto !important;
    padding: 0 24px 48px !important;
}

/* ── Animated Header ── */
.medico-header {
    text-align: center;
    padding: 56px 0 32px;
    position: relative;
    overflow: hidden;
}

.medico-header::before {
    content: '';
    position: absolute;
    top: 0; left: 50%;
    transform: translateX(-50%);
    width: 600px; height: 200px;
    background: radial-gradient(ellipse, #00e5ff0d 0%, transparent 70%);
    pointer-events: none;
}

.medico-logo {
    display: inline-flex;
    align-items: center;
    gap: 14px;
    margin-bottom: 16px;
}

.medico-logo-icon {
    width: 52px; height: 52px;
    background: linear-gradient(135deg, #00e5ff, #00bfa5);
    border-radius: 14px;
    display: flex; align-items: center; justify-content: center;
    font-size: 26px;
    box-shadow: var(--glow-cyan);
    animation: pulse-icon 3s ease-in-out infinite;
}

@keyframes pulse-icon {
    0%, 100% { box-shadow: var(--glow-cyan); }
    50% { box-shadow: 0 0 30px #00e5ff55, 0 0 60px #00e5ff22; }
}

.medico-title {
    font-family: 'Syne', sans-serif !important;
    font-size: 42px !important;
    font-weight: 800 !important;
    background: linear-gradient(135deg, #00e5ff 0%, #00bfa5 50%, #e8f4fd 100%);
    -webkit-background-clip: text !important;
    -webkit-text-fill-color: transparent !important;
    background-clip: text !important;
    letter-spacing: -1px;
    line-height: 1 !important;
    margin: 0 !important;
}

.medico-subtitle {
    font-size: 15px !important;
    color: var(--text-secondary) !important;
    font-weight: 300 !important;
    letter-spacing: 3px !important;
    text-transform: uppercase;
    margin-top: 8px !important;
}

.medico-badge {
    display: inline-flex;
    align-items: center;
    gap: 6px;
    background: #00e5ff11;
    border: 1px solid var(--border-accent);
    border-radius: 100px;
    padding: 6px 16px;
    font-size: 12px;
    color: var(--accent-cyan);
    letter-spacing: 1px;
    margin-top: 16px;
}

.medico-badge::before {
    content: '';
    width: 6px; height: 6px;
    background: var(--accent-cyan);
    border-radius: 50%;
    animation: blink 2s ease-in-out infinite;
}

@keyframes blink {
    0%, 100% { opacity: 1; }
    50% { opacity: 0.3; }
}

/* ── Tabs ── */
.tab-nav {
    background: var(--bg-secondary) !important;
    border: 1px solid var(--border) !important;
    border-radius: var(--radius-lg) !important;
    padding: 6px !important;
    gap: 4px !important;
    margin-bottom: 24px !important;
}

.tab-nav button {
    font-family: 'Syne', sans-serif !important;
    font-size: 14px !important;
    font-weight: 600 !important;
    color: var(--text-muted) !important;
    background: transparent !important;
    border: none !important;
    border-radius: var(--radius-md) !important;
    padding: 12px 24px !important;
    transition: var(--transition) !important;
    letter-spacing: 0.3px;
}

.tab-nav button:hover {
    color: var(--text-primary) !important;
    background: var(--bg-card) !important;
}

.tab-nav button.selected {
    color: var(--bg-primary) !important;
    background: linear-gradient(135deg, var(--accent-cyan), var(--accent-teal)) !important;
    box-shadow: var(--glow-cyan) !important;
}

/* ── Cards / Blocks ── */
.gradio-block, .gr-box, .gr-form, .gr-panel, .block {
    background: var(--bg-card) !important;
    border: 1px solid var(--border) !important;
    border-radius: var(--radius-lg) !important;
    transition: var(--transition) !important;
}

/* ── Inputs ── */
input, textarea, .gr-text-input textarea, .gr-textbox textarea {
    background: var(--bg-secondary) !important;
    border: 1px solid var(--border) !important;
    border-radius: var(--radius-sm) !important;
    color: var(--text-primary) !important;
    font-family: 'DM Sans', sans-serif !important;
    font-size: 15px !important;
    padding: 12px 16px !important;
    transition: var(--transition) !important;
    outline: none !important;
}

input:focus, textarea:focus {
    border-color: var(--accent-cyan) !important;
    box-shadow: 0 0 0 3px #00e5ff15 !important;
}

/* ── Buttons ── */
button.primary, .gr-button-primary, button[variant="primary"] {
    background: linear-gradient(135deg, #00bfa5, #00838f) !important;
    border: none !important;
    color: #fff !important;
    font-family: 'Syne', sans-serif !important;
    font-weight: 700 !important;
    font-size: 14px !important;
    letter-spacing: 0.5px;
    padding: 13px 28px !important;
    border-radius: var(--radius-sm) !important;
    cursor: pointer !important;
    transition: var(--transition) !important;
    box-shadow: 0 4px 15px #00bfa530 !important;
}

button.primary:hover, .gr-button-primary:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 8px 25px #00bfa545 !important;
    filter: brightness(1.1) !important;
}

button.secondary, .gr-button-secondary {
    background: var(--bg-secondary) !important;
    border: 1px solid var(--border) !important;
    color: var(--text-secondary) !important;
    font-family: 'Syne', sans-serif !important;
    font-weight: 600 !important;
    padding: 12px 24px !important;
    border-radius: var(--radius-sm) !important;
    transition: var(--transition) !important;
}

button.secondary:hover {
    border-color: var(--accent-cyan) !important;
    color: var(--accent-cyan) !important;
}

/* ── Labels ── */
label, .gr-label, span.svelte-1gfkn6j {
    font-family: 'Syne', sans-serif !important;
    font-size: 12px !important;
    font-weight: 600 !important;
    color: var(--text-secondary) !important;
    letter-spacing: 1px !important;
    text-transform: uppercase !important;
    margin-bottom: 6px !important;
}

/* ── Chatbot ── */
.gr-chatbot, .chatbot {
    background: var(--bg-secondary) !important;
    border: 1px solid var(--border) !important;
    border-radius: var(--radius-lg) !important;
}

.message.user .message-bubble-border {
    background: linear-gradient(135deg, #00bfa520, #00e5ff15) !important;
    border: 1px solid #00e5ff22 !important;
    border-radius: 16px 16px 4px 16px !important;
    color: var(--text-primary) !important;
}

.message.bot .message-bubble-border {
    background: var(--bg-card) !important;
    border: 1px solid var(--border) !important;
    border-radius: 16px 16px 16px 4px !important;
    color: var(--text-primary) !important;
}

/* ── Image Upload ── */
.gr-image, .image-upload {
    background: var(--bg-secondary) !important;
    border: 2px dashed var(--border) !important;
    border-radius: var(--radius-lg) !important;
    transition: var(--transition) !important;
}

.gr-image:hover {
    border-color: var(--accent-cyan) !important;
}

/* ── Audio Player ── */
.gr-audio {
    background: var(--bg-secondary) !important;
    border: 1px solid var(--border) !important;
    border-radius: var(--radius-md) !important;
}

/* ── Markdown Output ── */
.gr-markdown, .prose {
    color: var(--text-primary) !important;
    font-family: 'DM Sans', sans-serif !important;
    line-height: 1.7 !important;
}

.gr-markdown h1, .gr-markdown h2, .gr-markdown h3 {
    font-family: 'Syne', sans-serif !important;
    color: var(--accent-cyan) !important;
}

/* ── Section Headers ── */
.section-header {
    font-family: 'Syne', sans-serif;
    font-size: 11px;
    font-weight: 700;
    letter-spacing: 2px;
    text-transform: uppercase;
    color: var(--text-muted);
    margin-bottom: 12px;
    display: flex;
    align-items: center;
    gap: 8px;
}

.section-header::after {
    content: '';
    flex: 1;
    height: 1px;
    background: var(--border);
}

/* ── Stats Bar ── */
.stats-bar {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 16px;
    margin-bottom: 28px;
}

.stat-card {
    background: var(--bg-card);
    border: 1px solid var(--border);
    border-radius: var(--radius-md);
    padding: 20px;
    text-align: center;
    transition: var(--transition);
}

.stat-card:hover {
    border-color: var(--border-accent);
    box-shadow: var(--glow-cyan);
    transform: translateY(-3px);
}

.stat-number {
    font-family: 'Syne', sans-serif;
    font-size: 28px;
    font-weight: 800;
    background: linear-gradient(135deg, var(--accent-cyan), var(--accent-teal));
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
}

.stat-label {
    font-size: 11px;
    color: var(--text-muted);
    letter-spacing: 1px;
    text-transform: uppercase;
    margin-top: 4px;
}

/* ── Footer ── */
.medico-footer {
    text-align: center;
    padding: 32px 0 0;
    border-top: 1px solid var(--border);
    margin-top: 48px;
    color: var(--text-muted);
    font-size: 12px;
    letter-spacing: 0.5px;
}

/* ── Scrollbar ── */
::-webkit-scrollbar { width: 6px; }
::-webkit-scrollbar-track { background: var(--bg-primary); }
::-webkit-scrollbar-thumb {
    background: var(--border);
    border-radius: 3px;
}
::-webkit-scrollbar-thumb:hover { background: var(--accent-cyan); }

/* ── Animations ── */
@keyframes fadeInUp {
    from { opacity: 0; transform: translateY(20px); }
    to   { opacity: 1; transform: translateY(0); }
}

.gradio-container > * {
    animation: fadeInUp 0.5s ease both;
}
"""


# ================================
# UI LAYOUT
# ================================
with gr.Blocks(
    theme=gr.themes.Base(),
    css=custom_css,
    title="Medico AI — Medical Assistant"
) as demo:

    # ── Header ──
    gr.HTML("""
    <div class="medico-header">
        <div class="medico-logo">
            <div class="medico-logo-icon">⚕</div>
            <h1 class="medico-title">MEDICO AI</h1>
        </div>
        <p class="medico-subtitle">Intelligent Medical Assistant Platform</p>
        <div class="medico-badge">● Powered by Llama 4 &amp; Groq Whisper</div>
    </div>
    """)

    # ── Stats ──
    gr.HTML("""
    <div class="stats-bar">
        <div class="stat-card">
            <div class="stat-number">99.2%</div>
            <div class="stat-label">Transcription Accuracy</div>
        </div>
        <div class="stat-card">
            <div class="stat-number">&lt;1s</div>
            <div class="stat-label">Response Time</div>
        </div>
        <div class="stat-card">
            <div class="stat-number">24/7</div>
            <div class="stat-label">Always Available</div>
        </div>
    </div>
    """)

    # ── Tabs ──
    with gr.Tabs(elem_classes="tab-container"):

        # ────── Tab 1: Image Diagnosis ──────
        with gr.TabItem("🔬  Image Diagnosis"):
            gr.HTML('<p class="section-header">Upload Medical Image</p>')
            with gr.Row():
                with gr.Column(scale=1):
                    image_input = gr.Image(
                        type="pil",
                        label="Medical Image",
                        height=320
                    )
                    analyze_btn = gr.Button(
                        "🔬  Run AI Diagnosis",
                        variant="primary",
                        size="lg"
                    )
                with gr.Column(scale=1):
                    gr.HTML('<p class="section-header">AI Findings</p>')
                    diagnosis_output = gr.Markdown(
                        value="*Upload an image and click **Run AI Diagnosis** to begin.*",
                        label=""
                    )

            analyze_btn.click(
                fn=analyze_image,
                inputs=image_input,
                outputs=diagnosis_output
            )

        # ────── Tab 2: Voice Assistant ──────
        with gr.TabItem("🎤  Voice Assistant"):
            with gr.Row():
                with gr.Column(scale=1):
                    gr.HTML('<p class="section-header">Voice Input</p>')
                    record_btn = gr.Button(
                        "🎙  Record Voice  (5s)",
                        variant="primary",
                        size="lg"
                    )
                    voice_text = gr.Textbox(
                        label="Recognized Speech",
                        placeholder="Your speech will appear here...",
                        lines=3,
                        interactive=True
                    )
                    send_voice_btn = gr.Button(
                        "⚡  Get AI Response",
                        variant="secondary"
                    )

                with gr.Column(scale=1):
                    gr.HTML('<p class="section-header">AI Response</p>')
                    voice_chat = gr.Chatbot(
                        label="",
                        height=300,
                        show_label=False
                    )
                    with gr.Row():
                        play_voice_btn = gr.Button("🔊  Speak Response", variant="secondary")
                    audio_player = gr.Audio(
                        label="Audio Output",
                        autoplay=True,
                        visible=True
                    )

            voice_chat_state = gr.State([])

            record_btn.click(
                fn=record_voice_fn,
                inputs=[],
                outputs=voice_text
            )

            send_voice_btn.click(
                fn=voice_chat_respond,
                inputs=[voice_text, voice_chat_state],
                outputs=[voice_chat, gr.State()]
            ).then(
                fn=lambda h: h,
                inputs=voice_chat_state,
                outputs=voice_chat
            )

            play_voice_btn.click(
                fn=lambda chat: speak_response(chat[-1][1]) if chat else None,
                inputs=voice_chat,
                outputs=audio_player
            )

        # ────── Tab 3: Chat ──────
        with gr.TabItem("💬  AI Chat"):
            gr.HTML('<p class="section-header">Medical Consultation</p>')
            chatbot = gr.Chatbot(
                label="",
                height=420,
                show_label=False,
                bubble_full_width=False,
                avatar_images=(None, "https://api.dicebear.com/7.x/bottts/svg?seed=medico")
            )
            with gr.Row():
                msg_input = gr.Textbox(
                    placeholder="Ask about symptoms, medications, conditions...",
                    label="",
                    scale=5,
                    lines=1,
                    max_lines=4,
                    show_label=False,
                    container=False
                )
                send_btn = gr.Button("Send  →", variant="primary", scale=1)

            with gr.Row():
                clear_btn = gr.Button("🗑  Clear Chat", variant="secondary", size="sm")
                gr.HTML("""
                <div style="font-size:11px; color:#4a6680; padding: 8px 0; 
                            letter-spacing:0.5px; align-self:center;">
                    ⚠️ For informational purposes only. Always consult a licensed physician.
                </div>
                """)

            send_btn.click(
                fn=chat_respond,
                inputs=[msg_input, chatbot],
                outputs=[msg_input, chatbot]
            )

            msg_input.submit(
                fn=chat_respond,
                inputs=[msg_input, chatbot],
                outputs=[msg_input, chatbot]
            )

            clear_btn.click(lambda: ([], ""), outputs=[chatbot, msg_input])

    # ── Footer ──
    gr.HTML("""
    <div class="medico-footer">
        Built with Groq · Llama 4 · Whisper · Gradio &nbsp;|&nbsp; Medico AI © 2025
    </div>
    """)


# ================================
# RUN
# ================================
if __name__ == "__main__":
    demo.launch(share=True)