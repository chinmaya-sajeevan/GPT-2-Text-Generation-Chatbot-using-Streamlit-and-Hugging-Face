import streamlit as st
from transformers import pipeline

# Page Configuration

st.set_page_config(
    page_title="GPT-2 Text Generation Chatbot",
    page_icon="🤖"
)

st.title("🤖 GPT-2 Text Generation Chatbot")

# Load GPT-2 Model (Cached)

@st.cache_resource
def load_model():
    generator = pipeline(
        "text-generation",
        model="gpt2"
    )
    return generator

chatbot = load_model()

# Session State (Chat Memory)

if "messages" not in st.session_state:
    st.session_state.messages = []

# User Input

user_input = st.text_input("You:", placeholder="Ask a question...")

# Generate Response

if st.button("Send") and user_input:

    # Prompt Engineering (IMPORTANT)
    prompt = f"""
You are a helpful AI assistant.
Answer clearly and briefly.

Question: {user_input}
Answer:
"""

    with st.spinner("Bot is thinking..."):

        response = chatbot(
            prompt,
            max_new_tokens=60,
            temperature=0.3,
            top_p=0.85,
            repetition_penalty=1.3,
            do_sample=True
        )

    # Clean Output
    bot_reply = response[0]["generated_text"]
    bot_reply = bot_reply.replace(prompt, "").strip()
    bot_reply = bot_reply.lstrip('?"\' ')

    # Save Chat
    st.session_state.messages.append(("You", user_input))
    st.session_state.messages.append(("Bot", bot_reply))

# Display Conversation

for speaker, message in st.session_state.messages:
    if speaker == "You":
        st.markdown(f"🧑 **You:** {message}")
    else:
        st.markdown(f"🤖 **Bot:** {message}")

# Clear Chat Button

if st.button("Clear Chat"):
    st.session_state.messages = []