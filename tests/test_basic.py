from ragproof.data import make_docs, make_questions
from ragproof.search import score, search, words


def test_words_drops_short_words():
    assert words("What is the API?") == ["what", "the", "api"]


def test_docs_have_expected_keys():
    docs = make_docs()
    assert len(docs) == 10
    assert set(docs[0]) == {"id", "title", "text"}


def test_docs_are_deterministic():
    assert make_docs() == make_docs()


def test_score_counts_matching_words():
    doc = {"id": "d", "title": "billing service", "text": "the retry policy is 3 attempts"}
    # question and doc share: what->no, the, retry, policy, billing (from title) = 4
    assert score(doc, "what is the retry policy for billing?") == 4


def test_search_puts_the_right_doc_first():
    docs = make_docs()
    hits = search(docs, "what is the timeout for the auth service?", k=3)
    assert hits[0]["title"] == "The auth service"


def test_questions_point_at_real_docs():
    docs = make_docs()
    questions = make_questions(docs)
    ids = {d["id"] for d in docs}
    assert len(questions) == 20
    assert all(q["doc_id"] in ids for q in questions)
