## Project: MindMate – AI-Powered Mental Health Screening

### Problem
Traditional mental health screening tools are static and lack contextual, personalized interaction.

### Context & Constraints
- Needed safe, grounded responses
- Required structured assessments (PHQ-9, GAD-7)
- Must support many concurrent users

### Solution
Built an end-to-end RAG platform integrating:
- LangChain for orchestration
- TiDB vector database for retrieval
- OpenAI APIs for LLM responses
- FastAPI backend for scalable serving

The system provided contextual, personalized responses based on retrieved assessment data.

### Key Decisions
- Used RAG instead of fine-tuning for transparency and update flexibility
- Structured retrieved context to avoid hallucinations
- Separated persona from retrieved knowledge

### Trade-offs
- Retrieval quality directly impacted response quality
- Required careful chunking and metadata design

### Outcome
- Supported thousands of user sessions
- Delivered context-aware and grounded LLM responses
- Demonstrated scalable RAG system design

### What I’d Do Differently
- Add reranking for improved retrieval precision
- Improve long-context handling for complex conversations