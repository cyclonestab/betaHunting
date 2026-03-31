# tests/test_pipeline.py

import numpy as np
import pytest
from sklearn.preprocessing import MinMaxScaler


def make_sequences(data: np.ndarray, seq_len: int):
    n       = len(data)
    indices = np.arange(seq_len + 1)[None, :] + np.arange(n - seq_len)[:, None]
    windows = data[indices, 0]
    X       = windows[:, :-1, np.newaxis]
    y       = windows[:, -1:  ]
    return X, y


# ── Test 1 : make_sequences output shape ───────────────────────────────────────
def test_make_sequences_shape():
    data    = np.arange(100).reshape(-1, 1).astype(float)
    seq_len = 30
    X, y    = make_sequences(data, seq_len)

    assert X.shape == (70, 30, 1), f"unexpected X shape: {X.shape}"
    assert y.shape == (70, 1),     f"unexpected y shape: {y.shape}"


# ── Test 2 : make_sequences correct values ─────────────────────────────────────
def test_make_sequences_values():
    data    = np.arange(10).reshape(-1, 1).astype(float)
    seq_len = 3
    X, y    = make_sequences(data, seq_len)

    # first window  : X=[0,1,2], y=3
    # second window : X=[1,2,3], y=4
    assert X[0].flatten().tolist() == [0.0, 1.0, 2.0]
    assert y[0].tolist()           == [3.0]
    assert X[1].flatten().tolist() == [1.0, 2.0, 3.0]
    assert y[1].tolist()           == [4.0]
