import faiss
import numpy as np


def create_index(embedding_dimension):
    """
    Creates a FAISS index for vector search.
    """

    print(f"Creating FAISS index (dimension = {embedding_dimension})...")

    index = faiss.IndexFlatL2(embedding_dimension)

    print("FAISS index created successfully.\n")

    return index


def add_embeddings(index, embedding_matrix):
    """
    Adds embedding vectors to the FAISS index.
    """

    print(f"Adding {len(embedding_matrix)} embeddings to the index...")

    index.add(np.asarray(embedding_matrix, dtype=np.float32))

    print("Embeddings added successfully.\n")


def search(index, question_embedding, k=3):
    """
    Searches the FAISS index for the most similar vectors.

    Args:
        index: FAISS index
        question_embedding: User question embedding
        k: Number of nearest neighbours

    Returns:
        distances, indices
    """

    distances, indices = index.search(
        np.asarray(question_embedding, dtype=np.float32),
        k
    )

    return distances, indices