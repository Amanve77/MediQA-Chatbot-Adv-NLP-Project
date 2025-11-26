from rag.rag_query_engine import RAG
from safety_scripts.safety_pipeline import safety_check_and_answer
from inference_scripts.mistral_inference import mistral_generate_with_meta

GENERATOR = "mistral"

rag = RAG()

def build_prompt_for_generator(query, retrieved):
    context = "\n\n".join([
        f"[Source: {r.get('book')}, Page: {r.get('page')}]\n{r.get('preview', '')}"
        for r in retrieved
    ])

    return f"""
You are a medical assistant. Use ONLY the context below to answer the user's question.
If the context does not support a safe answer, say:
"I don't have enough medical information to answer that safely."

User Query:
{query}

Context:
{context}

Answer:
"""

def generator_fn_mistral(prompt, seed=0, temperature=0.0, return_generate_obj=False):
    return mistral_generate_with_meta(prompt, seed=seed, temperature=temperature, return_generate_obj=False)

def ask(query):
    retrieved = rag.retrieve(query, k=5)

    decision = safety_check_and_answer(
        query, retrieved,
        build_prompt_for_generator,
        generator_fn_mistral,
        thresholds=None,
        n_consistency=2,
        nli_model_id="pritamdeka/PubMedBERT-MNLI-MedNLI"
    )

    if decision["status"] == "accept":
        return decision

    return {
        "status": "abstain",
        "answer": "I’m not confident enough to answer safely.",
        "meta": decision.get("meta", {})
    }
