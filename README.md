# Medical Wellness Assistant - Advanced NLP Project

A sophisticated medical question-answering system that combines Retrieval-Augmented Generation (RAG) with multi-layered safety checks to provide accurate, reliable medical information.

## 📋 Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Architecture](#architecture)
- [Installation](#installation)
- [Dataset Preparation](#dataset-preparation)
- [RAG System Setup](#rag-system-setup)
- [Model Training](#model-training)
- [Running the System](#running-the-system)
- [API Documentation](#api-documentation)
- [Safety Pipeline](#safety-pipeline)
- [Project Structure](#project-structure)
- [Troubleshooting](#troubleshooting)

---

## 🎯 Overview

This project implements an **Advanced NLP-based Medical Wellness Assistant** that:

- **Retrieves** relevant medical information from authoritative textbooks using semantic search
- **Generates** answers using Mistral-7B model (zero-shot with RAG context)
- **Validates** answers through 4 independent safety checks
- **Abstains** from answering when confidence is insufficient

The system prioritizes **safety and accuracy** over answering every question, making it suitable for medical applications.

---

## ✨ Features

### Core Capabilities
- **RAG-based Retrieval**: Semantic search over 4 medical textbooks
- **Zero-Shot LLM**: Mistral-7B used with RAG context for medical domain
- **Multi-layered Safety**: 4 independent validation checks
- **Abstention Mechanism**: Refuses to answer when uncertain
- **Web Interface**: Modern React-based chat UI
- **Session Management**: Maintains conversation context

### Safety Features
1. **Retrieval Confidence Check**: Ensures relevant context is found
2. **Consistency Check**: Verifies model generates stable answers
3. **Model Confidence Check**: Validates token-level certainty
4. **Entailment Verification**: Confirms answer is supported by context

---

## 🏗️ Architecture

### System Flow

```
User Query
    ↓
RAG Retrieval (BGE + FAISS)
    ↓
Safety Check 1: Retrieval Confidence
    ↓
Safety Check 2: Consistency (Multi-generation)
    ↓
Primary Generation (Mistral-7B)
    ↓
Safety Check 3: Model Confidence (Log-probability)
    ↓
Safety Check 4: Entailment (NLI)
    ↓
Accept/Abstain Decision
    ↓
Response to User
```

### Components

1. **Dataset Processing Pipeline**: Merges and cleans medical QA datasets
2. **PDF Processing**: Extracts and chunks medical textbooks
3. **RAG System**: Semantic search with BGE embeddings + FAISS
4. **Safety Pipeline**: Multi-check validation system
5. **Model Inference**: Mistral-7B with log-probability extraction
6. **API Layer**: FastAPI backend + Express.js proxy
7. **Web Frontend**: React-based chat interface

---

## 📦 Installation

### Prerequisites

- **Python 3.8+**
- **Node.js 16+** (for web frontend)
- **CUDA-capable GPU** (recommended, but CPU works)
- **8GB+ RAM** (16GB+ recommended)
- **10GB+ free disk space**

### Step 1: Clone Repository

```bash
git clone <repository-url>
cd "Medical Wellness Assistant"
```

### Step 2: Install Python Dependencies

```bash
cd "Medical QA"
pip install -r requirements.txt
```

**Key Dependencies**:
- `sentence-transformers` (for BGE embeddings)
- `faiss-cpu` or `faiss-gpu` (for vector search)
- `pdfplumber` (for PDF processing)
- `transformers` (for NLI model)
- `llama-cpp-python` (for Mistral inference)
- `fastapi` (for API)
- `peft` (optional, for potential future fine-tuning)

**For GPU support**:
```bash
pip install faiss-gpu
pip install llama-cpp-python --extra-index-url https://abetlen.github.io/llama-cpp-python/whl/cu118
```

### Step 3: Install Node.js Dependencies

```bash
cd ../MediChatUI
npm install
```

### Step 4: Download Models

#### BGE Embedding Model
The model will be automatically downloaded on first use:
```python
# Model: BAAI/bge-large-en-v1.5
# Location: models/bge/
```

#### Mistral-7B Model
Download Mistral-7B-Instruct GGUF format:
```bash
# Download from HuggingFace or other source
# Place in: Medical QA/models/mistral-7b-instruct.gguf
```

#### NLI Model (for Entailment)
The model will be automatically downloaded on first use:
```python
# Model: pritamdeka/PubMedBERT-MNLI-MedNLI
```

---

## 📊 Dataset Preparation

### Step 1: Prepare Raw Datasets

Place your datasets in `datasets/raw/`:

```
datasets/raw/
├── meddialog/
│   ├── english-train.json
│   ├── english-dev.json
│   └── english-test.json
├── medquad/
│   └── MedQuAD.csv
└── pubmedqa/
    └── PubMedQA.csv
```

### Step 2: Merge Datasets

Run the dataset creation notebook:
```bash
cd dataset_scripts
jupyter notebook dataset_creation.ipynb
```

This will:
- Load all raw datasets
- Standardize format
- Merge into `datasets/final_dataset/merged_data.jsonl`

### Step 3: Split Dataset

Run the EDA and split notebook:
```bash
jupyter notebook eda&data_split.ipynb
```

This creates:
- `datasets/processed/train.jsonl` (80%)
- `datasets/processed/val.jsonl` (10%)
- `datasets/processed/test.jsonl` (10%)

### Step 4: Convert to Instruction Format

```bash
python convert_to_instruction.py
```

This creates:
- `datasets/processed/train_inst.jsonl`
- `datasets/processed/val_inst.jsonl`
- `datasets/processed/test_inst.jsonl`

---

## 📚 RAG System Setup

### Step 1: Prepare PDF Books

Place medical PDFs in `datasets/raw/Rag/`:

- `Ramdas Nayak Pathology Book.pdf`
- `The-Gale-Encyclopedia-of-Medicine-3rd-Edition-staibabussalamsula.ac_.id_.pdf`
- `8205Oxford Handbook of Clinical Medicine 10th 2017 Edition_SamanSarKo.pdf`
- `KD-Tripathi-Pharmacology-Book.pdf`

### Step 2: Process PDFs and Create Chunks

**Update paths in script** (`dataset_scripts/pdf_preprocess_and_chunk.py`):

```python
PDFS = [
    {
        "path": r"path/to/Ramdas Nayak Pathology Book.pdf",
        "name": "Ramdas_Nayak_Pathology",
        "skip_first": 27,
        "skip_last": 41,
    },
    # ... other books
]
```

**Run processing**:
```bash
cd dataset_scripts
python pdf_preprocess_and_chunk.py
```

**Output**: Chunks saved to `rag/chunks/*.jsonl`

### Step 3: Build Embeddings and FAISS Index

```bash
cd rag
python embed_and_build_faiss.py
```

This will:
- Load all chunks
- Generate embeddings with BGE-large
- Build FAISS index
- Save `faiss_index.bin`, `embeddings.npy`, `index_map.json`

**Expected time**: 30-60 minutes (depending on chunk count and hardware)

---

## 🎓 Model Usage

### Zero-Shot Inference with Mistral-7B

The system uses **Mistral-7B in zero-shot mode** without fine-tuning. The base model is used directly with RAG-provided medical context to generate answers.

**Model**: `mistralai/Mistral-7B-Instruct-v0.2` (GGUF format)
- **Inference Mode**: Zero-shot (no fine-tuning)
- **Context Source**: RAG retrieval provides medical context
- **Format**: GGUF quantized for efficient inference

**Note on Training Script**: A fine-tuning script (`training_scripts/mistral_finetune_qLoRA.py`) exists in the codebase but was **not used** in this project due to non-availability of GPU resources. The system relies on the base model's instruction-following capabilities combined with RAG context for domain adaptation.

---

## 🚀 Running the System

### Option 1: Full Stack (Recommended)

#### Step 1: Start FastAPI Backend

```bash
cd "Medical QA"
python -m uvicorn api:app --host 127.0.0.1 --port 8000
```

**Expected output**:
```
INFO:     Started server process
INFO:     Uvicorn running on http://127.0.0.1:8000
```

#### Step 2: Start Express Server (Frontend Proxy)

```bash
cd MediChatUI
npm run dev
```

**Expected output**:
```
Server running on http://localhost:5173
```

#### Step 3: Open Web Interface

Open browser: `http://localhost:5173`

### Option 2: API Only (for testing)

```bash
cd "Medical QA"
python -m uvicorn api:app --host 127.0.0.1 --port 8000
```

Test with curl:
```bash
curl -X POST http://127.0.0.1:8000/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "What are the symptoms of flu?", "session_id": null}'
```

### Option 3: Direct Python Usage

```python
from rag.rag_query_engine_safe import ask

result = ask("What are the symptoms of asthma?")
print(result["answer"])
print(result["meta"])  # Safety check metadata
```

---

## 📡 API Documentation

### Base URL
```
http://127.0.0.1:8000
```

### Endpoints

#### 1. Health Check
```http
GET /health
```

**Response**:
```json
{"status": "ok"}
```

#### 2. New Session
```http
POST /new_session
```

**Response**:
```json
{"session_id": "sess_abc123xyz"}
```

#### 3. Chat
```http
POST /chat
Content-Type: application/json
```

**Request Body**:
```json
{
  "session_id": "sess_abc123" | null,
  "message": "What are the symptoms of diabetes?",
  "developer_mode": false,
  "stream": false
}
```

**Response** (Success):
```json
{
  "answer": "Diabetes symptoms include...",
  "meta": {
    "retrieval": {
      "top1": 0.85,
      "mean3": 0.78
    },
    "consistency": {
      "mean_pairwise_sim": 0.82,
      "samples": ["answer1", "answer2"]
    },
    "avg_logprob": -1.8,
    "entailment": {
      "pct": 0.75,
      "details": [...]
    }
  },
  "session_id": "sess_abc123"
}
```

**Response** (Abstain):
```json
{
  "answer": "I'm not confident enough to answer safely.",
  "meta": {
    "retrieval": {...},
    "reason": "Low retrieval confidence (top1=0.45, mean3=0.42)"
  },
  "session_id": "sess_abc123"
}
```

#### 4. Clear Memory
```http
POST /clear_memory
Content-Type: application/json
```

**Request Body**:
```json
{"session_id": "sess_abc123"}
```

**Response**:
```json
{"ok": true}
```

---

## 🛡️ Safety Pipeline

The system performs **4 sequential safety checks**. If any check fails, the system **abstains** from answering.

### Check 1: Retrieval Confidence

**Purpose**: Ensures retrieved chunks are relevant to the query

**Metrics**:
- `top1`: Similarity score of best-matching chunk
- `mean3`: Average similarity of top 3 chunks

**Thresholds** (default):
- `retrieval_top1` ≥ 0.55
- `retrieval_mean3` ≥ 0.50

**Failure**: Returns abstain message

### Check 2: Consistency

**Purpose**: Verifies model generates consistent answers

**Process**:
- Generates 2-3 answers with different random seeds
- Computes pairwise semantic similarity
- Checks if mean similarity ≥ 0.75

**Failure**: Returns abstain message

### Check 3: Model Confidence

**Purpose**: Validates token-level certainty

**Metrics**:
- `avg_logprob`: Average log-probability of generated tokens

**Threshold** (default):
- `avg_logprob` ≥ -2.5

**Failure**: Returns abstain message

### Check 4: Entailment

**Purpose**: Confirms answer is supported by retrieved context

**Model**: `pritamdeka/PubMedBERT-MNLI-MedNLI` (biomedical NLI)

**Process**:
- Splits answer into sentences
- Checks each sentence against retrieved chunks
- Computes entailment percentage

**Threshold** (default):
- `entailment_pct` ≥ 0.60 (60% of sentences must be entailed)

**Failure**: Returns abstain message

### Customizing Thresholds

Edit `safety_scripts/safety_pipeline.py`:

```python
thresholds = {
    "retrieval_top1": 0.60,      # Stricter retrieval
    "retrieval_mean3": 0.55,
    "consistency_sim": 0.80,     # Stricter consistency
    "entailment_pct": 0.70,      # Stricter entailment
    "avg_logprob": -2.0          # Stricter confidence
}

decision = safety_check_and_answer(
    query, retrieved, build_prompt_fn, generator_fn,
    thresholds=thresholds
)
```

---

## 📁 Project Structure

```
Medical QA/
├── dataset_scripts/
│   ├── dataset_creation.ipynb          # Merge raw datasets
│   ├── eda&data_split.ipynb            # EDA and train/val/test split
│   ├── convert_to_instruction.py       # Convert to instruction format
│   └── pdf_preprocess_and_chunk.py    # PDF processing and chunking
│
├── rag/
│   ├── chunks/                         # Processed PDF chunks (JSONL)
│   ├── embed_and_build_faiss.py       # Embedding and FAISS creation
│   ├── rag_query_engine.py             # RAG retrieval engine
│   ├── rag_query_engine_safe.py       # RAG + Safety integration
│   ├── faiss_index.bin                 # FAISS vector index
│   ├── embeddings.npy                  # Chunk embeddings
│   └── index_map.json                  # Metadata mapping
│
├── safety_scripts/
│   ├── safety_pipeline.py              # Main safety orchestration
│   ├── safety_retrieval.py             # Retrieval confidence check
│   ├── safety_consistency.py           # Consistency check
│   ├── safety_entailment.py            # Entailment verification
│   └── safety_logprob.py               # Log-probability computation
│
├── inference_scripts/
│   └── mistral_inference.py            # Mistral-7B inference wrapper
│
├── training_scripts/
│   └── mistral_finetune_qLoRA.py       # Fine-tuning script (not used - zero-shot mode)
│
├── datasets/
│   ├── raw/                            # Raw datasets
│   │   ├── meddialog/
│   │   ├── medquad/
│   │   ├── pubmedqa/
│   │   └── Rag/                        # PDF books
│   ├── processed/                      # Processed splits
│   └── final_dataset/
│       └── merged_data.jsonl           # Merged dataset
│
├── models/
│   ├── bge/                            # BGE embedding model cache
│   ├── mistral_7B/                     # Mistral model files
│   ├── mistral-7b-instruct.gguf       # Mistral GGUF file
│   └── mistral_lora/                   # (Not used - zero-shot mode)
│
├── api.py                              # FastAPI backend
├── requirements.txt                    # Python dependencies
```

---

## 🔧 Troubleshooting

### Issue: FAISS Index Not Found

**Error**: `FileNotFoundError: faiss_index.bin`

**Solution**:
```bash
cd rag
python embed_and_build_faiss.py
```

### Issue: Model Files Not Found

**Error**: `FileNotFoundError: mistral-7b-instruct.gguf`

**Solution**: Download Mistral-7B GGUF from HuggingFace and place in `models/`

### Issue: CUDA Out of Memory

**Error**: `RuntimeError: CUDA out of memory`

**Solutions**:
1. Reduce batch size in `embed_and_build_faiss.py`:
   ```python
   BATCH_SIZE = 2  # Instead of 4
   ```
2. Use CPU for embeddings:
   ```python
   device = "cpu"
   ```
3. Reduce number of GPU layers in `mistral_inference.py`:
   ```python
   n_gpu_layers=20  # Instead of 35
   ```

### Issue: Slow Inference

**Solutions**:
1. Use GPU for Mistral inference
2. Reduce `n_consistency` in safety pipeline (from 3 to 2)
3. Disable entailment check (set `nli_model_id="disable"`)

### Issue: API Connection Error

**Error**: `Error: Unable to connect to the medical assistant backend`

**Solutions**:
1. Ensure FastAPI is running: `python -m uvicorn api:app --host 127.0.0.1 --port 8000`
2. Check `FLASK_API_URL` in `MediChatUI/server/routes.ts`
3. Verify CORS settings in `api.py`

### Issue: Import Errors

**Error**: `ModuleNotFoundError: No module named 'rag'`

**Solution**: Run scripts from project root:
```bash
cd "Medical QA"
python -c "from rag.rag_query_engine_safe import ask"
```

### Issue: PDF Processing Fails

**Error**: `pdfplumber` extraction issues

**Solutions**:
1. Ensure PDFs are text-based (not scanned images)
2. Check PDF paths in `pdf_preprocess_and_chunk.py`
3. Adjust `skip_first` and `skip_last` values for each book

---

## 📊 Performance Benchmarks

### Typical Query Times (GPU)

- **RAG Retrieval**: 50-100ms
- **Mistral Generation**: 2-5 seconds
- **Consistency Check**: 3-6 seconds
- **Entailment Check**: 2-4 seconds
- **Total**: 5-15 seconds per query

### Resource Usage

- **GPU Memory**: ~6-8GB (Mistral + BGE + NLI)
- **CPU Memory**: ~12-16GB
- **Disk Space**: ~15GB (models + data)

---

## 🎓 Academic Context

This project was developed for an **Advanced NLP course**, focusing on:

- **Retrieval-Augmented Generation (RAG)**
- **Safety and Reliability in LLMs**
- **Medical Domain Adaptation**
- **Multi-layered Validation Systems**

---

## 🙏 Acknowledgments

- **BAAI** for BGE embedding models
- **Mistral AI** for Mistral-7B model
- **HuggingFace** for transformers and model hosting
- **Medical Dataset Providers**: MedDialog, MedQuAD, PubMedQA

---

## 🔄 Updates and Maintenance

### Version History
- **v1.0**: Initial release with RAG + 4 safety checks

### Future Improvements
- [ ] Fine-tune Mistral-7B (or similar model) on the processed medical dataset using QLoRA to replace zero-shot inference for better domain adaptation
- [ ] Batch processing for consistency checks
- [ ] Caching of embeddings and retrievals
- [ ] Support for more medical textbooks
- [ ] Real-time streaming responses
- [ ] Multi-language support