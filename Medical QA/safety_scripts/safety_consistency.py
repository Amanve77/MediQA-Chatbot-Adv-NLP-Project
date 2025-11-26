"""
Multi-generation consistency check.
Generates N answers and computes mean pairwise semantic similarity using sentence-transformers.

Function:
 - check_consistency(model_generate_fn, prompt, n=3, sim_thr=0.75)

model_generate_fn(prompt, seed, temperature) -> text
"""
from sentence_transformers import SentenceTransformer, util
import numpy as np

_embedder = None
def _get_embedder():
    global _embedder
    if _embedder is None:
        _embedder = SentenceTransformer("BAAI/bge-large-en-v1.5", cache_folder="models/bge/")
    return _embedder

def check_consistency(model_generate_fn, prompt: str, n: int = 3, sim_thr: float = 0.75, temperature: float = 0.2):
    samples = []
    for i in range(n):
        out = model_generate_fn(prompt, seed=1000 + i, temperature=temperature)
        txt = out if isinstance(out, str) else out.get("text", "")
        samples.append(txt.strip())

    uniq = list(dict.fromkeys(samples))
    if len(uniq) == 1:
        return True, {"samples": samples, "mean_pairwise_sim": 1.0}

    embedder = _get_embedder()
    embs = embedder.encode(samples, convert_to_tensor=True)
    sim_matrix = util.cos_sim(embs, embs).cpu().numpy()

    sims = []
    for i in range(len(samples)):
        for j in range(i+1, len(samples)):
            sims.append(sim_matrix[i,j])
    mean_sim = float(np.mean(sims)) if sims else 1.0
    ok = mean_sim >= sim_thr
    return ok, {"samples": samples, "mean_pairwise_sim": mean_sim}
