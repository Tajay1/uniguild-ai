import streamlit as st
import requests

# ==============================
# PAGE CONFIG
# ==============================
st.set_page_config(
    page_title="UniGuild AI",
    page_icon="🎓",
    layout="wide"
)

API_URL = st.secrets["http://localhost:3001/api/v1/workspace/UniGuild/chat"]
API_KEY = st.secrets["4JW5Z6P-GC9MBN4-J8BKYA4-DJGW1ZB"]

# ==============================
# CUSTOM CSS (THIS MAKES IT NICE)
# ==============================
st.markdown("""
<style>
body {
    background-color: #0f172a;
    color: white;
}

.main {
    background-color: #0f172a;
}

h1, h2, h3 {
    color: #38bdf8;
}

.stChatMessage {
    border-radius: 12px;
    padding: 10px;
}

[data-testid="stChatMessageContent"] {
    font-size: 16px;
}

.stTextInput input {
    border-radius: 10px;
}

.stButton>button {
    background-color: #38bdf8;
    color: black;
    border-radius: 10px;
}
</style>
""", unsafe_allow_html=True)

# ==============================
# HERO SECTION
# ==============================

st.markdown("""
# 🎓 UniGuild AI  
### 🚀 Your Smart Academic & Business Assistant  

Get instant answers, strategies, and insights powered by AI.
""")

st.divider()

# ==============================
# QUICK PROMPTS (COOL FEATURE)
# ==============================

col1, col2, col3 = st.columns(3)

if col1.button("📈 Business Ideas"):
    st.session_state.prompt = "Give me a profitable business idea"

if col2.button("📚 Study Help"):
    st.session_state.prompt = "Explain this topic simply"

if col3.button("💡 Startup Advice"):
    st.session_state.prompt = "How do I start a business?"

# ==============================
# SESSION STATE
# ==============================

if "messages" not in st.session_state:
    st.session_state.messages = []

# ==============================
# DISPLAY CHAT
# ==============================

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

# ==============================
# INPUT
# ==============================

user_input = st.chat_input("Ask UniGuild AI anything...")

# Handle quick prompt click
if "prompt" in st.session_state:
    user_input = st.session_state.prompt
    del st.session_state.prompt

if user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})

    with st.chat_message("user"):
        st.write(user_input)

    with st.chat_message("assistant"):
        with st.spinner("🤖 Thinking..."):
            try:
                response = requests.post(
                    API_URL,
                    headers={
                        "Authorization": f"Bearer {API_KEY}",
                        "Content-Type": "application/json"
                    },
                    json={"message": user_input},
                    timeout=60
                )

                if response.status_code == 200:
                    reply = response.json().get("textResponse", "No response.")
                else:
                    reply = f"Error: {response.status_code}"

            except Exception as e:
                reply = f"Connection error: {e}"

            st.write(reply)

    st.session_state.messages.append({"role": "assistant", "content": reply})
