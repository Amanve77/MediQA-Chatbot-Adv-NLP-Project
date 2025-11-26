"""
Biomedical entailment using a MedNLI-tuned sequence classification model.

Uses a model like 'pritamdeka/PubMedBERT-MNLI-MedNLI' (example). Adjust model_id if you prefer another.
"""
from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch
from typing import List, Tuple
import numpy as np

DEFAULT_NLI = "pritamdeka/PubMedBERT-MNLI-MedNLI"

_nli_tokenizer = None
_nli_model = None
_label_map = None

def load_entailment_model(model_id: str = DEFAULT_NLI, device: str = None):
    global _nli_tokenizer, _nli_model, _label_map
    if device is None:
        device = "cuda" if torch.cuda.is_available() else "cpu"
    if _nli_tokenizer is None:
        _nli_tokenizer = AutoTokenizer.from_pretrained(model_id)
    if _nli_model is None:
        _nli_model = AutoModelForSequenceClassification.from_pretrained(model_id).to(device)
        cfg = _nli_model.config
        id2label = getattr(cfg, "id2label", None)
        if id2label:
            _label_map = {v.lower(): int(k) for k, v in id2label.items()}
        else:
            _label_map = {"contradiction": 0, "neutral": 1, "entailment": 2}
    return _nli_tokenizer, _nli_model, _label_map

def _chunk_texts(texts: List[str], max_chars: int = 1500):
    out = []
    for t in texts:
        if len(t) <= max_chars:
            out.append(t)
        else:
            for i in range(0, len(t), max_chars):
                out.append(t[i:i+max_chars])
    return out

def entailment_check(hypotheses: List[str], retrieved_texts: List[str],
                     model_id: str = DEFAULT_NLI, device: str = None,
                     entailment_threshold: float = 0.6) -> Tuple[float, List[dict]]:
    """
    For each hypothesis sentence, check across retrieved_text chunks for best entailment prob.
    Returns:
      entailment_pct: fraction of hypothesis sentences with entail_prob >= entailment_threshold
      details: list of {hypothesis, best_entail_p, best_premise_idx}
    """
    tokenizer, model, label_map = load_entailment_model(model_id, device)
    if device is None:
        device = "cuda" if torch.cuda.is_available() else "cpu"

    retrieved_chunks = _chunk_texts(retrieved_texts, max_chars=1500)
    details = []
    entailed_count = 0

    for hyp in hypotheses:
        best_p = 0.0
        best_idx = None
        for idx, premise in enumerate(retrieved_chunks):
            enc = tokenizer(premise, hyp, truncation='only_first', padding='max_length', max_length=512, return_tensors="pt").to(device)
            with torch.no_grad():
                out = model(**enc)
                probs = torch.softmax(out.logits, dim=-1).cpu().numpy()[0]
            entail_idx = label_map.get("entailment", 2)
            entail_p = float(probs[entail_idx])
            if entail_p > best_p:
                best_p = entail_p
                best_idx = idx
        details.append({"hypothesis": hyp, "best_entail_p": best_p, "best_premise_idx": best_idx})
        if best_p >= entailment_threshold:
            entailed_count += 1

    entailment_pct = entailed_count / max(1, len(hypotheses))
    return entailment_pct, details
