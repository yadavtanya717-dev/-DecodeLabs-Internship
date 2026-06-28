import streamlit as st
from gemini_api import get_response
from memory import add_message, get_memory, save_memory


# ---------- PAGE CONFIG ----------
st.set_page_config(
    page_title="AI Memory Chatbot",
    page_icon="🤖",
    layout="wide"
)


# ---------- CUSTOM CSS ----------
st.markdown("""
<style>

.stApp {
    background-color: #F5EBDD;
    color: #10233F;
}

[data-testid="stSidebar"] {
    background-color: #0B1F3A;
}

[data-testid="stSidebar"] * {
    color: #F5EBDD;
}

.title {
    font-size:40px;
    font-weight:bold;
    color:#0B1F3A;
}

.subtitle{
    font-size:18px;
    color:#5B4A3A;
}

.user-msg{
    background:#0B1F3A;
    color:white;
    padding:15px;
    border-radius:18px;
    margin:10px;
}

.bot-msg{
    background:#E8D3B3;
    color:#0B1F3A;
    padding:15px;
    border-radius:18px;
    margin:10px;
}

</style>
""", unsafe_allow_html=True)


# ---------- SIDEBAR ----------

with st.sidebar:

    st.markdown("""
    <h1>🤖</h1>
    <h2>AI Memory<br>Chatbot</h2>

    <p>
    I remember conversations and learn from your chats.
    </p>

    <hr>
    """, unsafe_allow_html=True)

    if st.button("🗑 Clear Chat"):
        save_memory([])
        st.success("Conversation memory cleared.")
        st.rerun()

    memory = get_memory()

    st.markdown("### 📊 Stats")
    st.write(f"💬 Messages: {len(memory)}")
    st.write("🧠 Memory Enabled")
    st.write("⚡ Powered by Gemini")


# ---------- HEADER ----------

st.markdown("""
<div class="title">
Welcome to AI Memory Chatbot 👋
</div>

<div class="subtitle">
Your conversations are remembered locally.
</div>

<br>
""", unsafe_allow_html=True)


st.info(
    "🧠 I remember previous conversations until you clear the memory."
)


# ---------- DISPLAY CHAT ----------

messages = get_memory()

for msg in messages:

    if msg["role"] == "user":

        st.markdown(f"""
        <div class="user-msg">
        <b>You</b><br>
        {msg["content"]}
        </div>
        """, unsafe_allow_html=True)

    else:

        st.markdown(f"""
        <div class="bot-msg">
        <b>AI Memory Chatbot</b><br>
        {msg["content"]}
        </div>
        """, unsafe_allow_html=True)


# ---------- USER INPUT ----------

user_input = st.chat_input("Type your message here...")


if user_input:

    # Get history BEFORE adding current message
    history = get_memory()

    response = get_response(
        user_input,
        history
    )

    # Save conversation AFTER response
    add_message("user", user_input)
    add_message("assistant", response)

    st.rerun()