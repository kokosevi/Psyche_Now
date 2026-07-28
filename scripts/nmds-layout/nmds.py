import numpy as np


def pav(y, w):
    """Pool-Adjacent-Violators: gewichtete isotone (nicht-fallende) Regression."""
    y = np.asarray(y, float)
    w = np.asarray(w, float)
    n = len(y)
    lvl_val, lvl_w, lvl_n = [], [], []
    for i in range(n):
        cv, cw, cn = y[i], w[i], 1
        while lvl_val and lvl_val[-1] > cv:
            pv, pw, pn = lvl_val.pop(), lvl_w.pop(), lvl_n.pop()
            cv = (pv * pw + cv * cw) / (pw + cw)
            cw = pw + cw
            cn = pn + cn
        lvl_val.append(cv)
        lvl_w.append(cw)
        lvl_n.append(cn)
    out = np.empty(n)
    k = 0
    for v, cnt in zip(lvl_val, lvl_n):
        out[k:k + cnt] = v
        k += cnt
    return out


def _stress(D, Y, disp):
    d = np.linalg.norm(Y[:, None, :] - Y[None, :, :], axis=-1)
    iu = np.triu_indices(len(D), 1)
    num = np.sum((disp[iu] - d[iu]) ** 2)
    den = np.sum(d[iu] ** 2)
    return np.sqrt(num / den) if den > 0 else 0.0


def _smacof_once(D, Y, iters):
    n = len(D)
    iu = np.triu_indices(n, 1)
    npairs = len(iu[0])
    order = np.argsort(D[iu], kind="mergesort")   # stabile Rangordnung
    prev = None
    disp = np.zeros((n, n))
    for _ in range(iters):
        d = np.linalg.norm(Y[:, None, :] - Y[None, :, :], axis=-1)
        # Disparitäten: isotone Regression der Distanzen entlang der D-Rangordnung
        dvec = d[iu][order]
        disp_sorted = pav(dvec, np.ones(len(dvec)))
        tmp = np.empty(npairs)
        tmp[order] = disp_sorted
        # Skalen-Normierung der Disparitäten -> verhindert Kollaps auf einen Punkt
        ss = np.sum(tmp ** 2)
        if ss > 0:
            tmp = tmp * np.sqrt(npairs / ss)
        disp = np.zeros((n, n))
        disp[iu] = tmp
        disp = disp + disp.T
        # Guttman-Transform (SMACOF) mit disp als Ziel-Distanzen
        with np.errstate(divide="ignore", invalid="ignore"):
            ratio = np.where(d > 1e-12, disp / d, 0.0)
        B = -ratio
        np.fill_diagonal(B, 0.0)
        np.fill_diagonal(B, -B.sum(axis=1))
        Y = (B @ Y) / n
        s = _stress(D, Y, disp)
        if prev is not None and abs(prev - s) < 1e-9:
            break
        prev = s
    return Y, _stress(D, Y, disp)


def _classical_mds(D):
    n = len(D)
    J = np.eye(n) - np.ones((n, n)) / n
    B = -0.5 * J @ (D ** 2) @ J
    w, V = np.linalg.eigh(B)
    idx = np.argsort(w)[::-1][:2]
    L = np.clip(w[idx], 0, None)
    return V[:, idx] * np.sqrt(L)


def nmds(D, seed=42, restarts=8, iters=300):
    D = np.asarray(D, float)
    n = len(D)
    if n == 1:
        return np.zeros((1, 2)), 0.0
    rng = np.random.default_rng(seed)
    best_Y, best_s = None, np.inf
    # Init 0: klassisches MDS (Torgerson) als deterministischer Startpunkt
    inits = [_classical_mds(D)]
    for _ in range(restarts - 1):
        inits.append(rng.standard_normal((n, 2)))
    for Y0 in inits:
        Y, s = _smacof_once(D, Y0.copy(), iters)
        if s < best_s:
            best_s, best_Y = s, Y
    return best_Y, best_s
