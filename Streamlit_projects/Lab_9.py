import streamlit as st
import pandas as pd
import time

# Page settings
st.set_page_config(page_title="Simple Chatbot", page_icon="🤖")

st.title("🤖 Simple Chatbot")
st.write("Chat with a simple rule-based chatbot.")

# Store chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display previous messages
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

# User input
prompt = st.chat_input("Type your message...")

if prompt:
    # Save and display user message
    st.session_state.messages.append({
        "role": "user",
        "content": prompt
    })

    with st.chat_message("user"):
        st.write(prompt)

    # Generate reply
    with st.spinner("Assistant is typing..."):
        time.sleep(1)

        if "python" in prompt.lower():
            reply = "Python is a popular language for AI and Data Science."

        elif "streamlit" in prompt.lower():
            reply = "Streamlit is a Python framework for creating web apps."

        elif "hello" in prompt.lower() or "hi" in prompt.lower():
            reply = "Hello! How can I help you?"

        elif "thank" in prompt.lower():
            reply = "You're welcome!"

        else:
            reply = f"You said: {prompt}. I'm a demo chatbot!"

    # Save and display assistant reply
    st.session_state.messages.append({
        "role": "assistant",
        "content": reply
    })

    with st.chat_message("assistant"):
        st.write(reply)

# Download chat history
st.subheader("Chat Options")

if st.session_state.messages:
    chat_text = "\n".join(
        f"{msg['role'].capitalize()}: {msg['content']}"
        for msg in st.session_state.messages
    )

    st.download_button(
        label="Download Chat History",
        data=chat_text,
        file_name="chat_history.txt",
        mime="text/plain"
    )

# Clear chat history
if st.button("Clear Chat"):
    st.session_state.messages = []
    st.rerun()
