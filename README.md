# Ask Your Portfolio — AI/ML Intern Assignment (BYLD Wealth)

## Overview

**Ask Your Portfolio** is a Python CLI tool that allows a user to query their investment portfolio using natural language.
It combines **Retrieval-Augmented Generation (RAG)**, **structured outputs**, and a **strict validation layer** to produce grounded, reliable answers with citations.

This system is designed not as a chatbot demo, but as a **disciplined AI system** focusing on:

* Retrieval quality
* Structured outputs (Pydantic)
* Evaluation and validation
* Failure handling

---

## Key Features

### 1. CLI Interface

Run queries directly:

```bash
python -m portfolio_ask "Which stock has highest investment value?"
```

---

### 2. Retrieval-Augmented Generation (RAG)

* Embeds portfolio + news data
* Uses vector similarity (FAISS)
* Retrieves relevant context before answering

---

### 3. Structured Output (Pydantic)

Certain queries return structured JSON instead of plain text:

```json
{
  "answer": "TCS has the highest investment value of 152000 INR.",
  "stock": "TCS",
  "value": 152000
}
```

✔ No regex parsing
✔ Schema-enforced outputs

---

### 4. Citation System

Each response includes:

```json
"sources": ["portfolio.json"]
```

Ensures traceability to input data.

---

### 5. Variant A — Citation Validator (Implemented)

Every numeric claim is validated against context.

Example:

```json
"validation": {
  "status": "VERIFIED",
  "reason": "All numbers found in context"
}
```

If mismatch:

```json
"status": "UNVERIFIED"
```

---

### 6. Smart Query Routing

Different query types handled differently:

* Portfolio calculations → computed metrics
* News queries → filtered news
* General queries → retriever

---

### 7. Evaluation Harness

Test system reliability using:

```bash
python -m tests.eval
```

Uses:

```
evals/cases.yaml
```

Outputs:

```
PASS / FAIL per test case
```

---

## Project Structure

```
portfolio-ask/
│
├── portfolio_ask/        # Core system
│   ├── data_pipeline/
│   ├── retrieval/
│   ├── llm/
│   ├── validator/
│   ├── utils/
│   └── main.py
│
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

## Data Design

### portfolio.json

* 15 holdings
* Includes:

  * sector
  * quantity
  * avg_cost
  * current_price

### news/

* 20+ market news snippets
* Includes both relevant and irrelevant news

### glossary.md

* 15+ financial terms
* Helps LLM grounding

---

## Installation

### 1. Create environment

```bash
python -m venv venv
```

### 2. Install dependencies

```bash
venv\Scripts\pip install -r requirements.txt
```

---

## Running the System

### Run query

```bash
python -m portfolio_ask "What is my IT exposure?"
```

---

### Run evaluation

```bash
python -m tests.eval
```

---

## Makefile (Optional)

Commands provided:

```bash
make setup
make run
make eval
```

⚠ Note: On Windows, `make` may not be available.
Use direct Python commands instead.

---

## Technical Design

### Pipeline

```
Query
 → Retrieval (FAISS)
 → Smart Routing
 → LLM (Ollama - Llama3.2)
 → Structured Output (Pydantic)
 → Validation Layer
 → Final Response
```

---

### Technologies Used

* Python 3.11+
* Ollama (Llama 3.2)
* sentence-transformers
* FAISS
* Pydantic
* NumPy

---

## Key Technical Improvements (Your Work)

* Implemented **structured output enforcement**
* Built **custom citation validator**
* Added **numeric normalization (comma handling)**
* Designed **smart routing system**
* Removed LLM hallucinations via validation
* Cleaned dependency management
* Implemented **evaluation harness with YAML-based tests**
* Added **deep null-field cleaning in outputs**

---

## Failure Modes

The system may fail in:

1. **Retrieval mismatch**

   * Relevant context not retrieved

2. **Derived values vs raw context**

   * Fixed via enriched context validation

3. **LLM hallucination**

   * Reduced using validator

4. **Sector mapping errors**

   * If mapping is incomplete

---

## What I’d Do With 2 More Days

* Add real-time stock API integration
* Improve ranking for news impact
* Add UI (React / Streamlit)
* Add caching for embeddings
* Improve evaluation metrics (precision/recall)

---

## Reproducibility

A reviewer can:

1. Clone repo
2. Install dependencies
3. Run:

```bash
python -m portfolio_ask "query"
```

---

## Security

* No API keys committed
* Uses `.env` (ignored)
* `.env.example` provided

---

## AI Usage

See `AI_LOG.md` for:

* prompts used
* design decisions
* debugging process

---

## Conclusion

This project demonstrates:

* Practical RAG implementation
* Structured AI output design
* Validation against hallucinations
* Evaluation-driven development

---

## Submission Checklist

✔ CLI working
✔ RAG implemented
✔ Structured outputs
✔ Citation validation
✔ Eval harness
✔ Makefile
✔ AI_LOG.md
✔ README

---

## Author

Thamarai Selvan
