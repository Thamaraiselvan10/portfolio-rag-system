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
* Designed a **separate validation layer** (not part of default RAG)

---

### Reasoning

The assignment explicitly emphasizes:

* grounding
* validation
* evaluation

A basic RAG pipeline is insufficient without enforcing correctness.

---

## 2. Citation Validator (Most Critical Component)

### Prompt

"Design a validator ensuring every numeric claim in LLM output is grounded in retrieved context."

---

### AI Suggestions

1. Use embeddings to compare numeric claims with context
2. Allow approximate numeric matching (e.g., 39.8 ≈ 40)
3. Use the LLM itself to verify claims

---

## What I Rejected (Detailed)

### 1. Embedding-based validation

**AI Idea:**
Use semantic similarity between generated output and retrieved chunks.

**Why I rejected it:**

* Embeddings measure **semantic similarity, not factual accuracy**
* Numeric values can match unrelated content (false positives)
* Example risk:

  * “40% growth” could match any financial text mentioning “growth”
* No guarantee that the **exact number exists in context**

**Conclusion:**
Not suitable for strict numeric grounding required in financial systems.

---

### 2. Approximate numeric matching

**AI Idea:**
Allow tolerance (e.g., 39.8 ≈ 40)

**Why I rejected it:**

* Introduces ambiguity in validation
* Breaks **determinism**
* Makes system non-auditable
* Financial systems require **exact traceability**

**Conclusion:**
Even small deviations cannot be accepted without explicit justification.

---

### 3. LLM as validator

**AI Idea:**
Ask the LLM to verify its own output

**Why I rejected it:**

* Creates **circular dependency**
* Same model both generates and validates
* Does not reduce hallucination risk
* Non-deterministic and hard to debug

**Conclusion:**
Validation must be independent of generation.

---

## What I Kept from AI

* Extract numeric claims from output
* Validate each claim independently
* Return structured validation results

---

## Final Implementation

A deterministic validator:

1. Extract numbers using regex (integers, currency, percentages)
2. Normalize values (remove commas, symbols)
3. Compare against retrieved context (exact match)
4. If mismatch:

   * Mark response as **UNVERIFIED**
   * Return list of unmatched values

---

## Outcome

* Fully deterministic
* No reliance on LLM for validation
* Transparent and auditable
* Strictly aligned with assignment Variant A

---

## 3. Structured Output

### Prompt

"How to ensure consistent structured output from LLM?"

---

### AI Suggestion

* Use JSON-like prompts
* Parse output using string operations

---

### What I Rejected

* Regex-based JSON extraction
* Loose parsing of model output

---

### Final Approach

* Enforced strict JSON format in prompt
* Used **Pydantic schema validation**
* Added fallback JSON extraction only when necessary

---

### Outcome

* Reliable structured outputs
* Strong schema enforcement
* Reduced parsing errors

---

## 4. Evaluation Strategy

### Prompt

"How to evaluate a RAG system effectively?"

---

### AI Suggestion

* Basic query testing

---

### My Implementation

* Introduced **evals/cases.yaml** (as required)
* Built evaluation harness:

  * Executes queries
  * Compares structured output with expected values
  * Reports PASS / FAIL

---

### Design Decision

Focused evaluation on:

* deterministic queries (e.g., highest, lowest)

Avoided strict scoring for:

* subjective queries (news impact, diversification)

---

## 5. Smart Routing

### AI Suggestion

* Keyword-based routing

---

### My Improvement

* Combined:

  * keyword detection
  * portfolio-specific preprocessing
  * filtered news retrieval

---

### Outcome

* Better context relevance
* Reduced noise for LLM

---

## 6. Issues Introduced by AI and Fixes

| Issue                     | Cause                   | Fix                                |
| ------------------------- | ----------------------- | ---------------------------------- |
| Incorrect numeric outputs | LLM hallucination       | Added strict validator             |
| Broken JSON outputs       | inconsistent formatting | Enforced schema + fallback parsing |
| Overly verbose responses  | default LLM behavior    | constrained prompt rules           |
| Path/import errors        | environment assumptions | fixed module execution             |

---

## 7. Time Distribution

| Task           | Approx Time |
| -------------- | ----------- |
| System design  | 20%         |
| Implementation | 40%         |
| Debugging      | 20%         |
| Evaluation     | 15%         |
| Documentation  | 5%          |

---

## 8. Key Learnings

* LLM outputs require strict validation in financial contexts
* Semantic similarity is not sufficient for factual correctness
* Deterministic checks improve reliability significantly
* Evaluation is essential for system credibility

---

## 9. Conclusion

AI was used as a **support tool**, not as a decision-maker.

* Multiple AI suggestions were **critically evaluated and rejected**
* Core components (validation, structured output, evaluation) were **designed manually**

This project reflects an **engineering-first approach to AI systems**, focusing on correctness, transparency, and reliability.
