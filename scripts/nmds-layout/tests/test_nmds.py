import sys, os
import numpy as np
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from nmds import pav, nmds


def test_pav_is_monotone():
    out = pav(np.array([3.0, 1.0, 2.0, 4.0]), np.ones(4))
    assert np.all(np.diff(out) >= -1e-9), out


def test_nmds_deterministic_and_recovers_line():
    # 5 Punkte auf einer Linie -> Rangordnung der Distanzen in 2D erhalten
    true = np.array([[0, 0], [1, 0], [2, 0], [3, 0], [4, 0]], float)
    D = np.sqrt(((true[:, None, :] - true[None, :, :]) ** 2).sum(-1))
    Y1, s1 = nmds(D, seed=42)
    Y2, s2 = nmds(D, seed=42)
    assert np.allclose(Y1, Y2) and abs(s1 - s2) < 1e-12      # deterministisch
    assert s1 < 0.05                                          # niedriger Stress
    # Rangordnung: Nachbardistanzen < Randdistanz
    d01 = np.linalg.norm(Y1[0] - Y1[1])
    d04 = np.linalg.norm(Y1[0] - Y1[4])
    assert d01 < d04


if __name__ == "__main__":
    test_pav_is_monotone()
    test_nmds_deterministic_and_recovers_line()
    print("OK test_nmds")
