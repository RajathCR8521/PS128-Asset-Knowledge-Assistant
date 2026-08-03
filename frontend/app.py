import sys
from pathlib import Path
import tempfile

import streamlit as st

# --------------------------------------
# Add backend folder to Python path
# --------------------------------------

backend_path = Path(__file__).resolve().parent.parent / "backend"
sys.path.append(str(backend_path))

from rag import initialize_rag, answer_question
# --------------------------------------
# Page Configuration
# --------------------------------------

st.set_page_config(
    page_title="Asset Knowledge Assistant",
    page_icon="📄",
    layout="wide"
)

# --------------------------------------
# Sidebar
# --------------------------------------

st.sidebar.title("📄 Asset Knowledge Assistant")

st.sidebar.markdown("""
### Tech Stack

- 🐍 Python
- 🔍 FAISS Vector Database
- 🧠 Sentence Transformers
- 🤖 Google Gemini
- 🌐 Streamlit

---

### Project

AI-powered Asset Knowledge Assistant for document question answering using Retrieval-Augmented Generation (RAG).
""")

# --------------------------------------
# Session State
# --------------------------------------

if "initialized" not in st.session_state:
    st.session_state.initialized = False

# --------------------------------------
# Main Page
# --------------------------------------

st.title("📄 Asset Knowledge Assistant")

st.write(
    "An AI-powered document assistant that uses Retrieval-Augmented Generation (RAG) to answer questions from PDF documents."
)

# --------------------------------------
# Upload PDF
# --------------------------------------

uploaded_file = st.file_uploader(
    "Upload a PDF document",
    type=["pdf"]
)

if uploaded_file is not None:

    if (
        not st.session_state.initialized
        or st.session_state.get("current_file") != uploaded_file.name
    ):

        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_file:
            tmp_file.write(uploaded_file.read())
            pdf_path = tmp_file.name

        with st.spinner("Processing PDF..."):

            initialize_rag(pdf_path)

        st.session_state.initialized = True
        st.session_state.current_file = uploaded_file.name

        # Clear previous question and answer
        st.session_state.question = ""
        st.session_state.answer = ""

        st.success(f"'{uploaded_file.name}' loaded successfully!")
        

# --------------------------------------
# Ask Questions
# --------------------------------------

if st.session_state.initialized:

    question = st.text_input(
        "Enter your question",
        key="question"
    )

    if st.button("Ask"):

        if question.strip() == "":

            st.warning("Please enter a question.")

        else:

            with st.spinner("Generating answer..."):

                answer = answer_question(question)

            st.success("Answer generated successfully.")

            st.markdown("### Answer")

            st.write(answer)

else:

    st.info("Please upload a PDF document to begin.")

# --------------------------------------
# Footer
# --------------------------------------

st.markdown("---")
st.caption(
    "Developed by Rajath CR | Powered by Gemini, FAISS & Sentence Transformers"
)