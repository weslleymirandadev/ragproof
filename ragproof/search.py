def words(text):
    """Lowercase words longer than 2 characters."""
    cleaned = text.lower().replace(",", " ").replace(".", " ").replace("?", " ")
    return [w for w in cleaned.split() if len(w) > 2]


def score(doc, question):
    """How many different question words appear in this doc."""
    asked = set(words(question))
    text = set(words(doc["title"] + " " + doc["text"]))
    return len(asked & text)


def search(docs, question, k=3):
    """Return up to k docs with the most matching words, best first."""
    ranked = [(score(doc, question), doc) for doc in docs]
    ranked = [pair for pair in ranked if pair[0] > 0]
    ranked.sort(key=lambda pair: pair[0], reverse=True)
    return [doc for _, doc in ranked[:k]]
