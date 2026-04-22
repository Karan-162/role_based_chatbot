import streamlit as st
import requests

# ── Page config ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="AI Chat",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Custom CSS ────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700;800&family=DM+Mono:wght@300;400;500&display=swap');

/* Global reset & theme */
html, body, [class*="css"] {
    font-family: 'DM Mono', monospace;
    background-color: #0a0a0f;
    color: #e8e6f0;
}

/* Sidebar */
[data-testid="stSidebar"] {
    background: #0f0f1a;
    border-right: 1px solid #1e1e35;
    padding-top: 1rem;
}
[data-testid="stSidebar"] * {
    font-family: 'DM Mono', monospace !important;
}

/* Hide default header */
header[data-testid="stHeader"] { display: none; }

/* Custom title area */
.app-title {
    font-family: 'Syne', sans-serif;
    font-weight: 800;
    font-size: 2rem;
    letter-spacing: -0.03em;
    background: linear-gradient(135deg, #a78bfa, #60a5fa, #34d399);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    margin-bottom: 0.15rem;
}
.app-subtitle {
    font-size: 0.7rem;
    color: #4a4a6a;
    letter-spacing: 0.15em;
    text-transform: uppercase;
    margin-bottom: 1.5rem;
}

/* Sidebar section labels */
.sidebar-label {
    font-family: 'Syne', sans-serif;
    font-size: 0.65rem;
    letter-spacing: 0.2em;
    text-transform: uppercase;
    color: #4a4a6a;
    margin: 1.2rem 0 0.4rem;
}

/* Model badge */
.model-badge {
    display: inline-block;
    background: #1a1a2e;
    border: 1px solid #2a2a4a;
    border-radius: 4px;
    padding: 2px 8px;
    font-size: 0.7rem;
    color: #a78bfa;
    letter-spacing: 0.05em;
    margin-top: 0.3rem;
}

/* Chat container */
.chat-wrapper {
    max-width: 820px;
    margin: 0 auto;
    padding: 0 1rem;
}

/* Chat bubbles */
.msg-row-user {
    display: flex;
    justify-content: flex-end;
    margin: 0.6rem 0;
}
.msg-row-ai {
    display: flex;
    justify-content: flex-start;
    margin: 0.6rem 0;
}
.bubble-user {
    background: linear-gradient(135deg, #4f46e5, #7c3aed);
    color: #fff;
    border-radius: 16px 16px 4px 16px;
    padding: 0.75rem 1.1rem;
    max-width: 72%;
    font-size: 0.85rem;
    line-height: 1.6;
    box-shadow: 0 4px 20px rgba(124,58,237,0.3);
}
.bubble-ai {
    background: #13131f;
    border: 1px solid #1e1e35;
    color: #d4d0e8;
    border-radius: 16px 16px 16px 4px;
    padding: 0.75rem 1.1rem;
    max-width: 72%;
    font-size: 0.85rem;
    line-height: 1.6;
    box-shadow: 0 4px 20px rgba(0,0,0,0.4);
}
.bubble-error {
    background: #1a0a0a;
    border: 1px solid #4a1010;
    color: #f87171;
    border-radius: 16px 16px 16px 4px;
    padding: 0.75rem 1.1rem;
    max-width: 72%;
    font-size: 0.85rem;
    line-height: 1.6;
}
.avatar {
    width: 28px;
    height: 28px;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 0.75rem;
    font-weight: 700;
    flex-shrink: 0;
    margin-top: 4px;
}
.avatar-user {
    background: #4f46e5;
    color: #fff;
    margin-left: 8px;
}
.avatar-ai {
    background: #1e1e35;
    color: #a78bfa;
    margin-right: 8px;
}

/* Search toggle chip */
.search-on  { color: #34d399; font-size: 0.75rem; }
.search-off { color: #4a4a6a; font-size: 0.75rem; }

/* Status dot */
.status-dot {
    display: inline-block;
    width: 7px; height: 7px;
    border-radius: 50%;
    background: #34d399;
    box-shadow: 0 0 8px #34d399;
    margin-right: 6px;
}

/* Selectbox & text area overrides */
[data-testid="stSelectbox"] > div > div {
    background: #13131f !important;
    border: 1px solid #2a2a4a !important;
    border-radius: 6px !important;
    color: #e8e6f0 !important;
    font-family: 'DM Mono', monospace !important;
    font-size: 0.8rem !important;
}
textarea {
    background: #13131f !important;
    border: 1px solid #2a2a4a !important;
    border-radius: 6px !important;
    color: #e8e6f0 !important;
    font-family: 'DM Mono', monospace !important;
    font-size: 0.82rem !important;
}
.stButton > button {
    background: linear-gradient(135deg, #4f46e5, #7c3aed) !important;
    color: #fff !important;
    border: none !important;
    border-radius: 8px !important;
    font-family: 'Syne', sans-serif !important;
    font-weight: 700 !important;
    font-size: 0.85rem !important;
    letter-spacing: 0.05em !important;
    padding: 0.55rem 1.5rem !important;
    transition: opacity 0.2s !important;
    width: 100%;
}
.stButton > button:hover { opacity: 0.88 !important; }

/* Divider */
.side-divider {
    border: none;
    border-top: 1px solid #1e1e35;
    margin: 1rem 0;
}
</style>
""", unsafe_allow_html=True)

# ── Constants ─────────────────────────────────────────────────────────────────
BACKEND_URL = "http://127.0.0.1:9999/chat"

MODELS = {
    "llama-3.3-70b-versatile":                      {"provider": "Groq",   "label": "LLaMA 3.3 70B Versatile"},
    "llama-3.1-8b-instant":                         {"provider": "Groq",   "label": "LLaMA 3.1 8B Instant"},
    "meta-llama/llama-4-scout-17b-16e-instruct":    {"provider": "Groq",   "label": "LLaMA 4 Scout 17B"},
    "gpt-4o-mini":                                  {"provider": "OpenAI", "label": "GPT-4o Mini"},
    "gpt-4o":                                       {"provider": "OpenAI", "label": "GPT-4o"},
}

# ── Session state ─────────────────────────────────────────────────────────────
if "messages" not in st.session_state:
    st.session_state.messages = []   # list of {"role": "user"|"assistant", "content": str}

# ── Sidebar ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown('<div class="app-title">⚡ AI Chat</div>', unsafe_allow_html=True)
    st.markdown('<div class="app-subtitle">Powered by FastAPI + LLM</div>', unsafe_allow_html=True)
    st.markdown('<span class="status-dot"></span><span style="font-size:0.7rem;color:#4a4a6a;">Backend connected on :9999</span>', unsafe_allow_html=True)

    st.markdown('<hr class="side-divider">', unsafe_allow_html=True)

    # Model selection
    st.markdown('<div class="sidebar-label">Model</div>', unsafe_allow_html=True)
    model_key = st.selectbox(
        label="model",
        options=list(MODELS.keys()),
        format_func=lambda k: MODELS[k]["label"],
        label_visibility="collapsed",
    )
    provider = MODELS[model_key]["provider"]
    st.markdown(f'<span class="model-badge">provider: {provider}</span>', unsafe_allow_html=True)

    # System prompt
    st.markdown('<div class="sidebar-label">System Prompt</div>', unsafe_allow_html=True)
    system_prompt = st.text_area(
        label="system_prompt",
        value="You are a helpful, concise, and thoughtful AI assistant.",
        height=110,
        label_visibility="collapsed",
    )

    # Web search toggle
    st.markdown('<div class="sidebar-label">Web Search</div>', unsafe_allow_html=True)
    allow_search = st.toggle("Enable web search", value=False)
    if allow_search:
        st.markdown('<span class="search-on">🟢 Search enabled</span>', unsafe_allow_html=True)
    else:
        st.markdown('<span class="search-off">⚫ Search disabled</span>', unsafe_allow_html=True)

    st.markdown('<hr class="side-divider">', unsafe_allow_html=True)

    # Clear chat
    if st.button("🗑  Clear conversation"):
        st.session_state.messages = []
        st.rerun()

    st.markdown(
        '<div style="font-size:0.65rem;color:#2a2a4a;margin-top:1.5rem;line-height:1.8;">'
        'Model · System Prompt · Search<br>settings apply to every message.'
        '</div>',
        unsafe_allow_html=True,
    )

# ── Main chat area ────────────────────────────────────────────────────────────
st.markdown('<div class="chat-wrapper">', unsafe_allow_html=True)

# Render conversation history
for msg in st.session_state.messages:
    if msg["role"] == "user":
        st.markdown(
            f'<div class="msg-row-user">'
            f'  <div class="bubble-user">{msg["content"]}</div>'
            f'  <div class="avatar avatar-user">U</div>'
            f'</div>',
            unsafe_allow_html=True,
        )
    else:
        st.markdown(
            f'<div class="msg-row-ai">'
            f'  <div class="avatar avatar-ai">AI</div>'
            f'  <div class="bubble-ai">{msg["content"]}</div>'
            f'</div>',
            unsafe_allow_html=True,
        )

st.markdown('</div>', unsafe_allow_html=True)

# ── Input row ─────────────────────────────────────────────────────────────────
st.markdown("<br>", unsafe_allow_html=True)
col_input, col_btn = st.columns([5, 1], gap="small")

with col_input:
    user_input = st.chat_input("Type a message…")

# Handle submission (chat_input auto-submits on Enter)
if user_input and user_input.strip():
    user_text = user_input.strip()

    # Add user message to history
    st.session_state.messages.append({"role": "user", "content": user_text})

    # Build payload — messages list is all user turns in order
    history_texts = [m["content"] for m in st.session_state.messages if m["role"] == "user"]

    payload = {
        "model_name":    model_key,
        "model_provider": provider,
        "System_prompt": system_prompt,
        "messages":      history_texts,
        "allow_search":  allow_search,
    }

    with st.spinner("Thinking…"):
        try:
            resp = requests.post(BACKEND_URL, json=payload, timeout=60)
            resp.raise_for_status()
            data = resp.json()

            # ── Parse response ──────────────────────────────────────────────
            # Handles common response shapes from various agent setups
            if isinstance(data, str):
                reply = data
            elif isinstance(data, dict):
                # Try common keys
                reply = (
                    data.get("response")
                    or data.get("message")
                    or data.get("content")
                    or data.get("output")
                    or data.get("answer")
                    or data.get("error")
                    or str(data)
                )
            else:
                reply = str(data)

            st.session_state.messages.append({"role": "assistant", "content": reply})

        except requests.exceptions.ConnectionError:
            st.session_state.messages.append({
                "role": "assistant",
                "content": "⚠️ Could not reach the backend at `127.0.0.1:9999`. Make sure your FastAPI server is running.",
            })
        except requests.exceptions.Timeout:
            st.session_state.messages.append({
                "role": "assistant",
                "content": "⏱ Request timed out. The model may be slow to respond — try again.",
            })
        except Exception as e:
            st.session_state.messages.append({
                "role": "assistant",
                "content": f"❌ Error: {e}",
            })

    st.rerun()