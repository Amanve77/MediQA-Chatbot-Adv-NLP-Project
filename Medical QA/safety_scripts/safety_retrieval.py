from typing import List, Dict
import numpy as np

def check_retrieval_confidence(retrieved: List[Dict],
                               top1_thr: float = 0.55,
                               mean3_thr: float = 0.50):
    """
    retrieved: list of dicts with 'score' keys (descending order)
    Returns: (ok:bool, reason:str, metrics:dict)
    """
    if not retrieved:
        return False, "No retrieved context.", {"top1": None, "mean3": None}
    scores = [float(x.get("score", 0.0)) for x in retrieved]
    top1 = scores[0]
    mean3 = float(np.mean(scores[:3])) if len(scores) >= 3 else float(np.mean(scores))
    if top1 < top1_thr or mean3 < mean3_thr:
        reason = f"Low retrieval confidence (top1={top1:.3f}, mean3={mean3:.3f})."
        return False, reason, {"top1": top1, "mean3": mean3}
    return True, "Retrieval confident.", {"top1": top1, "mean3": mean3}
