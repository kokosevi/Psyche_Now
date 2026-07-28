import sys, os
import numpy as np
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from tfidf import tokenize, tfidf_matrix, cosine_dissim


def test_tokenize_strips_timestamps_and_stopwords():
    toks = tokenize("Das Erleben (19:37) ist und der die das Netzwerk.")
    assert "erleben" in toks and "netzwerk" in toks
    assert "und" not in toks and "der" not in toks
    assert not any(":" in t for t in toks)


def test_dissim_is_symmetric_zero_diag_and_deterministic():
    docs = ["erleben netzwerk trance", "erleben netzwerk fokus", "diagnose symptom ursache"]
    m1 = cosine_dissim(tfidf_matrix(docs))
    m2 = cosine_dissim(tfidf_matrix(docs))
    assert np.allclose(m1, m1.T)
    assert np.allclose(np.diag(m1), 0.0)
    assert np.array_equal(m1, m2)                    # deterministisch
    assert m1[0, 1] < m1[0, 2]                       # 0 & 1 ähnlicher als 0 & 2


if __name__ == "__main__":
    test_tokenize_strips_timestamps_and_stopwords()
    test_dissim_is_symmetric_zero_diag_and_deterministic()
    print("OK test_tfidf")
