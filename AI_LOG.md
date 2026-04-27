# AI_LOG.md

## AI Usage Overview

**Tool Used:** ChatGPT (GPT-4 / Pro)

AI was used as a **design assistant and debugging partner**, not as an authoritative source.
All critical components were **validated, modified, or redesigned manually** to meet assignment requirements.

---

## 1. System Design

### Prompt

"Validate my workflow: CLI → Retriever (MiniLM + FAISS) → LLM (Ollama) → Validator → Output. Suggest improvements."

---

### AI Suggestion

* Standard RAG pipeline
* Retrieval → LLM → output flow
* No strict validation layer by default

---

### My Decision

Accepted the core pipeline, but **extended it significantly**:

* Added **smart routing** (portfolio vs news vs general queries)
* Introduced **structured outputs using Pydantic**
* Designed a **separate validation layer**

---

### Reasoning

The assignment emphasizes:

* grounding
* validation
* evaluation

A basic RAG pipeline is insufficient without enforcing correctness.

---

## 2. Hybrid System Design (Critical Architectural Decision)

### Prompt

"Should all portfolio queries be handled purely by the LLM, or should some logic be computed programmatically?"

---

### AI Suggestion

* Use LLM for all queries, including calculations and comparisons

---

### What I Rejected

**Full LLM-based computation**

**Why I rejected it:**

* LLMs are **not reliable for numerical computation**
* Observed issues:

  * incorrect totals (e.g., wrong IT exposure)
  * inconsistent results across runs
* No guarantee of **deterministic output**
* Violates requirement for **financial correctness**

---

### Final Approach — Hybrid System

I implemented a **hybrid architecture combining deterministic logic and LLM reasoning**:

#### 1. Deterministic Layer (Python)

Used for:

* portfolio calculations (total, exposure)
* comparisons (highest, lowest)
* sector aggregation

✔ Guarantees correctness
✔ Fully auditable
✔ No hallucination

---

#### 2. LLM Layer (Ollama)

Used for:

* explanation
* summarization
* news interpretation

✔ Handles natural language reasoning
✔ Improves usability

---

#### 3. Integration Strategy

* Pre-compute values in backend
* Inject results into LLM context
* LLM formats final response

---

### Outcome

* Eliminated numeric hallucinations
* Improved reliability of financial outputs
* Balanced flexibility with correctness

---

### Key Insight

Not all problems should be solved using LLMs.

* **Computation → deterministic code**
* **Explanation → LLM**

---

## 3. Citation Validator (Most Critical Component)

### Prompt

"Design a validator ensuring every numeric claim in LLM output is grounded in retrieved context."

---

### AI Suggestions

1. Embedding-based validation
2. Approximate numeric matching
3. LLM-as-validator

---

### What I Rejected

#### 1. Embedding-based validation

* Measures semantic similarity, not factual correctness
* Numeric values may match unrelated context
* No guarantee exact value exists

---

#### 2. Approximate matching

* Introduces ambiguity
* Breaks determinism
* Not suitable for financial systems

---

#### 3. LLM as validator

* Circular dependency
* Non-deterministic
* Does not reduce hallucination

---

### What I Kept

* Extract numeric values
* Validate independently
* Return structured result

---

### Final Implementation

1. Extract numbers using regex
2. Normalize values
3. Exact match with context
4. Mark UNVERIFIED if mismatch

---

### Outcome

* Deterministic
* Transparent
* Audit-friendly

---

## 4. Structured Output

### Prompt

"How to ensure consistent structured output from LLM?"

---

### AI Suggestion

* JSON prompting
* String parsing

---

### What I Rejected

* Regex-based parsing
* Loose JSON handling

---

### Final Approach

* Enforced JSON format
* Used **Pydantic validation**
* Added fallback parsing

---

### Outcome

* Reliable structured output
* Reduced parsing errors

---

## 5. Evaluation Strategy

### Prompt

"How to evaluate a RAG system effectively?"

---

### AI Suggestion

* Basic query testing

---

### My Implementation

* Created `evals/cases.yaml`
* Built evaluation harness:

  * run queries
  * compare structured output
  * report PASS / FAIL

---

### Design Decision

* Focused on deterministic queries
* Avoided strict scoring for subjective queries

---

## 6. Smart Routing

### AI Suggestion

* Keyword-based routing

---

### My Improvement

* Combined:

  * keyword detection
  * portfolio preprocessing
  * filtered news

---

### Outcome

* Better relevance
* Reduced noise

---

## 7. Issues Introduced by AI and Fixes

| Issue                | Cause                   | Fix                |
| -------------------- | ----------------------- | ------------------ |
| Wrong calculations   | LLM limitation          | Hybrid system      |
| Hallucinated numbers | LLM behavior            | Validator          |
| Broken JSON          | formatting issues       | Schema enforcement |
| Import errors        | environment assumptions | module fixes       |

---

## 8. Time Distribution

| Task           | Time |
| -------------- | ---- |
| Design         | 20%  |
| Implementation | 40%  |
| Debugging      | 20%  |
| Evaluation     | 15%  |
| Docs           | 5%   |

---

## 9. Key Learnings

* LLMs must be **controlled, not trusted blindly**
* Deterministic logic is essential in finance
* Validation improves reliability
* Hybrid systems outperform pure LLM systems

---

## 10. Conclusion

AI was used as a **support tool**, not a decision-maker.

* Multiple suggestions were **rejected after evaluation**
* Core system design reflects **independent engineering decisions**

This project demonstrates a **controlled, reliable AI system design**, not just prompt-based experimentation.
