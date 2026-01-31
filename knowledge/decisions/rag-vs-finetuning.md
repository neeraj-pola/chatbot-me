## Decision: RAG vs Fine-Tuning for LLM Systems

### Context
Needed to build an AI system that produced grounded, updateable, and explainable responses for user-facing applications.

### Options Considered
- Fine-tuning a language model
- Retrieval-Augmented Generation (RAG)

### Decision
Chose RAG over fine-tuning.

### Reasoning
- Allowed updates to knowledge without retraining models
- Made responses traceable to source documents
- Reduced hallucination risk for sensitive domains

### Trade-offs
- Retrieval quality directly impacts generation quality
- Requires careful chunking and metadata design

### Outcome
Enabled rapid iteration, transparent responses, and reliable updates without retraining overhead.