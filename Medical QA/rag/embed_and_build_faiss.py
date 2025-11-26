"""
embed_and_build_faiss.py

This script:
1. Loads all clean chunk JSONL files from rag_data/chunks/
2. Embeds them using BAAI/bge-large-en-v1.5
3. Builds a FAISS index (cosine similarity via IndexFlatIP)
4. Saves:
   - faiss_index.bin
   - embeddings.npy
   - index_map.json
"""

import os
import json
import numpy as np
import faiss
from tqdm import tqdm
from sentence_transformers import SentenceTransformer

CHUNKS_DIR = "chunks"

FAISS_INDEX_PATH = "faiss_index.bin"
EMBEDDINGS_PATH  = "embeddings.npy"
INDEX_MAP_PATH   = "index_map.json"

EMBED_MODEL = "BAAI/bge-large-en-v1.5"

print("\nLoading chunks from:", CHUNKS_DIR)
chunk_files = [f for f in os.listdir(CHUNKS_DIR) if f.endswith(".jsonl")]

all_chunks = []
all_texts  = []

for cf in chunk_files:
    path = os.path.join(CHUNKS_DIR, cf)
    print(f"Reading: {cf}")

    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            rec = json.loads(line)
            all_chunks.append(rec)
            all_texts.append(rec["text"])

print(f"\nTotal chunks loaded: {len(all_texts)}")

print("\nLoading embedding model:", EMBED_MODEL)

import torch
if torch.cuda.is_available():
    device = "cuda"
    print("Using GPU:", torch.cuda.get_device_name(0))
else:
    device = "cpu"
    print("Using CPU")

embedder = SentenceTransformer(EMBED_MODEL, device=device, cache_folder="models/bge/")

print("\nEmbedding all chunks...")

BATCH_SIZE = 4 if device == "cuda" else 16

embeddings = embedder.encode(
    all_texts,
    batch_size=BATCH_SIZE,
    convert_to_numpy=True,
    normalize_embeddings=True,
    show_progress_bar=True
)

print("Embedding shape:", embeddings.shape)

np.save(EMBEDDINGS_PATH, embeddings)
print("Saved embeddings ->", EMBEDDINGS_PATH)

print("\nBuilding FAISS index...")

dim = embeddings.shape[1]
index = faiss.IndexFlatIP(dim) 
index.add(embeddings.astype("float32"))

faiss.write_index(index, FAISS_INDEX_PATH)

print("FAISS ntotal:", index.ntotal)
print("Saved FAISS index ->", FAISS_INDEX_PATH)

print("\nSaving index map...")

index_map = []
for i, rec in enumerate(all_chunks):
    index_map.append({
        "row": i,
        "book": rec["book"],
        "page": rec["page"],
        "preview": rec["text"][:300]
    })

with open(INDEX_MAP_PATH, "w", encoding="utf-8") as f:
    json.dump(index_map, f, indent=2, ensure_ascii=False)

print("Saved index map ->", INDEX_MAP_PATH)

print("\nRunning quick retrieval test...")

query = "What are the symptoms of asthma?"
q_emb = embedder.encode(query, convert_to_numpy=True, normalize_embeddings=True)

D, I = index.search(np.array([q_emb]).astype("float32"), k=5)

print("\nTop 5 results:")
for score, idx in zip(D[0], I[0]):
    meta = index_map[idx]
    print(f"\nScore: {score:.4f}")
    print("Book:", meta["book"])
    print("Page:", meta["page"])
    print("Text:", meta["preview"])
    print("-" * 60)

print("\nEmbedding + FAISS build completed successfully!")
