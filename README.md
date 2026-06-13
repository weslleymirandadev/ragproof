# ragproof

A tiny search demo over fake technical docs.
It builds 10 made-up service docs, lets you ask questions about them,
and checks whether the search actually finds the right doc.

No API key and no internet needed.

## What it does

- Generates 10 fake docs about services like `auth`, `billing`, and `ingest`.
- Answers a question by finding the doc that shares the most words with it.
- Measures how often the top result is the right one, out of 20 questions.

## Install

```bash
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

## Usage

```bash
python -m ragproof build
python -m ragproof ask "how do I rotate the database credentials?"
python -m ragproof evaluate
python -m pytest tests -q
```

## How it works

`build` writes the fake docs to `data/docs.json`. Each doc is just a dict with
an `id`, a `title`, and a `text`.

`search` splits the question into words and counts how many of those words
appear in each doc (words of 3 letters or fewer are ignored). The docs with the
highest count come first. There is no machine learning and no vector database.

`ask` searches, then either sends the top docs to an LLM (if `OPENAI_API_KEY`
is set) or just prints the top doc's text with an `(offline)` marker.

## Results

On the 20 built-in questions:

```
Hit rate: 20/20 = 1.00
Random guess: 4/20 = 0.20
```

A perfect score here is not impressive. Every question contains the name of
the service it is about, and that name appears in only one doc, so the search
mostly just matches that name. If I remove the service name from the
questions, the hit rate drops to 3/20. The questions are too easy, not the
search too good.

## Tests

```bash
python -m pytest tests -q
# 6 passed
```

## License

MIT
