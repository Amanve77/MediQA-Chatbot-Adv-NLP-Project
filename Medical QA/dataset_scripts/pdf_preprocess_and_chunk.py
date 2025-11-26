"""
pdf_preprocess_and_chunk.py

This script:
1. Loads multiple medical PDFs (your 4 books)
2. Skips unwanted front/back pages
3. Removes:
   - headers/footers
   - watermarks
   - website names
   - table artifacts
   - figure labels
   - page numbers
   - indexes/references
4. Merges broken lines
5. Creates clean text chunks
6. Saves chunks into rag_data/chunks/*.jsonl

NO embeddings or FAISS here!
"""

import os
import re
import json
from glob import glob
import pdfplumber
from tqdm import tqdm

# -------------------------------------------------------
# CONFIG
# -------------------------------------------------------

OUTPUT_DIR = "../rag/chunks"
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Book paths (replace with your actual paths)
PDFS = [
    {
        "path": r"C:\Users\amanv\Downloads\Adv. NLP\Medical Wellness Assistant\Medical QA\datasets\raw\Rag\Ramdas Nayak Pathology Book.pdf",
        "name": "Ramdas_Nayak_Pathology",
        "skip_first": 27,
        "skip_last": 41,
    },
    {
        "path": r"C:\Users\amanv\Downloads\Adv. NLP\Medical Wellness Assistant\Medical QA\datasets\raw\Rag\The-Gale-Encyclopedia-of-Medicine-3rd-Edition-staibabussalamsula.ac_.id_.pdf",
        "name": "Gale Encyclopedia of Medicine",
        "skip_first": 30,
        "skip_last": 440,
    },
    {
        "path": r"C:\Users\amanv\Downloads\Adv. NLP\Medical Wellness Assistant\Medical QA\datasets\raw\Rag\8205Oxford Handbook of Clinical Medicine 10th 2017 Edition_SamanSarKo.pdf",
        "name": "Oxford_Handbook",
        "skip_first": 14,
        "skip_last": 47,
    },
    {
        "path": r"C:\Users\amanv\Downloads\Adv. NLP\Medical Wellness Assistant\Medical QA\datasets\raw\Rag\KD-Tripathi-Pharmacology-Book.pdf",
        "name": "Tripathi_Pharmacology",
        "skip_first": 17,
        "skip_last": 76,
    }
]

# Chunk settings
CHUNK_WORDS = 250
CHUNK_OVERLAP = 25


# -------------------------------------------------------
# CLEANING FUNCTIONS
# -------------------------------------------------------

HEADER_FOOTER_PATTERNS = [
    r"OXFORD HANDBOOK.*",
    r"Downloaded\sfrom.*",
    r"Tripathi.*Pharmacology.*",
    r"Oxford.*Press.*",
    r"Page\s*\d+",
    r"www\..*",
    r"[A-Za-z ]+Edition.*",
]

TABLE_DETECTION = r"\s{4,}"             # multiple spaces = table-like
FIGURE_PATTERNS = r"^(Fig|Figure|Plate|Table)\s*\d+"

STOP_SECTIONS = [
    "REFERENCES",
    "References",
    "Bibliography"
]


def clean_line(line: str) -> str:
    """Remove headers, footers, tables, figure labels, watermarks."""
    if not line or not isinstance(line, str):
        return ""

    # Remove headers/footers
    for pat in HEADER_FOOTER_PATTERNS:
        if re.search(pat, line, re.IGNORECASE):
            return ""

    # Remove figure/table labels
    if re.match(FIGURE_PATTERNS, line.strip()):
        return ""

    # Remove multi-space table rows
    if re.search(TABLE_DETECTION, line):
        return ""

    return line.strip()


def clean_page_text(text: str) -> str:
    if not text:
        return ""

    lines = text.split("\n")
    cleaned = []

    for line in lines:
        cl = clean_line(line)
        if cl:
            cleaned.append(cl)

    merged = " ".join(cleaned)
    merged = re.sub(r"\s+", " ", merged).strip()

    return merged


def stop_section_reached(text: str) -> bool:
    """Stop processing when reference/index pages appear."""
    for s in STOP_SECTIONS:
        if s.lower() in text.lower()[:100]:
            return True
    return False


def chunk_text(words, chunk_size, overlap):
    """Chunk words with overlap."""
    chunks = []
    step = chunk_size - overlap

    for i in range(0, len(words), step):
        chunk = words[i:i+chunk_size]
        if len(chunk) > 20:  # ignore trivial chunks
            chunks.append(" ".join(chunk))
    return chunks


# -------------------------------------------------------
# MAIN EXTRACTION LOOP
# -------------------------------------------------------

all_chunks_meta = []

for book in PDFS:
    pdf_path = book["path"]
    name = book["name"]
    skip_first = book["skip_first"]
    skip_last = book["skip_last"]

    if not os.path.exists(pdf_path):
        print(f"[WARN] Missing PDF: {pdf_path}")
        continue

    print(f"\nProcessing: {name}")

    chunks_file = os.path.join(OUTPUT_DIR, f"{name}.jsonl")

    with pdfplumber.open(pdf_path) as pdf, open(chunks_file, "w", encoding="utf-8") as out:
        total_pages = len(pdf.pages)
        start = skip_first
        end = total_pages - skip_last

        for p in tqdm(range(start, end), desc=f"{name} pages"):
            raw = pdf.pages[p].extract_text()
            if not raw:
                continue

            cleaned = clean_page_text(raw)
            if len(cleaned) < 200:
                continue

            if stop_section_reached(cleaned):
                break

            words = cleaned.split()
            chunks = chunk_text(words, CHUNK_WORDS, CHUNK_OVERLAP)

            for c in chunks:
                record = {
                    "book": name,
                    "page": p + 1,
                    "text": c
                }
                out.write(json.dumps(record, ensure_ascii=False) + "\n")
                all_chunks_meta.append(record)

print("\nCompleted clean chunk generation.")
print(f"Files saved in: {OUTPUT_DIR}")
print(f"Total chunks generated: {len(all_chunks_meta)}")
