# -*- coding: utf-8 -*-
"""
Dynamic Time Warping
"""
import numpy as np

from alignment.cy_dtw import _dtw, get_full_window
from utils import euclidean


def dynamic_time_warping(X, Y, metric=euclidean, window=None):
    """
    Dynamic Time Warping

    Parameters
    ----------
    X : np.ndarray
        A 2D array with size (n_observations, n_features)
    Y : np.ndarray
        A 2D array with size (m_observations, n_features)
    metric: Metric
        A cythonized metric (see utils/distances.pyx)
    window: np.dnarray or None
        A window for looking for a solution for DTW. If
        `None`, it gets the window of all observations in
        X and Y.

    Returns
    -------
    path : np.ndarray
        A 2D array containing the alignment with columns
        (index_in_X, index_in_Y).
    dtwdist: float
        The DTW-distance
    """
    if window is None:
        window = get_full_window(len(X), len(Y))

    X, Y = np.atleast_2d(X, Y)
    path, dtwdist = _dtw(X=X, Y=Y,
                         local_distance=metric,
                         window=window)

    return np.array(path[::-1], dtype=int), dtwdist
