from rag import initialize_rag, answer_question


def main():

    print("=" * 60)
    print(" Asset Knowledge Assistant (RAG)")
    print("=" * 60)

    print("\nInitializing RAG Pipeline...\n")

    initialize_rag()

    print("\nSystem Ready!")
    print("Type 'exit' to quit.\n")

    while True:

        question = input("Ask a Question: ")

        if question.lower() == "exit":
            print("\nThank you for using Asset Knowledge Assistant!")
            break

        answer = answer_question(question)

        print("\nAnswer:\n")
        print(answer)
        print("\n" + "-" * 60 + "\n")


if __name__ == "__main__":
    main()