import streamlit as st
from google import genai

# 1. Page Config for Mobile
st.set_page_config(page_title="My AI App", page_icon="🤖", layout="centered")

# 2. Setup the NEW Client
try:
    # In Streamlit Secrets, ensure you have GEMINI_API_KEY = "your_key"
    client = genai.Client(api_key=st.secrets["GEMINI_API_KEY"])
except Exception as e:
    st.error(f"Setup Error: {e}")

# 3. Simple Chat UI
st.title("📱 My Mobile AI (2026)")
st.caption("Powered by Gemini 2.5 Flash")

if "messages" not in st.session_state:
    st.session_state.messages = []

# Show previous chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Chat Input
if prompt := st.chat_input("How can I help?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        # The new 2026 way to call the model
        response = client.models.generate_content(
            model="gemini-2.5-flash", 
            contents=prompt
        )
        st.markdown(response.text)
        st.session_state.messages.append({"role": "assistant", "content": response.text})
