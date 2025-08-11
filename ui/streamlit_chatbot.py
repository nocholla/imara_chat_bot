import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import streamlit as st
import pandas as pd
import logging
import requests
from streamlit_js_eval import streamlit_js_eval
from src.config import load_config
from src.faq_loader import load_faqs

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Load configuration
config = load_config()
data_dir = config.get('data_dir', 'data')
backend_url = config.get('backend_url', 'http://localhost:8000')

# Load FAQs dynamically from Firestore
FAQ_RESPONSES = load_faqs()

# Initialize session state
if "setup_complete" not in st.session_state:
    st.session_state.setup_complete = False
if "user_message_count" not in st.session_state:
    st.session_state.user_message_count = 0
if "feedback_shown" not in st.session_state:
    st.session_state.feedback_shown = False
if "chat_complete" not in st.session_state:
    st.session_state.chat_complete = False
if "messages" not in st.session_state:
    st.session_state.messages = []
if "profile" not in st.session_state:
    st.session_state.profile = {
        "firstName": "",
        "language": "en",
        "aboutMe": "",
        "current_state": "Initial"
    }
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Helper functions
def complete_setup():
    st.session_state.setup_complete = True
    save_chat_history()

def show_feedback():
    st.session_state.feedback_shown = True
    save_chat_history()

def save_chat_history():
    try:
        chat_data = {
            "userId": st.session_state.profile.get("userId", "anonymous"),
            "timestamp": pd.Timestamp.now(),
            "messages": st.session_state.messages,
            "language": st.session_state.profile["language"]
        }
        st.session_state.chat_history.append(chat_data)
        chat_df = pd.DataFrame(st.session_state.chat_history)
        chat_df.to_csv(os.path.join(data_dir, "chat_history.csv"), index=False)
        logger.info("Chat history saved successfully")
    except Exception as e:
        logger.error(f"Error saving chat history: {e}")

# Setup phase
if not st.session_state.setup_complete:
    st.set_page_config(page_title="Africa Love Match FAQ Chatbot", page_icon="💖")
    st.title("💬 Imara Chat Bot")

    st.subheader("Profile Information")
    st.session_state.profile["firstName"] = st.text_input(
        label="First Name",
        value=st.session_state.profile["firstName"],
        placeholder="Enter your first name",
        max_chars=40
    )
    st.session_state.profile["language"] = st.selectbox(
        "Select Language",
        options=["English", "Arabic", "German", "Spanish", "French", "Italian", "Dutch", "Portuguese"],
        index=0
    )
    st.session_state.profile["aboutMe"] = st.text_area(
        label="About Me",
        value=st.session_state.profile["aboutMe"],
        placeholder="Tell us about yourself (e.g., hobbies, interests)",
        max_chars=200
    )

    if st.button("Start Chatting"):
        st.session_state.profile["userId"] = f"user_{pd.Timestamp.now().strftime('%Y%m%d%H%M%S')}"
        complete_setup()
        st.rerun()

# Chat phase
if st.session_state.setup_complete and not st.session_state.feedback_shown:
    st.set_page_config(page_title="Africa Love Match FAQ Chatbot", page_icon="💖")
    st.title("IMARA: Africa Love Match FAQ Chatbot")

    # Soccer enthusiast check
    soccer_keywords = ["soccer", "football"]
    is_soccer_enthusiast = any(keyword in st.session_state.profile["aboutMe"].lower() for keyword in soccer_keywords)
    if is_soccer_enthusiast:
        st.info("Hey, a soccer fan! ⚽ Ready to connect with fellow Africa Soccer Kings enthusiasts? Ask IMARA anything! 😊")
    else:
        st.info("Welcome to Africa Love Match! 😊 Ask IMARA about subscriptions, profiles, or anything else!")

    # Language map
    language_map = {
        "English": "en", "Arabic": "ar", "German": "de", "Spanish": "es",
        "French": "fr", "Italian": "it", "Dutch": "nl", "Portuguese": "pt"
    }
    lang_code = language_map.get(st.session_state.profile["language"], "en")

    # Initial message if not set
    if not st.session_state.messages:
        initial_message = FAQ_RESPONSES.get("Initial", {}).get("messages", {}).get(lang_code, "Hello! How can I help?")
        if is_soccer_enthusiast:
            initial_message += f" Loving the soccer vibe, {st.session_state.profile['firstName']}! ⚽ Ready to connect with Africa Soccer Kings fans?"
        st.session_state.messages.append({"role": "assistant", "content": initial_message})

    # Display messages
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Display options
    current_state = st.session_state.profile["current_state"]
    if current_state in FAQ_RESPONSES and "options" in FAQ_RESPONSES[current_state]:
        st.subheader("Quick Options")
        cols = st.columns(3)
        for idx, option in enumerate(FAQ_RESPONSES[current_state]["options"]):
            with cols[idx % 3]:
                if st.button(option["text"].get(lang_code, option["text"]["en"])):
                    next_state = option["nextState"]
                    st.session_state.profile["current_state"] = next_state
                    response = FAQ_RESPONSES.get(next_state, {}).get("messages", {}).get(lang_code, "Sorry, no response available.")
                    if is_soccer_enthusiast and any(kw in response.lower() for kw in soccer_keywords):
                        response += " By the way, loving your soccer passion! ⚽"
                    st.session_state.messages.append({"role": "user", "content": option["text"][lang_code]})
                    st.session_state.messages.append({"role": "assistant", "content": response})
                    st.session_state.user_message_count += 1
                    st.rerun()

    # User input
    if st.session_state.user_message_count < 5:
        prompt = st.chat_input("Your question or message", max_chars=1000)
        if prompt:
            st.session_state.messages.append({"role": "user", "content": prompt})
            with st.chat_message("user"):
                st.markdown(prompt)

            with st.chat_message("assistant"):
                try:
                    response = requests.post(
                        f"{backend_url}/generate",
                        json={
                            "query": prompt,
                            "lang_code": lang_code,
                            "is_soccer_enthusiast": is_soccer_enthusiast,
                            "name": st.session_state.profile["firstName"]
                        },
                        timeout=30
                    )
                    response.raise_for_status()
                    answer = response.json()["response"]
                    st.markdown(answer)
                    st.session_state.messages.append({"role": "assistant", "content": answer})
                except requests.exceptions.RequestException as e:
                    logger.error(f"Error calling backend: {e}")
                    st.error("Sorry, something went wrong. Please try again!")
                    st.session_state.messages.append({"role": "assistant", "content": "Sorry, something went wrong. Please try again! 😊"})

            st.session_state.user_message_count += 1
            save_chat_history()
            st.rerun()

    if st.session_state.user_message_count >= 5:
        st.session_state.chat_complete = True
        save_chat_history()

# Feedback phase
if st.session_state.chat_complete and not st.session_state.feedback_shown:
    if st.button("Get Feedback"):
        show_feedback()
        st.rerun()

if st.session_state.feedback_shown:
    st.subheader("Feedback")
    conversation_history = "\n".join([f"{msg['role']}: {msg['content']}" for msg in st.session_state.messages])
    try:
        response = requests.post(
            f"{backend_url}/feedback",
            json={"conversation_history": conversation_history},
            timeout=30
        )
        response.raise_for_status()
        st.write(response.json()["feedback"])
    except requests.exceptions.RequestException as e:
        logger.error(f"Error generating feedback: {e}")
        st.error("Unable to generate feedback. Please try again later.")

    if st.button("Restart Chat", type="primary"):
        streamlit_js_eval(js_expressions="parent.window.location.reload()")