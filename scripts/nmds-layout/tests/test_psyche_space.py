import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from spaces import get_space, _grid_regions


def test_grid_regionen_im_canvas_und_disjunkt():
    r = _grid_regions(("p1", "p2", "p3", "p4", "p5"), cols=3)
    assert set(r) == {"p1", "p2", "p3", "p4", "p5"}
    for (x0, x1, y0, y1) in r.values():
        assert 5 <= x0 < x1 <= 95 and 5 <= y0 < y1 <= 95


def test_psyche_space_konfiguration():
    sp = get_space("psyche")
    assert sp["name"] == "psyche"
    assert sp["clusters"] == ("p1", "p2", "p3", "p4", "p5")
    assert sp["out_suffix"] == ".psyche"
    assert set(sp["regions"]) == set(sp["clusters"])
    assert sp["bib_dir"].endswith(os.path.join("Bibliothek", "Allgemeine Psychologie"))
    assert sp["themen_dir"].endswith(os.path.join("content", "psyche"))
    assert set(sp["edges"]) == {"cross_min_sim", "cross_topk", "curate_min_sim", "curate_max_deg"}


def test_erleben_unveraendert():
    sp = get_space("erleben")
    assert sp["out_suffix"] == "" and sp["clusters"] == ("k1", "k2", "k3", "k4")


if __name__ == "__main__":
    test_grid_regionen_im_canvas_und_disjunkt()
    test_psyche_space_konfiguration()
    test_erleben_unveraendert()
    print("OK test_psyche_space")
