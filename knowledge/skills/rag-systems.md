## Skill: RAG (Retrieval-Augmented Generation) Systems

### Where I’ve Used It
Built RAG systems in academic and applied projects, including an AI-powered mental health support platform.

### What I’ve Built With It
- End-to-end RAG pipelines using LangChain and vector databases
- Context-aware LLM responses for structured assessments (PHQ-9, GAD-7)
- Retrieval pipelines optimized for relevance and response quality

### How I Use It
I treat RAG as a reliability problem:
- Separate persona from retrieved knowledge
- Limit context size to avoid noise
- Prefer structured chunks over raw documents

### Decisions & Trade-offs
Chose RAG instead of fine-tuning because:
- Easier to update and debug
- Better factual grounding and transparency

Trade-offs:
- Requires careful chunking and metadata design
- Retrieval quality directly impacts generation quality

### Limits / What I’m Still Improving
- Advanced reranking strategies
- Long-context optimization for large knowledge bases