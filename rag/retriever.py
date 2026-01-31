from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS

def load_retriever(k: int = 4):
    embeddings = OpenAIEmbeddings()

    vectorstore = FAISS.load_local(
        "vector_store",
        embeddings,
        allow_dangerous_deserialization=True
    )

    return vectorstore.as_retriever(
        search_kwargs={"k": k}
    )