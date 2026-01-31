import os
from langchain.text_splitter import MarkdownHeaderTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from pathlib import Path
from langchain_community.document_loaders import TextLoader
from dotenv import load_dotenv
load_dotenv()

KNOWLEDGE_PATH = "knowledge"


def load_knowledge():
    docs = []

    for path in Path("knowledge").rglob("*.md"):
        # Skip bio files (persona, tone, boundaries)
        if "knowledge/bio" in str(path):
            continue

        loader = TextLoader(str(path), encoding="utf-8")
        docs.extend(loader.load())

    return docs


def chunk_documents(docs):
    splitter = MarkdownHeaderTextSplitter(
        headers_to_split_on=[
            ("##", "section"),
            ("###", "subsection"),
        ]
    )

    chunks = []
    for doc in docs:
        split_docs = splitter.split_text(doc.page_content)
        for sd in split_docs:
            sd.metadata.update(doc.metadata)
            chunks.append(sd)

    return chunks

def build_vector_store(chunks):
    embeddings = OpenAIEmbeddings()
    vectorstore = FAISS.from_documents(chunks, embeddings)
    vectorstore.save_local("vector_store")

if __name__ == "__main__":
    docs = load_knowledge()
    chunks = chunk_documents(docs)
    build_vector_store(chunks)

    print(f"Embedded {len(chunks)} chunks")