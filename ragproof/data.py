import random

COMPONENTS = [
    "auth", "billing", "search", "ingest", "notifier", "scheduler",
    "gateway", "ledger", "catalog", "telemetry",
]
TOPICS = [
    ("retry policy", ["3 attempts with exponential backoff", "5 attempts with a 2s wait", "no retries, dead-letter queue"]),
    ("authentication", ["an X-Org-Token header", "OAuth2 client credentials", "a signed X-Signature header"]),
    ("configuration", ["config/{name}.yaml in the deploy repo", "environment variables on the pod", "a Vault path at secret/{name}"]),
    ("timeout", ["30 seconds", "90 seconds", "5 minutes"]),
    ("rate limit", ["20 requests per second", "120 requests per second", "500 requests per second"]),
]

SEED = 7


def make_docs(seed=SEED):
    """10 fake service docs, each covering 3 of the 5 topics."""
    rng = random.Random(seed)
    docs = []
    for i, name in enumerate(COMPONENTS):
        lines = [f"The {name} service {label} is {rng.choice(options)}." for label, options in rng.sample(TOPICS, 3)]
        docs.append({"id": f"doc-{i + 1:02d}", "title": f"The {name} service", "text": " ".join(lines)})
    return docs


def make_questions(docs, seed=SEED + 1, count=20):
    """Questions whose answer lives in exactly one doc."""
    rng = random.Random(seed)
    questions = []
    for doc in docs:
        name = doc["title"].split()[1]
        for label, _ in TOPICS:
            if label in doc["text"]:
                questions.append({"question": f"what is the {label} for the {name} service?", "doc_id": doc["id"]})
    rng.shuffle(questions)
    return questions[:count]
