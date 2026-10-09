import streamlit as st
from rag import answer_ques


st.set_page_config(
    page_title="FinBase RAG Assistant",
    page_icon="📚",
    layout="wide"
)

# ------------------------------------------------------------------
# Styling only — palette: ink navy, slate, ledger green, paper white
# ------------------------------------------------------------------
st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=IBM+Plex+Sans:wght@400;500;600&family=IBM+Plex+Serif:wght@500;600&display=swap');

    :root {
        --ink: #12263F;
        --slate: #5B6B7F;
        --paper: #F4F6F9;
        --card: #FFFFFF;
        --line: #DDE3EB;
        --green: #0F7B5F;
        --green-dark: #0A5E49;
        --green-tint: #E6F3EE;
    }

    html, body, [class*="css"], .stApp {
        font-family: 'IBM Plex Sans', sans-serif;
        color: var(--ink);
    }

    .stApp { background: var(--paper); }

    /* Hide default Streamlit chrome (keep sidebar toggle) */
    #MainMenu, footer, [data-testid="stToolbar"], [data-testid="stDecoration"] {
        visibility: hidden;
        height: 0;
    }
    header[data-testid="stHeader"] { background: transparent; }

    .block-container {
        max-width: 820px;
        padding-top: 2.5rem;
        padding-bottom: 8rem;
    }

    /* Centered title */
    h1 {
        font-family: 'IBM Plex Serif', serif !important;
        font-weight: 600 !important;
        font-size: 2.3rem !important;
        letter-spacing: -0.01em;
        color: var(--ink) !important;
        text-align: center;
        padding-bottom: 0.2rem !important;
    }
    .tagline {
        text-align: center;
        color: var(--slate);
        font-size: 1.02rem;
        margin: 0 0 2rem 0;
    }

    h2, h3 {
        font-family: 'IBM Plex Sans', sans-serif !important;
        font-weight: 600 !important;
        color: var(--ink) !important;
    }

    p, li, label { color: var(--ink); line-height: 1.65; }

    hr {
        border: none !important;
        border-top: 1px solid var(--line) !important;
    }

    /* Sidebar */
    [data-testid="stSidebar"] {
        background: var(--card);
        border-right: 1px solid var(--line);
    }
    [data-testid="stSidebar"] h3 { font-size: 1.05rem !important; }

    /* File uploader */
    [data-testid="stFileUploaderDropzone"] {
        background: var(--paper);
        border: 1.5px dashed #B8C4D2;
        border-radius: 10px;
        transition: border-color 0.15s ease, background 0.15s ease;
    }
    [data-testid="stFileUploaderDropzone"]:hover {
        border-color: var(--green);
        background: var(--green-tint);
    }
    [data-testid="stFileUploaderDropzone"] button {
        background: var(--card);
        color: var(--ink);
        border: 1px solid var(--line);
        border-radius: 8px;
    }

    /* Chat messages */
    [data-testid="stChatMessage"] {
        background: transparent;
        padding: 0.9rem 0.2rem;
        gap: 0.9rem;
    }
    /* User messages: soft green bubble, right side feel */
    [data-testid="stChatMessage"]:has([data-testid="stChatMessageAvatarUser"]) {
        background: var(--green-tint);
        border: 1px solid #CFE6DD;
        border-radius: 14px;
        padding: 0.9rem 1.1rem;
        margin: 0.6rem 0;
    }
    /* Assistant messages: white card */
    [data-testid="stChatMessage"]:has([data-testid="stChatMessageAvatarAssistant"]) {
        background: var(--card);
        border: 1px solid var(--line);
        border-radius: 14px;
        padding: 0.9rem 1.1rem;
        margin: 0.6rem 0;
    }
    [data-testid="stChatMessage"] [data-testid^="stChatMessageAvatar"] {
        background: var(--paper);
        border: 1px solid var(--line);
    }

    /* Sources expander */
    [data-testid="stExpander"] {
        background: var(--paper);
        border: 1px solid var(--line);
        border-radius: 10px;
        margin-top: 0.6rem;
    }
    [data-testid="stExpander"] summary p { font-weight: 600; color: var(--ink); }

    /* Chat input (pinned bottom) */
    [data-testid="stBottom"] > div { background: var(--paper); }
    [data-testid="stChatInput"] {
        background: var(--card);
        border: 1px solid var(--line);
        border-radius: 16px;
        box-shadow: 0 4px 18px rgba(18, 38, 63, 0.07);
    }
    [data-testid="stChatInput"]:focus-within {
        border-color: var(--green);
        box-shadow: 0 0 0 3px rgba(15, 123, 95, 0.18);
    }
    [data-testid="stChatInput"] > div,
    [data-testid="stChatInput"] div[data-baseweb="textarea"],
    [data-testid="stChatInput"] div[data-baseweb="base-input"] {
        background: var(--card) !important;
    }
    [data-testid="stChatInput"] textarea {
        background: var(--card) !important;
        color: var(--ink) !important;
        -webkit-text-fill-color: var(--ink) !important;
        caret-color: var(--green);
    }
    [data-testid="stChatInput"] textarea::placeholder {
        color: #93A0B0 !important;
        -webkit-text-fill-color: #93A0B0 !important;
        opacity: 1;
    }
    [data-testid="stChatInput"] button {
        background: var(--green);
        color: #FFFFFF;
        border-radius: 10px;
    }
    [data-testid="stChatInput"] button:hover { background: var(--green-dark); }

    /* Alerts and spinner */
    [data-testid="stAlert"] { border-radius: 10px; border: 1px solid var(--line); }
    .stSpinner > div { border-top-color: var(--green) !important; }

    @media (max-width: 640px) {
        h1 { font-size: 1.8rem !important; }
        .block-container { padding-top: 1.5rem; }
    }
    </style>
    """,
    unsafe_allow_html=True
)

# ------------------------------------------------------------------
# Sidebar: documents
# ------------------------------------------------------------------
with st.sidebar:
    st.subheader("📄 Documents")

    uploaded_file = st.file_uploader("Upload a financial PDF",type=["pdf"])

    if uploaded_file:
        st.success(f"Uploaded: {uploaded_file.name}")

# ------------------------------------------------------------------
# Header (centered)
# ------------------------------------------------------------------
st.title("📚 FinBase RAG Assistant")
st.markdown(
    '<p class="tagline">Ask questions about your financial documents.</p>',
    unsafe_allow_html=True
)

# ------------------------------------------------------------------
# Chat
# ------------------------------------------------------------------
if "messages" not in st.session_state:
    st.session_state.messages = []


def show_sources(sources):
    with st.expander("📚 Sources"):
        for source in sources:
            st.write(
                f"**{source['source']}** — "
                f"Page {source['page']} "
                f"— Score: {source['score']:.4f}"
            )


for message in st.session_state.messages:
    avatar = "🤖" if message["role"] == "assistant" else "🧑"
    with st.chat_message(message["role"], avatar=avatar):
        st.write(message["content"])
        if message.get("sources"):
            show_sources(message["sources"])

question = st.chat_input("What was the company's revenue?")

if question:
    st.session_state.messages.append({"role": "user", "content": question})
    with st.chat_message("user", avatar="🧑"):
        st.write(question)

    with st.chat_message("assistant", avatar="🤖"):
        with st.spinner("Searching your knowledge base ..."):
            result = answer_ques(question)

        st.write(result["answer"])
        show_sources(result["sources"])

    st.session_state.messages.append({
        "role": "assistant",
        "content": result["answer"],
        "sources": result["sources"],
    })