
import streamlit as st
from rag import answer_ques

st.set_page_config(
    page_title="FinBase RAG Assistant",
    page_icon="📚",
    layout="wide"
)

# Cache the embedding model if your RAG pipeline uses this same model.
# This cache only helps if the pipeline uses this function.
@st.cache_resource
def load_embedding_model():
    from sentence_transformers import SentenceTransformer
    return SentenceTransformer("BAAI/bge-small-en-v1.5")


# ---------------------------------------------------------
# Styling
# ---------------------------------------------------------
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

    #MainMenu, footer, [data-testid="stToolbar"],
    [data-testid="stDecoration"] {
        visibility: hidden;
        height: 0;
    }

    header[data-testid="stHeader"] { background: transparent; }

    .block-container {
        max-width: 820px;
        padding-top: 2.5rem;
        padding-bottom: 8rem;
    }

    h1 {
        font-family: 'IBM Plex Serif', serif !important;
        font-weight: 600 !important;
        font-size: 2.3rem !important;
        letter-spacing: -0.01em;
        color: var(--ink) !important;
        text-align: center;
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

    [data-testid="stSidebar"] {
        background: var(--card);
        border-right: 1px solid var(--line);
    }

    [data-testid="stFileUploaderDropzone"] {
        background: var(--paper);
        border: 1.5px dashed #B8C4D2;
        border-radius: 10px;
    }

    [data-testid="stChatMessage"] {
        background: transparent;
        padding: 0.9rem 0.2rem;
        gap: 0.9rem;
    }

    [data-testid="stChatMessage"]:has([data-testid="stChatMessageAvatarUser"]) {
        background: var(--green-tint);
        border: 1px solid #CFE6DD;
        border-radius: 14px;
        padding: 0.9rem 1.1rem;
        margin: 0.6rem 0;
    }

    [data-testid="stChatMessage"]:has([data-testid="stChatMessageAvatarAssistant"]) {
        background: var(--card);
        border: 1px solid var(--line);
        border-radius: 14px;
        padding: 0.9rem 1.1rem;
        margin: 0.6rem 0;
    }

    [data-testid="stExpander"] {
        background: var(--paper);
        border: 1px solid var(--line);
        border-radius: 10px;
        margin-top: 0.6rem;
    }

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

    [data-testid="stChatInput"] textarea {
        color: var(--ink) !important;
        caret-color: var(--green);
    }

    [data-testid="stChatInput"] button {
        background: var(--green);
        color: white;
        border-radius: 10px;
    }

    [data-testid="stChatInput"] button:hover {
        background: var(--green-dark);
    }

    @media (max-width: 640px) {
        h1 { font-size: 1.8rem !important; }
        .block-container { padding-top: 1.5rem; }
    }

    /* Fix dark buttons and uploader text */
[data-testid="stFileUploaderDropzone"] button,
[data-testid="stFileUploaderDropzone"] button p {
    background-color: #FFFFFF !important;
    color: #12263F !important;
}

[data-testid="stFileUploaderDropzone"] small,
[data-testid="stFileUploaderDropzone"] span {
    color: #5B6B7F !important;
}

/* Fix New Chat button */
[data-testid="stSidebar"] button {
    background-color: #E6F3EE !important;
    color: #12263F !important;
    border: 1px solid #CFE6DD !important;
    border-radius: 10px !important;
}

[data-testid="stSidebar"] button:hover {
    background-color: #D4EBE2 !important;
    color: #12263F !important;
}

/* Completely white chat input */
[data-testid="stBottom"] {
    background: #FFFFFF !important;
}

[data-testid="stChatInput"] {
    background: #FFFFFF !important;
    background-color: #FFFFFF !important;
    border: 1px solid #DDE3EB !important;
    border-radius: 16px !important;
    box-shadow: 0 4px 18px rgba(18, 38, 63, 0.07) !important;
}

[data-testid="stChatInput"] > div,
[data-testid="stChatInput"] div[data-baseweb="textarea"],
[data-testid="stChatInput"] textarea {
    background: #FFFFFF !important;
    background-color: #FFFFFF !important;
    color: #12263F !important;
    -webkit-text-fill-color: #12263F !important;
    border-color: #DDE3EB !important;
}

[data-testid="stChatInput"] textarea::placeholder {
    color: #5B6B7F !important;
    -webkit-text-fill-color: #5B6B7F !important;
    opacity: 1 !important;
}

[data-testid="stChatInput"] button {
    background: #0F7B5F !important;
    color: #FFFFFF !important;
    border-radius: 10px !important;
}
    </style>
    """,
    unsafe_allow_html=True
)


# ---------------------------------------------------------
# Session state: current conversation + session chat history
# ---------------------------------------------------------
if "messages" not in st.session_state:
    st.session_state.messages = []

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

if "current_chat_id" not in st.session_state:
    st.session_state.current_chat_id = 1


# ---------------------------------------------------------
# Sidebar
# ---------------------------------------------------------
with st.sidebar:
    st.subheader("📄 Documents")

    uploaded_file = st.file_uploader(
        "Upload a financial PDF",
        type=["pdf"],
        key="financial_pdf"
    )

    if uploaded_file:
        st.success(f"Selected: {uploaded_file.name}")
        st.caption(
            "The current RAG pipeline uses its configured knowledge base. "
            "This upload widget does not yet add the PDF to that knowledge base."
        )

    st.divider()
    st.subheader("💬 Chat History")

    if st.button("＋ New Chat", use_container_width=True):
        if st.session_state.messages:
            st.session_state.chat_history.append({
                "id": st.session_state.current_chat_id,
                "messages": st.session_state.messages.copy()
            })

        st.session_state.current_chat_id += 1
        st.session_state.messages = []
        st.rerun()

    # Show earlier chats from this Streamlit session
    for index, chat in enumerate(
        reversed(st.session_state.chat_history), start=1
    ):
        first_question = next(
            (
                msg["content"]
                for msg in chat["messages"]
                if msg["role"] == "user"
            ),
            "Empty conversation"
        )

        st.caption(f"Chat {chat['id']}")
        st.write(first_question[:65])


# ---------------------------------------------------------
# Header
# ---------------------------------------------------------
st.title("📚 FinBase RAG Assistant")
st.markdown(
    '<p class="tagline">Ask questions about your financial documents.</p>',
    unsafe_allow_html=True
)


# ---------------------------------------------------------
# Source references
# ---------------------------------------------------------
def show_sources(sources):
    if not sources:
        return

    with st.expander("📚 Sources"):
        for source in sources:
            st.write(
                f"**{source['source']}** — "
                f"Page {source['page']} — "
                f"Score: {source['score']:.4f}"
            )


# ---------------------------------------------------------
# Render previous messages in the current chat
# ---------------------------------------------------------
for message in st.session_state.messages:
    avatar = "🤖" if message["role"] == "assistant" else "🧑"

    with st.chat_message(message["role"], avatar=avatar):
        st.write(message["content"])

        if message.get("sources"):
            show_sources(message["sources"])


# ---------------------------------------------------------
# RAG-connected question input
# ---------------------------------------------------------
question = st.chat_input("What was the company's revenue?")

if question:
    st.session_state.messages.append({
        "role": "user",
        "content": question
    })

    with st.chat_message("user", avatar="🧑"):
        st.write(question)

    with st.chat_message("assistant", avatar="🤖"):
        try:
            with st.spinner("Searching your knowledge base..."):
                result = answer_ques(question)

            answer = result["answer"]
            sources = result.get("sources", [])

            st.write(answer)
            show_sources(sources)

            st.session_state.messages.append({
                "role": "assistant",
                "content": answer,
                "sources": sources
            })

        except Exception as error:
            st.error("Something went wrong while generating the answer.")
            st.caption(f"Error details: {error}")
