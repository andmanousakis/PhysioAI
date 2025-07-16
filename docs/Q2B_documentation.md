# PT Message Generation – Production Design Document

---

## Problem / Motivation

**Problem:**  
Physical Therapists (PTs) are expected to provide empathetic, personalized feedback to patients after each recovery session. While this practice supports patient motivation and engagement, it is repetitive, time-consuming, and inconsistent across practitioners.

**Motivation:**  
Automating this task offers an opportunity to:
- Reduce PT workload
- Deliver timely and consistent communication
- Ensure every patient receives thoughtful encouragement

To succeed, the system must be clinically safe, customizable, and indistinguishable from a human-generated message — never robotic, generic, or AI-sounding.

---

## Overview of the Solution

We propose a modular, LLM-powered system that generates short (2–4 sentence) post-session messages using structured data. The messages will be reviewed by PTs through a dedicated UI before being delivered to patients.

### Core Components

1. **Feature Transformer** – Converts structured session metrics into a natural-language summary.
2. **Prompt Constructor** – Builds LLM prompts with explicit tone, personalization, and safety instructions.
3. **Message Generator (LLM)** – Uses GPT-4 or OSS LLMs (e.g., Mistral) to produce human-like messages.
4. **PT Review Interface** – A user-friendly UI allowing PTs to accept, edit, or reject messages.
5. **Feedback Loop** – Logs therapist actions to guide future refinement or fine-tuning.

---

## Success Metrics

| Category             | Metric                                               | Goal             |
|----------------------|------------------------------------------------------|------------------|
| Message Quality       | % accepted without edits                             | ≥ 80%            |
| Engagement            | % of sessions with reviewed messages                 | ≥ 90%            |
| Efficiency            | Avg. time saved per PT per session                   | ≥ 30 seconds     |
| Personalization       | % of messages with session-specific content          | ≥ 95%            |
| Safety                | % of messages with flagged clinical inaccuracies     | ≤ 0.5%           |
| Feedback Integration  | Rejection reason frequency reduction                 | Downward trend   |

---

## Methodology

### Data Inputs

- Structured features per session (e.g., pain, fatigue, exercises skipped)
- No labeled training data initially
- PT feedback (accept/edit/reject) used for iterative evaluation

### Model Strategy

- **Initial Phase:** Use GPT-4 with few-shot prompting
- **Fallback:** Template-based messages for incomplete outputs
- **Future State:** Fine-tune OSS model on curated PT-reviewed samples

### Clinical and Technical Safeguards

- Hardcoded tone and structural constraints in prompts
- Explicit avoidance of hallucinations and medical advice
- All messages routed through human-in-the-loop validation

---

## Deployment Architecture

| Layer            | Tooling                            | Purpose                                                      |
|------------------|-------------------------------------|--------------------------------------------------------------|
| LLM API          | OpenAI GPT-4 / OSS (Mistral, etc.) | Message generation                                           |
| Prompt Engine    | Python                              | Prompt generation from session data                          |
| API Backend      | FastAPI                             | Message orchestration, feedback logging                      |
| Frontend         | Streamlit (PoC/MVP) → React         | Therapist-facing message review interface                    |
| Scheduling       | Airflow                             | Message batch generation and feedback monitoring             |
| Streaming (opt.) | Kafka / Redis Streams               | Real-time session ingestion (optional at MVP stage)          |
| Storage          | PostgreSQL                          | Stores sessions, prompts, messages, feedback logs            |
| Monitoring       | Prometheus + Grafana                | Token usage, latency, completion success tracking            |
| Model Tracking   | MLflow / Weights & Biases           | Prompt versioning and experimentation tracking               |
| Infrastructure   | Docker + Kubernetes                 | Containerized, auto-scalable production deployment           |

---

## Delivery Phases & Timeline

| Phase                  | Duration        | Key Deliverables                                                |
|------------------------|-----------------|------------------------------------------------------------------|
| **Phase 1 – PoC**      | 1.5 months       | Manual prompt testing, sample messages, internal validation     |
| **Phase 2 – MVP**      | 4–6 months       | Prompt engine, GPT-4 integration, Streamlit UI, feedback loop   |
| **Phase 3 – Productionization** | 6–9 months | Full stack build, monitoring, React UI, Kubernetes deployment   |
| **Phase 4 – Continuous Improvement** | Ongoing | Fine-tuning, RAG, drift detection, multilingual support         |

> **Total estimated time to production maturity: 12–16 months**

---

## Timeline Risks and Mitigation

| Risk                         | Mitigation Strategy                                               |
|------------------------------|--------------------------------------------------------------------|
| Staff turnover               | Modular architecture, written documentation, onboarding guides    |
| Lack of LLM expertise        | Start with prompt-based PoC to defer fine-tuning complexity       |
| Feedback delays              | Incentivize early PT participation, use internal QA proxy         |
| Budget & pricing constraints | Track token usage; switch to OSS models or batching as needed     |
| Data annotation gaps         | Leverage weak supervision; mine accepted messages for tuning      |
| Compliance review bottlenecks| Involve clinical experts early, automate tone/safety checks       |

---

## Message Generation Pipeline

1. **Data Ingestion**
   - Sessions arrive via API or stream; stored in PostgreSQL

2. **Prompt Generation**
   - Prompt builder assembles structured user prompt

3. **LLM Call**
   - LLM generates message with latency/token metadata captured

4. **PT Review**
   - Message is presented in UI with accept/edit/reject tagging

5. **Feedback Storage**
   - Logged into DB and optionally fed into a fine-tuning dataset

---

## Future Improvements

- **Fine-tuning OSS models** to reduce cost and increase control
- **Multilingual support** for patients across regions
- **Configurable tone/length** per therapist or patient type
- **Session trend tracking** to reference previous progress
- **Retrieval-Augmented Generation (RAG)** to improve variety
- **Safety classifier** for hallucination or tone mismatches
- **Reinforcement via PT feedback** to gradually improve message quality

---

## Conclusion

This system is designed to balance clinical safety, PT usability, and technical feasibility while keeping costs and complexity in check. By deploying in progressive phases, we can derisk core components, gather feedback early, and scale toward a robust human-in-the-loop assistant that delivers high-value, human-like patient encouragement at scale.
