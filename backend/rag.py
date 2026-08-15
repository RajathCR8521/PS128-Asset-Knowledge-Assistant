from pathlib import Path

from backend.pdf_reader import read_pdf
from backend.embedder import create_embeddings
from backend.vector_store import create_index, add_embeddings, search
from backend.llm import generate_answer


# ============================================================
# CONFIGURATION
# ============================================================

DATA_DIR = Path("data/raw")

CHUNK_SIZE = 500
TOP_K = 5


# ============================================================
# GLOBAL RAG STATE
# ============================================================

index = None

document_chunks = []

document_sources = []


# ============================================================
# TEXT CHUNKING
# ============================================================

def chunk_text(text, chunk_size=CHUNK_SIZE):
    """
    Split extracted document text into smaller chunks.
    """

    if not text:
        return []

    chunks = []

    for start in range(0, len(text), chunk_size):

        chunk = text[start:start + chunk_size].strip()

        if chunk:
            chunks.append(chunk)

    return chunks


# ============================================================
# FIND DOCUMENTS
# ============================================================

def get_pdf_files():
    """
    Find all PDF documents inside data/raw.
    """

    if not DATA_DIR.exists():
        raise FileNotFoundError(
            f"Data directory not found: {DATA_DIR}"
        )

    pdf_files = sorted(DATA_DIR.glob("*.pdf"))

    if not pdf_files:
        raise FileNotFoundError(
            "No PDF documents found in data/raw."
        )

    return pdf_files


# ============================================================
# INITIALIZE RAG
# ============================================================

def initialize_rag():
    """
    Build the RAG knowledge base from all PDFs
    available inside data/raw.
    """

    global index
    global document_chunks
    global document_sources

    print("\n==============================================")
    print(" Initializing PS128 Asset Knowledge Base")
    print("==============================================\n")

    pdf_files = get_pdf_files()

    print(f"Found {len(pdf_files)} PDF documents.\n")

    all_chunks = []
    all_sources = []

    # --------------------------------------------------------
    # Process every PDF
    # --------------------------------------------------------

    for pdf_path in pdf_files:

        print("----------------------------------------------")
        print(f"Processing: {pdf_path.name}")
        print("----------------------------------------------")

        text = read_pdf(pdf_path)

        print(
            f"Extracted {len(text)} characters."
        )

        chunks = chunk_text(text)

        print(
            f"Created {len(chunks)} chunks."
        )

        all_chunks.extend(chunks)

        # Keep track of which document each chunk came from
        all_sources.extend(
            [pdf_path.name] * len(chunks)
        )

        print()

    if not all_chunks:
        raise ValueError(
            "No text chunks were created from the documents."
        )

    # --------------------------------------------------------
    # Generate embeddings
    # --------------------------------------------------------

    print("==============================================")
    print(" Generating Embeddings")
    print("==============================================\n")

    embeddings = create_embeddings(all_chunks)

    print(
        f"Total chunks: {len(all_chunks)}"
    )

    print(
        f"Embedding dimension: {embeddings.shape[1]}"
    )

    # --------------------------------------------------------
    # Create FAISS index
    # --------------------------------------------------------

    print("\n==============================================")
    print(" Creating FAISS Index")
    print("==============================================\n")

    index = create_index(
        embeddings.shape[1]
    )

    add_embeddings(
        index,
        embeddings
    )

    # --------------------------------------------------------
    # Save state
    # --------------------------------------------------------

    document_chunks = all_chunks
    document_sources = all_sources

    print("\n==============================================")
    print(" Knowledge Base Ready")
    print("==============================================")

    print(
        f"Documents indexed: {len(pdf_files)}"
    )

    print(
        f"Total chunks indexed: {len(document_chunks)}"
    )

    print("==============================================\n")

    return {
        "documents": len(pdf_files),
        "chunks": len(document_chunks),
        "embedding_dimension": embeddings.shape[1]
    }


# ============================================================
# ANSWER QUESTION
# ============================================================

def answer_question(question):
    """
    Retrieve relevant information from the knowledge base
    and generate an answer using Gemini.
    """

    global index
    global document_chunks
    global document_sources

    if not question or not question.strip():

        raise ValueError(
            "Question cannot be empty."
        )

    if index is None:

        raise RuntimeError(
            "RAG knowledge base is not initialized. "
            "Call /initialize first."
        )

    print("\n==============================================")
    print(" Processing Question")
    print("==============================================")

    print(
        f"Question: {question}"
    )

    # --------------------------------------------------------
    # Create question embedding
    # --------------------------------------------------------

    query_embedding = create_embeddings(
        [question]
    )

    # --------------------------------------------------------
    # Search FAISS
    # --------------------------------------------------------

    distances, indices = search(
        index,
        query_embedding,
        TOP_K
    )

    retrieved_chunks = []
    retrieved_sources = []

    for idx in indices[0]:

        if 0 <= idx < len(document_chunks):

            retrieved_chunks.append(
                document_chunks[idx]
            )

            retrieved_sources.append(
                document_sources[idx]
            )

    if not retrieved_chunks:

        raise RuntimeError(
            "No relevant information was retrieved."
        )

    print(
        f"Retrieved {len(retrieved_chunks)} chunks."
    )

    # --------------------------------------------------------
    # Build context
    # --------------------------------------------------------

    context_parts = []

    for i, chunk in enumerate(
        retrieved_chunks
    ):

        source = retrieved_sources[i]

        context_parts.append(
            f"""
SOURCE DOCUMENT:
{source}

CONTENT:
{chunk}
"""
        )

    context = "\n\n".join(
        context_parts
    )

    # --------------------------------------------------------
    # Gemini prompt
    # --------------------------------------------------------

    prompt = f"""
You are the Asset Knowledge Assistant for an
Energy & Utilities knowledge base.

Your task is to answer the user's question using
ONLY the retrieved information provided below.

The knowledge base contains technical documents
related to transformers, transformer protection,
maintenance, operation, and power-system equipment.

IMPORTANT RULES:

1. Use the retrieved documents as the primary source.
2. Do not invent technical facts.
3. If the retrieved information does not contain
   enough information to answer the question,
   clearly say that the information was not found
   in the provided knowledge base.
4. Give a concise and technically clear answer.
5. Mention the relevant source document names when
   appropriate.

RETRIEVED KNOWLEDGE
===================

{context}

USER QUESTION
=============

{question}

ANSWER
======
"""

    # --------------------------------------------------------
    # Generate answer
    # --------------------------------------------------------

    answer = generate_answer(
        prompt
    )

    return {
        "answer": answer,
        "sources": list(
            dict.fromkeys(
                retrieved_sources
            )
        )
    }