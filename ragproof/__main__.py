import argparse
import json
import os
import random

from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate

from .data import make_docs, make_questions
from .search import search

DATA = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", "docs.json")
PROMPT = ChatPromptTemplate.from_messages([
    ("system", "Answer using only this context:\n{context}"),
    ("user", "{question}"),
])


def build():
    docs = make_docs()
    os.makedirs(os.path.dirname(DATA), exist_ok=True)
    with open(DATA, "w") as f:
        json.dump(docs, f, indent=2)
    print(f"Wrote {len(docs)} docs to {DATA}")


def answer(question, docs, k=3):
    hits = search(docs, question, k)
    if not hits:
        return "No matching docs.", []
    context = "\n\n".join(f"[{d['id']}] {d['text']}" for d in hits)
    if os.getenv("OPENAI_API_KEY"):
        from langchain.chat_models import init_chat_model
        llm = init_chat_model("gpt-4o-mini")
        return (PROMPT | llm | StrOutputParser()).invoke({"context": context, "question": question}), hits
    return f"(offline) {hits[0]['text']}", hits


def evaluate(docs):
    questions = make_questions(docs)
    hits = 0
    for q in questions:
        found = search(docs, q["question"], k=1)
        if found and found[0]["id"] == q["doc_id"]:
            hits += 1
    guess = sum(1 for q in questions if random.Random(q["doc_id"]).choice(docs)["id"] == q["doc_id"])
    n = len(questions)
    print(f"Hit rate: {hits}/{n} = {hits / n:.2f}")
    print(f"Random guess: {guess}/{n} = {guess / n:.2f}")


def main():
    parser = argparse.ArgumentParser(prog="ragproof")
    parser.add_argument("command", choices=["build", "ask", "evaluate"])
    parser.add_argument("question", nargs="?", default="")
    args = parser.parse_args()

    if args.command == "build":
        return build()
    if not os.path.exists(DATA):
        return print("No docs yet. Run: python -m ragproof build")
    with open(DATA) as f:
        docs = json.load(f)

    if args.command == "evaluate":
        return evaluate(docs)
    if not args.question:
        return print('Usage: python -m ragproof ask "your question"')
    reply, hits = answer(args.question, docs)
    print(reply)
    print("\nSources: " + ", ".join(d["title"] for d in hits))


if __name__ == "__main__":
    main()
