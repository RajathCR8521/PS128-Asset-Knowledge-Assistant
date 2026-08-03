import numpy as np

from pdf_reader import read_pdf
from embedder import create_embeddings, model
from vector_store import create_index, add_embeddings, search
from llm import generate_answer

# ==================================================
# Configuration
# ==================================================

CHUNK_SIZE = 500
TOP_K = 3

# ==================================================
# Global Variables
# ==================================================

chunks = []
index = None


def initialize_rag(pdf_path="data/raw/manual.pdf"):
    """
    Initializes the complete RAG pipeline for the given PDF.
    """

    global chunks
    global index

    print("\n========== INITIALIZING RAG ==========\n")

    # --------------------------------------
    # Read PDF
    # --------------------------------------

    full_text = read_pdf(pdf_path)

    # --------------------------------------
    # Create Chunks
    # --------------------------------------

    chunks = []

    for i in range(0, len(full_text), CHUNK_SIZE):
        chunk = full_text[i:i + CHUNK_SIZE].strip()

        if chunk:
            chunks.append(chunk)

    print(f"Created {len(chunks)} chunks.")

    # --------------------------------------
    # Generate Embeddings
    # --------------------------------------

    embeddings = create_embeddings(chunks)

    embedding_matrix = np.asarray(
        embeddings,
        dtype=np.float32
    )

    # --------------------------------------
    # Create FAISS Index
    # --------------------------------------

    dimension = embedding_matrix.shape[1]

    index = create_index(dimension)

    add_embeddings(index, embedding_matrix)

    print("\nRAG initialized successfully!\n")


def answer_question(question):
    """
    Answers a user question using Retrieval-Augmented Generation.
    """

    global chunks
    global index

    if index is None:
        raise RuntimeError(
            "RAG is not initialized. Upload a PDF first."
        )

    if not question.strip():
        return "Please enter a valid question."

    # --------------------------------------
    # Embed Question
    # --------------------------------------

    question_embedding = model.encode(
        question,
        convert_to_numpy=True
    )

    question_embedding = np.asarray(
        [question_embedding],
        dtype=np.float32
    )

    # --------------------------------------
    # Search FAISS
    # --------------------------------------

    distances, indices = search(
        index,
        question_embedding,
        TOP_K
    )

    # --------------------------------------
    # Build Context
    # --------------------------------------

    retrieved_chunks = []

    for idx in indices[0]:
        if idx < len(chunks):
            retrieved_chunks.append(chunks[idx])

    context = "\n\n".join(retrieved_chunks)

    # --------------------------------------
    # Prompt
    # --------------------------------------

    prompt = f"""
You are an intelligent document assistant.

Answer ONLY using the information present in the context.

If the answer is not available in the context, reply exactly:

"I couldn't find this information in the provided document."

Context:
{context}

Question:
{question}

Answer:
"""

    # --------------------------------------
    # Gemini
    # --------------------------------------

    answer = generate_answer(prompt)

    return answer