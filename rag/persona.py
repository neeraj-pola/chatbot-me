def load_persona():
    with open("knowledge/bio/persona.md") as f:
        persona = f.read()

    with open("knowledge/bio/tone.md") as f:
        tone = f.read()

    with open("knowledge/bio/boundaries.md") as f:
        boundaries = f.read()

    return f"""
{persona}

{tone}

{boundaries}

Rules:
- Use retrieved context for facts only
- Be honest if information is missing
- No generic advice
- Default to concise answers
"""