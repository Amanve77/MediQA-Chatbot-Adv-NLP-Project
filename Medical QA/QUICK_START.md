# Quick Start Guide

## 🚀 Getting Started in 5 Steps

### Step 1: Install Dependencies

```bash
cd "Medical QA"
pip install -r requirements.txt
```

### Step 2: Update File Paths

**Important**: Update hardcoded paths in these files:

#### `dataset_scripts/pdf_preprocess_and_chunk.py`
```python
PDFS = [
    {
        "path": r"YOUR_PATH/datasets/raw/Rag/Ramdas Nayak Pathology Book.pdf",
        # ... update all paths
    }
]
```

#### `rag/rag_query_engine.py`
```python
FAISS_INDEX_PATH = r"YOUR_PATH/rag/faiss_index.bin"
INDEX_MAP_PATH = r"YOUR_PATH/rag/index_map.json"
```

#### `inference_scripts/mistral_inference.py`
```python
MODEL_PATH = r"YOUR_PATH/models/mistral-7b-instruct.gguf"
```

### Step 3: Prepare Data (One-time Setup)

```bash
# 1. Merge datasets
cd dataset_scripts
jupyter notebook dataset_creation.ipynb

# 2. Split dataset
jupyter notebook eda&data_split.ipynb

# 3. Convert to instruction format
python convert_to_instruction.py

# 4. Process PDFs
python pdf_preprocess_and_chunk.py

# 5. Build RAG index
cd ../rag
python embed_and_build_faiss.py
```

### Step 4: Start the API

```bash
cd "Medical QA"
python -m uvicorn api:app --host 127.0.0.1 --port 8000
```

### Step 5: Test the System

```python
from rag.rag_query_engine_safe import ask

result = ask("What are the symptoms of flu?")
print(result["answer"])
```

## 📝 Notes

- **First run**: Models will be downloaded automatically (may take time)
- **GPU recommended**: For faster inference
- **Zero-shot mode**: System uses base Mistral-7B model without fine-tuning

## 🐛 Common Issues

1. **Path errors**: Update all hardcoded paths (see Step 2)
2. **Missing models**: Download Mistral-7B GGUF file
3. **Memory errors**: Reduce batch sizes or use CPU

For detailed troubleshooting, see [README.md](README.md).

