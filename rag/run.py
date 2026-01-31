from chain import build_rag_chain

def main():
    rag_chain = build_rag_chain()

    print("Neeraj-bot ready. Ask a question (type 'exit' to quit).\n")

    while True:
        q = input("You: ")
        if q.lower() in ["exit", "quit"]:
            break

        answer = rag_chain.invoke(q)
        print("\nBot:", answer, "\n")

if __name__ == "__main__":
    main()