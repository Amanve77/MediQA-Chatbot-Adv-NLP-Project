from safety_scripts.safety_retrieval import check_retrieval_confidence
from safety_scripts.safety_consistency import check_consistency
from safety_scripts.safety_entailment import entailment_check, load_entailment_model
from safety_scripts.safety_logprob import compute_avg_logprob_from_generate
import nltk
nltk.download('punkt', quiet=True)
from nltk import sent_tokenize

DEFAULTS = {
    "retrieval_top1": 0.55,
    "retrieval_mean3": 0.50,
    "consistency_sim": 0.75,
    "entailment_pct": 0.60,
    "avg_logprob": -2.5
}

def safety_check_and_answer(query: str,
                            retrieved: list,
                            build_prompt_fn,
                            generator_fn,
                            thresholds: dict = None,
                            n_consistency: int = 3,
                            nli_model_id: str = None):
    """
    build_prompt_fn(query, retrieved) -> prompt string
    generator_fn(prompt, seed=..., temperature=..., return_generate_obj=bool) -> dict { "text":..., "generate_obj":..., "tokenizer":... }
    """
    thr = DEFAULTS.copy()
    if thresholds:
        thr.update(thresholds)

    ok, reason, metrics = check_retrieval_confidence(retrieved, top1_thr=thr["retrieval_top1"], mean3_thr=thr["retrieval_mean3"])
    meta = {"retrieval": metrics}
    if not ok:
        return {"status": "abstain", "reason": reason, "meta": meta}

    prompt = build_prompt_fn(query, retrieved)

    def _gen_text(p, seed, temperature=0.2):
        out = generator_fn(p, seed=seed, temperature=temperature, return_generate_obj=False)
        return out["text"]

    cons_ok, cons_meta = check_consistency(_gen_text, prompt, n=n_consistency, sim_thr=thr["consistency_sim"], temperature=0.2)
    meta["consistency"] = cons_meta
    if not cons_ok:
        return {"status": "abstain", "reason": "Inconsistent generations (low self-consistency).", "meta": meta}

    main_out = generator_fn(prompt, seed=0, temperature=0.0, return_generate_obj=True)
    text = main_out["text"]
    gen_obj = main_out.get("generate_obj", None)
    avg_logp = None
    if gen_obj is not None:
        try:
            avg_logp = main_out.get("avg_logprob")
        except Exception:
            avg_logp = None
    meta["avg_logprob"] = avg_logp
    if avg_logp is not None and avg_logp < thr["avg_logprob"]:
        return {"status": "abstain", "reason": f"Low model confidence (avg_logprob={avg_logp:.3f}).", "meta": meta}

    if nli_model_id == "disable":
        meta["entailment"] = {"pct": None, "details": "disabled"}
        return {"status": "accept", "answer": text, "meta": meta}

    sentences = sent_tokenize(text)
    sentences = [s for s in sentences if len(s.split()) >= 3]
    retrieved_texts = [r["text"] if "text" in r else r.get("preview", "") for r in retrieved]

    entail_pct, entail_details = entailment_check(
        sentences,
        retrieved_texts,
        model_id=nli_model_id if nli_model_id else None
    )

    meta["entailment"] = {"pct": entail_pct, "details": entail_details}
    if entail_pct < thr["entailment_pct"]:
        return {"status": "abstain", "reason": f"Insufficient evidence in retrieved docs (entailment_pct={entail_pct:.2f}).", "meta": meta}

    return {"status": "accept", "answer": text, "meta": meta}
