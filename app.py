import streamlit as st
from backend.models import generate_response
from backend.database import init_db, save_interaction

# --- Setup ---
init_db()
user_id = "katleho_victor"

st.set_page_config(
    page_title="Soso.AI – Chat with Katleho's Assistant",
    page_icon="🧠",  # You can also use "💬", "🧠", etc.
    layout="centered"
)

# --- Styling ---
st.markdown("""
    <style>
        .stApp {
            background-color: #0d1b2a;  /* Deep dark blue */
            font-family: 'Segoe UI', sans-serif;
        }

        .chat-container {
            max-width: 700px;
            margin: auto;
        }

        .chat-bubble {
            padding: 12px 18px;
            border-radius: 18px;
            margin: 8px 0;
            max-width: 75%;
            line-height: 1.5;
            word-wrap: break-word;
        }

        .user-message {
            background-color: #1b263b;
            color: #f1f1f1;
            margin-left: auto;
            text-align: right;
        }

        .soso-message {
            background-color: #415a77;
            color: #ffffff;
            margin-right: auto;
            text-align: left;
        }

        .header {
            text-align: center;
            font-size: 36px;
            font-weight: bold;
            margin: 20px 0 10px;
            color: #e0e1dd;
        }

        .message-block {
            display: flex;
            flex-direction: column;
        }
    </style>
""", unsafe_allow_html=True)

# --- Header ---
st.markdown("<div class='header'>Soso.AI! Katleho Victor's AI Assistant</div>", unsafe_allow_html=True)

# --- Chat state ---
if "messages" not in st.session_state:
    st.session_state.messages = []

# --- Display messages ---
st.markdown("<div class='chat-container'>", unsafe_allow_html=True)
for msg in st.session_state.messages:
    bubble_class = "user-message" if msg["role"] == "user" else "soso-message"
    st.markdown(f"<div class='chat-bubble {bubble_class}'>{msg['content']}</div>", unsafe_allow_html=True)
st.markdown("</div>", unsafe_allow_html=True)

# --- Input & response ---
if prompt := st.chat_input("Ask me anything about Mr Molangeni..."):
    # Add user prompt to history
    st.session_state.messages.append({"role": "user", "content": prompt})

    # Display user message immediately
    st.markdown("<div class='chat-container'>", unsafe_allow_html=True)
    st.markdown(f"<div class='chat-bubble user-message'>{prompt}</div>", unsafe_allow_html=True)

    # Show spinner while generating response
    with st.spinner("💭 Soso is thinking..."):
        response = generate_response(prompt)

    # Display response
    st.markdown(f"<div class='chat-bubble soso-message'>{response}</div>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

    # Save to session and DB
    st.session_state.messages.append({"role": "assistant", "content": response})
    save_interaction(user_id, prompt, response)
