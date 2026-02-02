import streamlit as st
import google.generativeai as genai

# 1. Page Config for Mobile
st.set_page_config(page_title="My AI App", page_icon="🤖", layout="centered")

# 2. Setup API Key (This will be pulled from Streamlit's secret settings later)
try:
    API_KEY = st.secrets["GEMINI_API_KEY"]
    genai.configure(api_key=API_KEY)
except:
    st.error("Please set the GEMINI_API_KEY in Streamlit Secrets.")

# 3. Simple UI
st.title("📱 My Mobile AI")
st.caption("Powered by Gemini 1.5 Flash")

if "messages" not in st.session_state:
    st.session_state.messages = []

# Show previous chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Chat Input (stays at bottom on mobile)
if prompt := st.chat_input("How can I help?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        model = genai.GenerativeModel('gemini-1.5-flash')
        response = model.generate_content(prompt)
        st.markdown(response.text)
        st.session_state.messages.append({"role": "assistant", "content": response.text})