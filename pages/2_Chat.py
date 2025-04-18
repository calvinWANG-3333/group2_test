import streamlit as st
import requests

st.set_page_config(page_title="Chat", layout="wide")
st.title("💬 Chat with LLM")

st.markdown("""
    <style>
        .stApp {
            background-image: url("https://i.imgur.com/j6CjBvn.jpeg");
            background-size: cover;
            background-position: center;
            background-repeat: no-repeat;
            background-attachment: fixed;
        }

        .title {
            font-size: 40px;
            font-weight: bold;
            color: #ffecec;
            text-shadow: 2px 2px 4px #000000;
        }

        h1, h2, h3, h4, h5, h6 {
            color: #fff0f0 !important;
            text-shadow: 1px 1px 2px #000;
        }

        .stAlert-success {
            color: #004d00 !important;
            background-color: rgba(232, 255, 232, 0.95) !important;
        }

        button[kind="primary"] {
            background-color: #ff6699 !important;
            color: white !important;
            border: None;
            font-weight: bold;
        }
    </style>
""", unsafe_allow_html=True)


# Initialization
if "chat_sessions" not in st.session_state:
    st.session_state.chat_sessions = {"Session 1": []}
    st.session_state.active_session = "Session 1"
if "messages" not in st.session_state:
    st.session_state.messages = []

# Sidebar
with st.sidebar:
    st.header("⚙️ Settings")

    # Model selection
    model = st.selectbox(
        "🤖 Choose Model",
        ["deepseek-r1-distill-qwen-7b", "another-model-id"],
        index=0,
        key="model_choice"
    )

    # Display session selector
    session_names = list(st.session_state.chat_sessions.keys())
    selected_session = st.selectbox("🕘 Chat History", session_names)

    if selected_session != st.session_state.active_session:
        st.session_state.active_session = selected_session
        st.session_state.messages = st.session_state.chat_sessions[selected_session]

    # Clear current chat
    if st.button("🧹 Clear This Chat"):
        st.session_state.messages = []
        st.session_state.chat_sessions[st.session_state.active_session] = []
        st.success("Chat cleared.")

# New Chat Button (top of main area)
if st.button("➕ New Chat"):
    new_name = f"Session {len(st.session_state.chat_sessions) + 1}"
    st.session_state.chat_sessions[new_name] = []
    st.session_state.active_session = new_name
    st.session_state.messages = []
    st.experimental_rerun()

#  Display Chat History
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

#  Call LM Studio API


def call_local_llm(prompt: str, model: str) -> str:
    """
    Calls the LM Studio local API server using OpenAI-compatible /v1/chat/completions.
    """
    url = "http://127.0.0.1:1234/v1/chat/completions"
    headers = {"Content-Type": "application/json"}
    payload = {
        "model": model,
        "messages": [
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.7,
        "max_tokens": 512
    }

    try:
        response = requests.post(url, headers=headers,
                                 json=payload, timeout=30)
        response.raise_for_status()
        return response.json()["choices"][0]["message"]["content"]
    except Exception as e:
        return f"⚠️ Error: {e}"


# User Input + Response
if user_input := st.chat_input("Type your message here..."):
    user_msg = {"role": "user", "content": user_input}
    st.session_state.messages.append(user_msg)
    st.session_state.chat_sessions[st.session_state.active_session].append(
        user_msg)

    with st.chat_message("user"):
        st.markdown(user_input)

    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            response = call_local_llm(
                user_input, st.session_state.model_choice)
            st.markdown(response)
            assistant_msg = {"role": "assistant", "content": response}
            st.session_state.messages.append(assistant_msg)
            st.session_state.chat_sessions[st.session_state.active_session].append(
                assistant_msg)
