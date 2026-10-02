
import streamlit as st
import ollama

# ---------------- PAGE SETTINGS ----------------
st.set_page_config(
    page_title="Meghana AI",
    page_icon="✨",
    layout="centered"
)

MODEL = "llama3.2:1b"

# ---------------- BEAUTIFUL DESIGN ----------------
st.markdown("""
<style>
.stApp {
    background:
        radial-gradient(ellipse at top, #25204b 0%, transparent 55%),
        linear-gradient(135deg, #0b1020, #121126, #0b1220);
    color: #f8fafc;
}

[data-testid="stHeader"] {
    background: transparent;
}

[data-testid="stSidebar"] {
    background: #101225;
    border-right: 1px solid #292747;
}

.hero {
    text-align: center;
    padding: 28px 0 22px;
}

.logo {
    display: inline-block;
    font-size: 42px;
    background: linear-gradient(135deg, #8b5cf6, #38bdf8);
    padding: 12px 20px;
    border-radius: 22px;
    margin-bottom: 12px;
    box-shadow: 0 0 35px #8b5cf644;
}

.hero h1 {
    font-size: 42px;
    font-weight: 800;
    margin: 0;
    background: linear-gradient(90deg, #c4b5fd, #7dd3fc);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}

.hero p {
    color: #b5b9d6;
    font-size: 15px;
}

.welcome {
    background: linear-gradient(
        135deg,
        rgba(139,92,246,.15),
        rgba(56,189,248,.07)
    );
    border: 1px solid #45416d;
    border-radius: 20px;
    padding: 22px;
    margin: 12px 0 20px;
}

.welcome h3 {
    margin-top: 0;
    color: #ddd6fe;
}

.welcome p {
    color: #cbd5e1;
}

div.stButton > button {
    background: #201d3d;
    color: #f8fafc;
    border: 1px solid #514779;
    border-radius: 13px;
    min-height: 48px;
    transition: all .2s ease;
}

div.stButton > button:hover {
    background: #33285c;
    border-color: #a78bfa;
    color: white;
}

[data-testid="stChatMessage"] {
    background: rgba(255,255,255,.045);
    border: 1px solid rgba(167,139,250,.18);
    border-radius: 17px;
    padding: 14px;
    margin-bottom: 12px;
}

[data-testid="stChatInput"] {
    border: 1px solid #6756a7;
    border-radius: 17px;
}

.footer {
    color: #969bb8;
    font-size: 12px;
    text-align: center;
    padding: 20px 0;
}
</style>
""", unsafe_allow_html=True)

# ---------------- CHAT HISTORY ----------------
if "messages" not in st.session_state:
    st.session_state.messages = []

if "prompt" not in st.session_state:
    st.session_state.prompt = None

# ---------------- SIDEBAR ----------------
with st.sidebar:
    st.markdown("## ✨ Meghana AI")
    st.caption("Your personal AI companion")
    st.markdown("---")

    st.markdown("### 💡 Things you can ask")
    st.markdown("""
    - 📚 Explain difficult concepts
    - 💻 Help with Python code
    - 🎓 Suggest college projects
    - ✍️ Improve your writing
    """)

    st.markdown("---")
    st.caption("Powered by Ollama")
    st.caption("Runs an AI model on your computer.")

    if st.button("🗑️ Clear conversation",
                 use_container_width=True):
        st.session_state.messages = []
        st.session_state.prompt = None
        st.rerun()

# ---------------- MAIN HEADER ----------------
st.markdown("""
<div class="hero">
    <div class="logo">✦</div>
    <h1>Nova AI</h1>
    <p>Your ideas deserve intelligent answers.</p>
</div>
""", unsafe_allow_html=True)

# ---------------- WELCOME SCREEN ----------------
if not st.session_state.messages:
    st.markdown("""
    <div class="welcome">
        <h3>👋 Welcome to your AI space!</h3>
        <p>Ask a question, explore an idea, or learn
        something new. I'm ready to help.</p>
    </div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col1:
        if st.button("🐍 Learn Python",
                     use_container_width=True):
            st.session_state.prompt = (
                "Teach me Python basics with examples."
            )

        if st.button("💡 Project ideas",
                     use_container_width=True):
            st.session_state.prompt = (
                "Suggest 5 useful BTech CSE projects."
            )

    with col2:
        if st.button("🧠 Explain AI",
                     use_container_width=True):
            st.session_state.prompt = (
                "Explain artificial intelligence simply."
            )

        if st.button("💼 Interview preparation",
                     use_container_width=True):
            st.session_state.prompt = (
                "Give me beginner software interview questions."
            )

# ---------------- DISPLAY MESSAGES ----------------
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# ---------------- USER INPUT ----------------
user_prompt = st.chat_input("Message Meghana...")

if st.session_state.prompt:
    user_prompt = st.session_state.prompt
    st.session_state.prompt = None

# ---------------- AI RESPONSE ----------------
if user_prompt:
    st.session_state.messages.append({
        "role": "user",
        "content": user_prompt
    })

    with st.chat_message("user"):
        st.markdown(user_prompt)

    with st.chat_message("assistant"):
        try:
            with st.spinner("Nova is thinking..."):
                response = ollama.chat(
                    model=MODEL,
                    messages=[
                        {
                            "role": "system",
                            "content": (
                                "You are Nova, a friendly AI assistant. "
                                "Answer clearly and accurately. "
                                "Use simple language and examples."
                            )
                        },
                        *st.session_state.messages
                    ]
                )

                answer = response["message"]["content"]

            st.markdown(answer)

            st.session_state.messages.append({
                "role": "assistant",
                "content": answer
            })

        except Exception as e:
            # Remove the unanswered user message so
            # it is not sent again as a failed turn.
            st.session_state.messages.pop()

            st.error(
                "Could not connect to the local AI model."
            )
            st.code(f"{type(e).__name__}: {e}")

            st.info(
                "Make sure Ollama is installed and running, "
                "then run: ollama run llama3.2:1b"
            )

# ---------------- FOOTER ----------------
st.markdown("""
<div class="footer">
    ✨ Meghana AI · Made with Python and Streamlit
</div>
""", unsafe_allow_html=True)
