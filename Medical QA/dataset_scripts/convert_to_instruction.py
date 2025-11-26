# convert_to_instruction.py
import json

def convert_file(in_path, out_path):
    print("Converting:", in_path)
    with open(in_path, "r", encoding="utf-8") as fin, open(out_path, "w", encoding="utf-8") as fout:
        for line in fin:
            ex = json.loads(line)

            q = ex.get("question", "").strip()
            a = ex.get("answer", "").strip()

            if not q or not a or len(a) < 20:
                continue

            out = {
                "instruction": q,
                "input": "",
                "output": a
            }
            fout.write(json.dumps(out, ensure_ascii=False) + "\n")

    print("Saved:", out_path)


convert_file("../datasets/processed/train.jsonl", "../datasets/processed/train_inst.jsonl")
convert_file("../datasets/processed/val.jsonl", "../datasets/processed/val_inst.jsonl")
convert_file("../datasets/processed/test.jsonl", "../datasets/processed/test_inst.jsonl")

print("DONE")
