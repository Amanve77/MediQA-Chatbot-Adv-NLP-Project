import os
import torch
from datasets import load_dataset
from transformers import AutoTokenizer, AutoModelForCausalLM, AutoConfig, Trainer, TrainingArguments, DataCollatorForLanguageModeling
from peft import LoraConfig, get_peft_model, prepare_model_for_kbit_training
import bitsandbytes as bnb

MODEL_NAME = "mistralai/Mistral-7B-Instruct-v0.2"

TRAIN_PATH = "datasets/processed/train_inst.jsonl"
VAL_PATH   = "datasets/processed/val_inst.jsonl"

OUT_DIR = "models/mistral_lora"
MAX_LEN = 1024

BATCH = 1
GRAD_ACCUM = 8
LR = 2e-4
EPOCHS = 2

tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME, use_fast=False)
tokenizer.pad_token = tokenizer.eos_token

def make_prompt(example):
    instr = example["instruction"]
    out   = example["output"]
    prompt = f"### Instruction:\n{instr}\n\n### Response:\n{out}{tokenizer.eos_token}"
    return {"text": prompt}

ds = load_dataset("json", data_files={"train": TRAIN_PATH, "val": VAL_PATH})

ds = ds.map(make_prompt)
ds = ds.map(lambda batch: tokenizer(batch["text"], truncation=True, max_length=MAX_LEN, padding="max_length"), batched=True)
ds.set_format(type="torch", columns=["input_ids", "attention_mask"])

bnb_config = {
    "load_in_4bit": True,
    "bnb_4bit_quant_type": "nf4",
    "bnb_4bit_use_double_quant": True,
    "bnb_4bit_compute_dtype": torch.bfloat16 if torch.cuda.is_available() else torch.float16
}

model = AutoModelForCausalLM.from_pretrained(
    MODEL_NAME,
    device_map="auto",
    trust_remote_code=True,
    **bnb_config
)

model = prepare_model_for_kbit_training(model)

lora = LoraConfig(
    r=16,
    lora_alpha=32,
    target_modules=["q_proj", "v_proj"],
    lora_dropout=0.05,
    task_type="CAUSAL_LM"
)

model = get_peft_model(model, lora)

args = TrainingArguments(
    output_dir=OUT_DIR,
    per_device_train_batch_size=BATCH,
    per_device_eval_batch_size=1,
    gradient_accumulation_steps=GRAD_ACCUM,
    eval_steps=1500,
    logging_steps=200,
    save_steps=2000,
    learning_rate=LR,
    warmup_ratio=0.05,
    num_train_epochs=EPOCHS,
    fp16=True,
    save_total_limit=3,
    evaluation_strategy="steps",
)

data_collator = DataCollatorForLanguageModeling(tokenizer, mlm=False)

trainer = Trainer(
    model=model,
    args=args,
    train_dataset=ds["train"],
    eval_dataset=ds["val"],
    data_collator=data_collator,
)

trainer.train()
model.save_pretrained(OUT_DIR)
print("Training complete.")
