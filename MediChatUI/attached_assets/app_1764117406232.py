import streamlit as st
import requests
import json
import html

API_URL = "http://127.0.0.1:8000"

st.set_page_config(page_title="Medical Wellness Assistant", layout="centered")

# --- Ensure session_state keys -------------------------------------------------
if "session_id" not in st.session_state:
    st.session_state.session_id = None
if "messages" not in st.session_state:
    st.session_state.messages = []
if "developer_mode" not in st.session_state:
    st.session_state.developer_mode = False

# --- Soft Pink Gradient Theme (Option E2) -------------------------------------
st.markdown(
    """
    <style>

    /* Force full-page light mode */
    html, body, [data-testid="stAppViewContainer"], [data-testid="stApp"], [data-testid="stSidebar"] {
        background-color: #fff7f5 !important;
        background: #fff7f5 !important;
        color: #5b233a !important;
    }

    .chat-container {
        max-width: 900px;
        margin: 0 auto;
    }

    /* HEADER GRADIENT */
    .header-gradient {
        background: linear-gradient(135deg, #fbcfe8, #fecdd3, #ffe4e6);
        padding: 20px;
        border-radius: 18px;
        text-align: center;
        color: #831843;
        font-size: 26px;
        font-weight: 600;
        box-shadow: 0 3px 10px rgba(0,0,0,0.08);
        margin-bottom: 10px;
    }

    /* USER BUBBLE */
    .user-bubble {
        background: #fb7185;
        color: white;
        padding: 12px 16px;
        border-radius: 18px 18px 2px 18px;
        margin: 8px 0;
        display: inline-block;
        max-width: 80%;
        box-shadow: 0 3px 8px rgba(251,113,133,0.35);
    }
    .user-avatar {
        background:#be123c;
        color:white;
        width:36px; height:36px;
        border-radius:50%;
        margin:6px;
        display:flex; align-items:center; justify-content:center;
        font-weight:700;
    }

    /* ASSISTANT BUBBLE */
    .assistant-bubble {
        background: #ffe4e6;
        color: #831843;
        padding: 12px 16px;
        border-radius: 18px 18px 18px 2px;
        margin: 8px 0;
        display: inline-block;
        max-width: 80%;
        border: 1px solid #f9a8d4;
        box-shadow: 0 3px 8px rgba(249,168,212,0.35);
    }
    .assistant-avatar {
        background:#f472b6;
        color:white;
        width:36px; height:36px;
        border-radius:50%;
        margin:6px;
        display:flex; align-items:center; justify-content:center;
        font-weight:700;
    }

    .chat-row {display:flex; align-items:flex-start;}
    .chat-row.user {justify-content:flex-end;}

    .meta-box {font-size:12px; color:#be185d; margin-top:4px;}

    </style>
    """,
    unsafe_allow_html=True,
)


# --- Title with gradient -------------------------------------------------------
st.markdown("<div class='chat-container'>", unsafe_allow_html=True)
st.markdown("<div class='header-gradient'>🌸 Medical Wellness Assistant</div>", unsafe_allow_html=True)

# --- Sidebar -------------------------------------------------------------------
with st.sidebar:
    st.header("Session")
    st.write(f"ID: {st.session_state.get('session_id')}")
    st.write(f"Messages: {len(st.session_state.messages)}")
    st.checkbox("Developer mode", key="developer_mode")

    if st.button("Clear Chat"):
        try:
            requests.post(f"{API_URL}/clear_memory", json={"session_id": st.session_state.session_id})
        except:
            pass
        st.session_state.messages = []
        st.rerun()

st.markdown("---")

# --- Display existing messages -------------------------------------------------
for m in st.session_state.messages:
    role = m.get("role")
    text = html.escape(str(m.get("content") or "")).replace("\n", "<br>")

    if role == "user":
        st.markdown(
            f"""
            <div class='chat-row user'>
                <div class='user-bubble'>{text}</div>
                <div class='avatar user-avatar'>U</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    else:
        meta = m.get("meta")
        st.markdown(
            f"""
            <div class='chat-row'>
                <div class='avatar assistant-avatar'>AI</div>
                <div class='assistant-bubble'>{text}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
        if st.session_state.developer_mode and meta:
            st.markdown(f"<div class='meta-box'>Meta: {html.escape(json.dumps(meta))}</div>", unsafe_allow_html=True)

# --- Chat Input ----------------------------------------------------------------
prompt = st.chat_input("Ask a medical or wellness question...")

if prompt:
    # Show user's message
    st.session_state.messages.append({"role": "user", "content": prompt})

    # Show temporary assistant bubble
    st.session_state.messages.append({
        "role": "assistant",
        "content": "🌸 Thinking...",
        "meta": {"temp": True},
    })
    st.rerun()

# --- Process pending temporary message ----------------------------------------
if st.session_state.messages:
    last = st.session_state.messages[-1]
    if last.get("meta", {}).get("temp"):
        user_msg = st.session_state.messages[-2]["content"]

        try:
            payload = {
                "session_id": st.session_state.session_id,
                "message": user_msg,
                "developer_mode": st.session_state.developer_mode,
                "stream": False,
            }
            r = requests.post(f"{API_URL}/chat", json=payload, timeout=120)
            data = r.json()
            answer = data.get("answer", "Error: No answer returned")
            meta = data.get("meta", {})
            sid = data.get("session_id")
            if sid: st.session_state.session_id = sid

        except Exception as e:
            answer = f"Error: {e}"
            meta = {}

        # Replace temp bubble with real answer
        st.session_state.messages[-1] = {
            "role": "assistant",
            "content": answer,
            "meta": meta,
        }

        st.rerun()

st.markdown("</div>", unsafe_allow_html=True)

# End of file
