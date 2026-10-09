import os
import asyncio
import urllib.parse
import requests
import streamlit as st
from PIL import Image
from google import genai
from google.genai import types
from telegram import Bot

# ==========================================
# SYSTEM PROMPT DEFINITION
# ==========================================
SYSTEM_PROMPT = """You are Snap & Study, an expert AI tutor for students.
Your goal is to break down difficult concepts, homework problems, diagrams, or handwritten study notes from images into simple, plain language.

Structure your response clearly using the following sections:

1. 📌 **Core Concept**: Explain the main idea or topic shown in the image in 2–3 simple, conversational sentences.
2. 🔍 **Step-by-Step Breakdown**: Walk through the problem, equation, or diagram logically. Use bullet points or numbered lists. Explain the 'why' behind each step, not just the answer.
3. 💡 **Key Takeaway**: Highlight 1–2 crucial rules, formulas, or concepts the student should remember for exams.

Tone: Friendly, encouraging, precise, and easy to understand. Avoid unnecessary jargon.
"""

USER_PROMPT = "Please analyze this image, identify the problem or notes, and explain it clearly following your system instructions."

# ==========================================
# STREAMLIT CONFIG & INITIALIZATION
# ==========================================
st.set_page_config(
    page_title="Snap & Study",
    page_icon="📚",
    layout="centered"
)

@st.cache_resource
def get_gemini_client():
    api_key = st.secrets.get("GEMINI_API_KEY") or os.getenv("GEMINI_API_KEY")
    if not api_key:
        st.error("API Key missing! Add `GEMINI_API_KEY` to `.streamlit/secrets.toml` or your environment variables.")
        st.stop()
    return genai.Client(api_key=api_key)

client = get_gemini_client()

def send_telegram_message(chat_id: str, text: str) -> bool:
    """Send message via Telegram Bot API."""
    bot_token = st.secrets.get("TELEGRAM_BOT_TOKEN")
    if not bot_token:
        return False
    try:
        bot = Bot(token=bot_token)
        asyncio.run(bot.send_message(chat_id=chat_id, text=text))
        return True
    except Exception as e:
        st.error(f"Telegram Error: {e}")
        return False

def send_email_via_mailgun(to_email: str, text_content: str) -> bool:
    """Send summary via Mailgun API."""
    api_key = st.secrets.get("MAILGUN_API_KEY")
    domain = st.secrets.get("MAILGUN_DOMAIN")
    sender = st.secrets.get("SENDER_EMAIL", f"Snap & Study <mailgun@{domain}>")
    
    if not api_key or not domain:
        return False

    try:
        response = requests.post(
            f"https://api.mailgun.net/v3/{domain}/messages",
            auth=("api", api_key),
            data={
                "from": sender,
                "to": [to_email],
                "subject": "📚 Your Snap & Study Explanation",
                "text": text_content,
            },
            timeout=10
        )
        return response.status_code == 200
    except Exception:
        return False

# ==========================================
# USER INTERFACE
# ==========================================
st.title("📚 Snap & Study")
st.write("Upload a photo of a problem, diagram, or handwritten notes to get a clear, step-by-step breakdown.")

uploaded_file = st.file_uploader("Upload an image or take a photo", type=["png", "jpg", "jpeg", "webp"])

if uploaded_file:
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Image", use_container_width=True)

    if st.button("🔍 Analyze & Explain", type="primary"):
        with st.spinner("Analyzing image with Gemini..."):
            try:
                response = client.models.generate_content(
                    model="gemini-3.5-flash",
                    contents=[image, USER_PROMPT],
                    config=types.GenerateContentConfig(
                        system_instruction=SYSTEM_PROMPT,
                        temperature=0.2
                    )
                )
                st.session_state["explanation"] = response.text
            except Exception as e:
                st.error(f"Error generating response: {e}")

# Display Explanation & Export Options
if "explanation" in st.session_state:
    st.markdown("---")
    st.subheader("💡 Simple Explanation")
    st.markdown(st.session_state["explanation"])

    st.markdown("---")
    st.subheader("📲 Save & Share")

    explanation_text = st.session_state["explanation"]
    tab_tg, tab_email = st.tabs(["Telegram Bot", "Email"])

    with tab_tg:
      st.write("Send explanation directly to your Telegram chat using your bot:")
      chat_id_input = st.text_input("Telegram Chat ID", placeholder="e.g. 123456789")
    
      st.caption("ℹ️ **First time?** Search for your bot in Telegram, press **Start**, and get your Chat ID from `@userinfobot`.")

      if st.button("✈️ Send via Telegram Bot"):
        if chat_id_input:
            if "TELEGRAM_BOT_TOKEN" in st.secrets:
                try:
                    bot = Bot(token=st.secrets["TELEGRAM_BOT_TOKEN"])
                    asyncio.run(bot.send_message(chat_id=chat_id_input.strip(), text=f"📚 Snap & Study Explanation:\n\n{explanation_text}"))
                    st.success("Message sent successfully via Telegram Bot!")
                except Exception as e:
                    if "Chat not found" in str(e):
                        st.error("❌ Chat not found. Please open your Telegram app, search for your bot, press **Start**, and double-check your Chat ID.")
                    else:
                        st.error(f"Telegram Error: {e}")
            else:
                st.error("`TELEGRAM_BOT_TOKEN` not found in Streamlit secrets.")
        else:
            st.warning("Please enter your Telegram Chat ID.")