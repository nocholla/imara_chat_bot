import pytest
import pandas as pd
from streamlit.testing.v1 import AppTest

def test_chatbot_initialization():
    at = AppTest.from_file("ui/streamlit_chatbot.py")
    at.run()
    assert not at.exception
    assert at.title[0].value == "Imara Chat Bot"

def test_chat_history_saving():
    at = AppTest.from_file("ui/streamlit_chatbot.py")
    at.session_state.profile = {"firstName": "Amani", "language": "en", "aboutMe": "I love soccer", "current_state": "Initial"}
    at.session_state.setup_complete = True
    at.session_state.messages = [{"role": "user", "content": "How do I edit my profile?"}, {"role": "assistant", "content": "It’s easy! 😊"}]
    at.run()
    at.button("Get Feedback").click()
    chat_df = pd.read_csv("data/chat_history.csv")
    assert len(chat_df) > 0
    assert chat_df.iloc[-1]["userId"].startswith("user_")