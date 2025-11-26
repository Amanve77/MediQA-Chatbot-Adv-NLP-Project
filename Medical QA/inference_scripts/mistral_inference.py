from llama_cpp import Llama
import numpy as np

MODEL_PATH = r"C:\Users\amanv\Downloads\Adv. NLP\Medical Wellness Assistant\Medical QA\models\mistral-7b-instruct.gguf"

print("Loading Mistral GGUF with logits_all=True...")

llm = Llama(
    model_path=MODEL_PATH,
    n_ctx=4096,
    n_gpu_layers=35,
    n_threads=6,
    logits_all=True,      # <-- REQUIRED
    verbose=False
)


def mistral_generate(prompt, max_tokens=256, temperature=0.2):
    """
    Simple text-only generation (no metadata)
    """
    out = llm.create_completion(
        prompt=prompt,
        max_tokens=max_tokens,
        temperature=temperature,
        top_p=0.9,
        stop=["</s>", "###"]
    )
    return out["choices"][0]["text"].strip()


def mistral_generate_with_meta(prompt, seed=0, temperature=0.2, return_generate_obj=False):
    """
    Full metadata generator compatible with your safety pipeline.
    Returns:
        text: final answer
        generate_obj: HF-style object with sequences + scores
        tokenizer: None
        input_len: length of prompt tokens
    """

    # 1. Run llama-cpp completion with logprobs enabled
    out = llm.create_completion(
        prompt=prompt,
        max_tokens=256,
        temperature=temperature,
        top_p=0.9,
        logprobs=1,            # <-- KEY
        stop=["</s>", "###"]
    )

    choice = out["choices"][0]
    text = choice["text"]
    logprobs = choice["logprobs"]

    # 2. Simulate a HF-style 'generate_obj'
    # sequences = token ids are NOT provided by llama-cpp, so we store tokens instead
    generate_obj = {
        "tokens": logprobs["tokens"],                # ["word1", "word2", ...]
        "token_logprobs": logprobs["token_logprobs"], # [-1.25, -0.35, ...]
        "text_offset": logprobs["text_offset"],
    }

    # 3. Compute avg logprob manually
    # Safety pipeline expects avg_logprob in meta, and we return token_logprobs here
    # The safety module will compute or use this directly.
    avg_logprob = float(np.mean(logprobs["token_logprobs"])) if logprobs["token_logprobs"] else None

    return {
        "text": text.strip(),
        "generate_obj": generate_obj,
        "tokenizer": None,
        "input_len": out["usage"]["prompt_tokens"],
        "avg_logprob": avg_logprob
    }
