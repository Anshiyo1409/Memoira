# memory_brain.py
from sentence_transformers import SentenceTransformer
import faiss
import numpy as np
import sqlite3
import os

DB_PATH = "data/memory.db"
INDEX_PATH = "data/memory_index.faiss"

# Load embedding model
model = SentenceTransformer("all-MiniLM-L6-v2")

# Load all memories from DB
def load_memories():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT id, content FROM memories")
    rows = c.fetchall()
    conn.close()
    return rows

# Build FAISS index for semantic search
def build_index():
    memories = load_memories()
    if not memories:
        return None

    texts = [m[1] for m in memories]
    embeddings = model.encode(texts)

    dimension = embeddings.shape[1]
    index = faiss.IndexFlatL2(dimension)
    index.add(np.array(embeddings))

    # Save index
    faiss.write_index(index, INDEX_PATH)
    return index, memories

# Search similar memories semantically
def search_memory(query, k=3):
    if not os.path.exists(INDEX_PATH):
        build_index()

    index = faiss.read_index(INDEX_PATH)
    memories = load_memories()
    texts = [m[1] for m in memories]

    query_embedding = model.encode([query])
    distances, indices = index.search(np.array(query_embedding), k)

    results = [texts[i] for i in indices[0]]
    return results