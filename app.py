
import streamlit as st
from huggingface_hub import InferenceClient

st.set_page_config(
    page_title="Nova AI",
    page_icon="✨",
    layout="centered"
)

st.markdown("""
<style>
.stApp {
    background: linear-gradient(135deg, #0b1020, #21123b);
    color: white;
}
h1 {
    color: #c4b5fd;
    text-align: center;
}
</style>
""", unsafe_allow_html=True)

st.title("✨ Nova AI")
st.caption("Your AI assistant")

try:
    token = st.secrets["HF_TOKEN"]
except (KeyError, FileNotFoundError):
    st.error("HF_TOKEN is missing. Add it in Streamlit Cloud → Settings → Secrets.")
    st.stop()

client = InferenceClient(
    api_key=token,
    provider="auto"
)

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

prompt = st.chat_input("Ask Nova AI anything...")

if prompt:
    st.session_state.messages.append(
        {"role": "user", "content": prompt}
    )

    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Nova is thinking..."):
            try:
                response = client.chat.completions.create(
                    model="google/gemma-2-2b-it",
                    messages=[
                        {
                            "role": "system",
                            "content": "You are Nova AI, a helpful and friendly assistant."
                        },
                        *st.session_state.messages
                    ],
                    max_tokens=300
                )

                answer = response.choices[0].message.content
                st.markdown(answer)

                st.session_state.messages.append(
                    {"role": "assistant", "content": answer}
                )

            except Exception as e:
                st.error(
                    "Nova AI could not connect to the hosted model. "
                    "Check your Hugging Face token permissions, model availability, "
                    "and inference credits."
                )
                st.caption(f"Technical details: {e}")
                st.session_state.messages.pop()

