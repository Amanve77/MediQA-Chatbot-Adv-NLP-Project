"""
Compute average token log-probability for a HuggingFace generate() output.

Works when model.generate(..., return_dict_in_generate=True, output_scores=True)
returns:
 - sequences (tensor) and scores (list of logits tensors)
"""
import numpy as np
import torch
import math

def compute_avg_logprob_from_generate(generate_output, input_len):
    sequences = generate_output.sequences  
    scores = generate_output.scores        
    if sequences is None or scores is None:
        return None
    token_logps = []

    for i, logits in enumerate(scores):
        if logits.dim() == 2:
            logit = logits[0]
        else:
            logit = logits
        logp = torch.nn.functional.log_softmax(logit, dim=-1)
        token_id = int(sequences[0, input_len + i]) 
        token_logps.append(float(logp[token_id].cpu().numpy()))
    if not token_logps:
        return None
    return float(np.mean(token_logps))

