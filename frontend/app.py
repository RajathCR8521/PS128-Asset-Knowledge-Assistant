import requests
import streamlit as st


# ============================================================
# CONFIG
# ============================================================

BACKEND_URL = "http://127.0.0.1:8000"


# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="PS128 Asset Knowledge Assistant",
    page_icon="⚡",
    layout="centered"
)


# ============================================================
# SESSION STATE
# ============================================================

if "messages" not in st.session_state:
    st.session_state.messages = []

if "knowledge_base_ready" not in st.session_state:
    st.session_state.knowledge_base_ready = False


# ============================================================
# BACKEND CHECK
# ============================================================

def check_backend():

    try:
        response = requests.get(
            f"{BACKEND_URL}/health",
            timeout=5
        )

        return response.status_code == 200

    except requests.exceptions.RequestException:
        return False


# ============================================================
# INITIALIZE KNOWLEDGE BASE
# ============================================================

def initialize_knowledge_base():

    try:

        response = requests.post(
            f"{BACKEND_URL}/initialize",
            timeout=300
        )

        if response.status_code == 200:

            return True, response.json()

        return False, response.text

    except requests.exceptions.RequestException as e:

        return False, str(e)


# ============================================================
# ASK QUESTION
# ============================================================

def ask_backend(question):

    try:

        response = requests.post(
            f"{BACKEND_URL}/ask",
            json={
                "question": question
            },
            timeout=180
        )

        if response.status_code == 200:

            return True, response.json()

        return False, response.text

    except requests.exceptions.RequestException as e:

        return False, str(e)


# ============================================================
# HEADER
# ============================================================

st.title("⚡ Asset Knowledge Assistant")

st.caption(
    "Retrieval-Augmented Generation for Energy & Utilities "
    "Technical Documentation"
)

st.info(
    "PS128 • Energy & Utilities • RAG"
)


# ============================================================
# BACKEND STATUS
# ============================================================

st.subheader("System Status")

if check_backend():

    st.success("🟢 Backend is online")

else:

    st.error(
        "🔴 Backend is offline. "
        "Start FastAPI using the command shown below."
    )

    st.code(
        "uvicorn backend.main:app --reload",
        language="bash"
    )


# ============================================================
# KNOWLEDGE BASE
# ============================================================

st.subheader("📚 Knowledge Base")


if st.session_state.knowledge_base_ready:

    st.success("Knowledge base is ready.")

else:

    if st.button(
        "Initialize Knowledge Base",
        type="primary",
        use_container_width=True
    ):

        with st.spinner(
            "Processing documents and building the vector index..."
        ):

            success, result = initialize_knowledge_base()

        if success:

            st.session_state.knowledge_base_ready = True

            st.success(
                "Knowledge base initialized successfully!"
            )

            st.json(result)

        else:

            st.error(
                f"Initialization failed: {result}"
            )


# ============================================================
# QUESTION SECTION
# ============================================================

st.subheader("💬 Ask a Question")

st.caption(
    "Ask questions about transformers, maintenance, "
    "protection systems, and other technical documentation."
)


# ============================================================
# CHAT HISTORY
# ============================================================

for message in st.session_state.messages:

    with st.chat_message(message["role"]):

        st.markdown(message["content"])

        if (
            message["role"] == "assistant"
            and message.get("sources")
        ):

            with st.expander("📄 Sources"):

                for source in message["sources"]:

                    st.write(f"• {source}")


# ============================================================
# QUESTION INPUT
# ============================================================

question = st.chat_input(
    "Ask something about the technical documents..."
)


# ============================================================
# PROCESS QUESTION
# ============================================================

if question:

    if not st.session_state.knowledge_base_ready:

        st.warning(
            "Please initialize the knowledge base first."
        )

        st.stop()


    # USER MESSAGE

    st.session_state.messages.append(
        {
            "role": "user",
            "content": question
        }
    )

    with st.chat_message("user"):

        st.markdown(question)


    # ASSISTANT MESSAGE

    with st.chat_message("assistant"):

        with st.spinner(
            "Searching technical documents..."
        ):

            success, result = ask_backend(question)


        if success:

            answer = result.get(
                "answer",
                "No answer returned."
            )

            sources = result.get(
                "sources",
                []
            )

            st.markdown(answer)


            if sources:

                with st.expander("📄 Sources"):

                    for source in sources:

                        st.write(f"• {source}")


            st.session_state.messages.append(
                {
                    "role": "assistant",
                    "content": answer,
                    "sources": sources
                }
            )

        else:

            error = f"Unexpected error: {result}"

            st.error(error)

            st.session_state.messages.append(
                {
                    "role": "assistant",
                    "content": error,
                    "sources": []
                }
            )


# ============================================================
# FOOTER
# ============================================================

st.divider()

st.caption(
    "PS128 Asset Knowledge Assistant • "
    "FastAPI + FAISS + Sentence Transformers + Gemini"
)