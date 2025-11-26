"""
rag_query_engine.py

Purpose:
- Load FAISS index and embeddings
- Load metadata (index_map.json)
- Create a retrieval function for top-k relevant chunks
- Build a final RAG prompt for your generator model
- Provide a generate_answer() stub to integrate GPT model

Use:
from rag_query_engine import RAG

rag = RAG()
rag.ask("What are the symptoms of asthma?")
"""

import json
import numpy as np
import faiss
from sentence_transformers import SentenceTransformer
import torch

RAG_FOLDER = "rag"
FAISS_INDEX_PATH = r"C:\Users\amanv\Downloads\Adv. NLP\Medical Wellness Assistant\Medical QA\rag\faiss_index.bin"
INDEX_MAP_PATH   = r"C:\Users\amanv\Downloads\Adv. NLP\Medical Wellness Assistant\Medical QA\rag\index_map.json"

EMBED_MODEL = "BAAI/bge-large-en-v1.5"

TOP_K = 5 

class RAG:

    def __init__(self):

        print("Loading embedding model:", EMBED_MODEL)

        if torch.cuda.is_available():
            device = "cuda"
            print("Using GPU:", torch.cuda.get_device_name(0))
        else:
            device = "cpu"
            print("Using CPU")

        self.embedder = SentenceTransformer(EMBED_MODEL, device=device, cache_folder="models/bge/")

        print("Loading FAISS index:", FAISS_INDEX_PATH)
        self.index = faiss.read_index(FAISS_INDEX_PATH)

        print("Loading index map:", INDEX_MAP_PATH)
        with open(INDEX_MAP_PATH, "r", encoding="utf-8") as f:
            self.index_map = json.load(f)

        print("\nRAG Engine initialized successfully!")

    def embed_query(self, query: str):
        """Embed a user query with BGE-large"""

        return self.embedder.encode(
            query,
            convert_to_numpy=True,
            normalize_embeddings=True
        ).astype("float32")

    def retrieve(self, query: str, k: int = TOP_K):
        """Retrieve top-k chunks for the user query with normalized similarity score."""

        q_emb = self.embedder.encode(
            query,
            convert_to_numpy=True,
            normalize_embeddings=True
        ).astype("float32")

        distances, indices = self.index.search(np.array([q_emb]), k)

        results = []

        for raw, idx in zip(distances[0], indices[0]):

            if idx < 0:
                continue

            if isinstance(self.index_map, dict):
                if str(idx) in self.index_map:
                    meta = dict(self.index_map[str(idx)])
                elif idx in self.index_map:
                    meta = dict(self.index_map[idx])
                else:
                    continue
            else:
                if idx >= len(self.index_map):
                    continue
                meta = dict(self.index_map[idx])

            if -1.05 <= raw <= 1.05:
                score = float(raw)

            else:
                score = float(1.0 / (1.0 + raw))

            meta["score"] = score
            results.append(meta)

        return results

    def build_context(self, retrieved_chunks):
        """Combine retrieved chunks into a single context string"""

        context_blocks = []
        for item in retrieved_chunks:
            block = f"[Source: {item['book']}, Page: {item['page']}]\n{item['preview']}"
            context_blocks.append(block)

        return "\n\n".join(context_blocks)

    def build_rag_prompt(self, query, retrieved_chunks):
        """Build a final prompt for your generator model"""

        context = self.build_context(retrieved_chunks)

        prompt = f"""
You are a medical assistant AI. Use ONLY the context below to answer.

Do NOT hallucinate. If information is not found, say "I don't have enough medical information."

User Question:
{query}

Relevant Medical Context:
{context}

Final Answer:
"""
        return prompt

    def ask(self, query):
        """Main function: retrieve and build prompt"""

        print(f"\nUser Query: {query}")

        retrieved = self.retrieve(query, TOP_K)
        print(f"\nTop {TOP_K} retrieved chunks:")

        for r in retrieved:
            print(f"Score: {r['score']:.4f} | {r['book']} | Page {r['page']}")

        prompt = self.build_rag_prompt(query, retrieved)

        print("\n\nGenerated RAG Prompt:\n")
        print(prompt)
        print("\n------ END PROMPT ------")

        print("\n⚠️ WARNING: RAG prompt created. You still need to feed it into your generator model (GPT-2 / LLAMA / OpenAI).")
        print("Use: rag.generate_answer(prompt) when your model is ready.")

        return prompt

    def generate_answer(self, prompt, model=None):
        """
        STUB:
        Add your generator model here.

        Examples:
        - Use your fine-tuned GPT-2 model
        - Use HuggingFace AutoModelForCausalLM
        - Or call OpenAI API

        For now, it only returns the prompt.
        """
        raise NotImplementedError("Add your model here!")

