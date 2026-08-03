from sentence_transformers import SentenceTransformer
import numpy as np

print("Loading embedding model...")

model = SentenceTransformer("all-MiniLM-L6-v2")

print("Embedding model loaded successfully.\n")


def create_embeddings(chunks):
    """
    Generate embeddings for a list of text chunks.

    Args:
        chunks (list): List of text chunks.

    Returns:
        numpy.ndarray: Matrix of embeddings.
    """

    if not chunks:
        raise ValueError("No chunks found.")

    print(f"Generating embeddings for {len(chunks)} chunks...")

    embeddings = model.encode(
        chunks,
        convert_to_numpy=True,
        show_progress_bar=True
    )

    embeddings = np.asarray(embeddings, dtype=np.float32)

    print("Embeddings generated successfully.\n")

    return embeddings