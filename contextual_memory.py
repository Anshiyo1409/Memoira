# contextual_memory.py
import sqlite3

try:
    import numpy as np
except ImportError:
    print("Warning: numpy not installed. Install it with: pip install numpy")
    np = None

try:
    from sentence_transformers import SentenceTransformer
    model = SentenceTransformer("all-MiniLM-L6-v2")
except ImportError:
    print("Warning: sentence_transformers not installed. Install it with: pip install sentence-transformers")
    SentenceTransformer = None
    model = None

DB_PATH = "data/memory.db"

# Fetch all memory texts from DB
def fetch_all_memories():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT content FROM memories")
    rows = c.fetchall()
    conn.close()
    return [r[0] for r in rows]

# Find related memories based on semantic similarity
def find_related_memories(user_text, threshold=0.55, top_k=3):
    memories = fetch_all_memories()
    if not memories:
        return []

    memory_embeddings = model.encode(memories)
    user_embedding = model.encode([user_text])[0]

    similarities = []
    for i, emb in enumerate(memory_embeddings):
        # Cosine similarity
        sim = np.dot(user_embedding, emb) / (np.linalg.norm(user_embedding) * np.linalg.norm(emb))
        if sim > threshold:
            similarities.append((memories[i], sim))

    # Sort by similarity descending
    similarities.sort(key=lambda x: x[1], reverse=True)
    # Return top_k memories
    return [m[0] for m in similarities[:top_k]]