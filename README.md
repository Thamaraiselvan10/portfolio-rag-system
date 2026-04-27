# Ask Your Portfolio — AI/ML Intern Assignment (BYLD Wealth)

## Overview

**Ask Your Portfolio** is a Python CLI tool that enables users to query their investment portfolio using natural language.

The system combines:

* Retrieval-Augmented Generation (RAG)
* Structured outputs (Pydantic)
* Deterministic validation

to produce **grounded, reliable, and auditable responses**.

This project focuses on:

* Retrieval quality
* Structured outputs
* Validation of LLM outputs
* Evaluation-driven development

---

## Key Features

### 1. CLI Interface

```bash
python -m portfolio_ask "Which stock has highest investment value?"
```

---

### 2. Retrieval-Augmented Generation (RAG)

* Uses MiniLM embeddings
* Vector search with FAISS
* Retrieves relevant portfolio/news context before answering

---

### 3. Structured Output (Pydantic)

Example:

```json
{
  "answer": "TCS has the highest investment value of 152000 INR.",
  "stock": "TCS",
  "value": 152000
}
```

✔ No regex parsing
✔ Schema-enforced

---

### 4. Citation System

```json
"sources": ["portfolio.json"]
```

Ensures traceability of answers.

---

### 5. Deterministic Validation (Variant A)

Every numeric value is validated against retrieved context.

```json
"validation": {
  "status": "VERIFIED"
}
```

If mismatch:

```json
"status": "UNVERIFIED"
```

---

### 6. Hybrid System Design

* **Python (deterministic)** → calculations, comparisons
* **LLM (Ollama)** → explanation, reasoning

This prevents numeric hallucinations.

---

### 7. Evaluation Harness

```bash
python -m tests.eval
```

* Uses `evals/cases.yaml`
* Outputs PASS / FAIL

---

## Project Structure

```
portfolio-rag-system/
│
├── portfolio_ask/
├── data/
│   ├── portfolio.json
│   ├── news/
│   └── glossary.md
│
├── evals/
│   └── cases.yaml
│
├── tests/
│   └── eval.py
│
├── Makefile
├── requirements.txt
├── README.md
├── AI_LOG.md
└── .env.example
```

---

## Installation

### 1. Create virtual environment

```bash
python -m venv venv
```

### 2. Install dependencies

```bash
venv\Scripts\pip install -r requirements.txt
```

---

## 🔥 Ollama Setup (Required)

This project uses **Ollama** to run the LLM locally.

### 1. Install Ollama

https://ollama.com/download

---

### 2. Start Ollama

```bash
ollama serve
```

---

### 3. Pull model

```bash
ollama pull llama3
```

---

### 4. Verify

```bash
ollama list
```

---

### 5. API Endpoint

```text
http://localhost:11434
```

Ensure Ollama is running before queries.

---

## Running the System

```bash
python -m portfolio_ask "What is my IT exposure?"
```

---

## Example Output

```
Answer: TCS has the highest investment value of 152000 INR.

Structured:
{
  "stock": "TCS",
  "value": 152000
}

Validation:
VERIFIED
```

---

## Evaluation

```bash
python -m tests.eval
```

Output:

```
PASS / FAIL
```

---

## Makefile (Optional)

```bash
make setup
make run
make eval
```

⚠ On Windows, use direct Python commands.

---

## Architecture

```
Query
 → Retrieval (FAISS)
 → Smart Routing
 → LLM (Ollama)
 → Structured Output
 → Validation
 → Response
```

---

## Technologies Used

* Python 3.11+
* Ollama (Llama3)
* sentence-transformers
* FAISS
* Pydantic
* NumPy

---

## Key Technical Contributions

* Deterministic numeric validation
* Structured output enforcement
* Hybrid architecture (LLM + code)
* Evaluation harness (YAML-based)
* Smart routing system
* Clean dependency management

---

## Failure Modes

* Retrieval mismatch
* Sector mapping limitations
* News relevance heuristics
* LLM formatting inconsistencies

---

## Future Improvements

* Real-time stock APIs
* Better ranking for news
* UI (Streamlit / React)
* Advanced evaluation metrics

---

## Reproducibility

```bash
pip install -r requirements.txt
python -m portfolio_ask "query"
python -m tests.eval
```

---

## AI Usage

See `AI_LOG.md` for:

* prompts
* decisions
* rejected approaches

---

## Submission Checklist

✔ CLI
✔ RAG
✔ Structured Output
✔ Validation
✔ Eval Harness
✔ README
✔ AI_LOG

---

## Author

**Thamarai Selvan**
