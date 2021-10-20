# -*- coding: utf-8 -*-
# cython: language_level=3
"""
Dynamic Time Warping
"""
cimport cython
cimport numpy as np

import numpy as np

from libc.math cimport sqrt, abs, INFINITY

from utils.distances import cdist, Euclidean
from utils.distances cimport Metric, cy_argmin


@cython.boundscheck(False)
@cython.wraparound(False)
def _dtw(double[:, :] X, double[:, :] Y,
         int[:, :] window, Metric local_distance):
    """
    Cythonized Dynamic Time Warping
    """
    
    cdef int M = min(X.shape[0], np.max(window[:, 0]) + 1)
    cdef int N = min(Y.shape[0], np.max(window[:, 1]) + 1)
    cdef int L = window.shape[0]

    # the dtwd distance matrix is initialized with INFINITY
    cdef double[:, :] dtwd = np.ones((M + 1, N + 1),
                                      dtype=float) * INFINITY
    cdef int[:, :, :] path_indices = np.zeros((M, N, 2),
                                              dtype=np.int32)
    # candidates insertion, deletion, match
    cdef double[:] dtw_candidates = np.zeros(3, dtype=float)
    cdef int[:, :] path_candidates = np.zeros((3, 2), dtype=np.int32)

    cdef double insertion, deletion, match, c, bc
    cdef Py_ssize_t i, j, l, insi, insj, deli, delj, mati, matj, best
    cdef int m = M, n = N

    # Initialize matrix
    dtwd[0, 0] = 0.0

    # Compute cost
    for l in range(L):

        # Current indices
        i = window[l, 0] + 1
        j = window[l, 1] + 1

        # Indices of the candidates
        # Insertion
        insi = i - 1
        insj = j
        # Deletion
        deli = i
        delj = j - 1
        # Match
        mati = i - 1
        matj = j - 1

        # compute local distance
        c = local_distance.distance(X[mati], Y[matj])

        # insertion
        path_candidates[0, 0] = insi
        path_candidates[0, 1] = insj
        # deletion
        path_candidates[1, 0] = deli
        path_candidates[1, 1] = delj
        # match
        path_candidates[2, 0] = mati
        path_candidates[2, 1] = matj

        # cost insertion
        dtw_candidates[0] = dtwd[insi, insj]
        # cost deletion
        dtw_candidates[1] = dtwd[deli, delj]
        # cost match
        dtw_candidates[2] = dtwd[mati, matj]

        # pick best cost
        best, bc = cy_argmin(dtw_candidates)
        
        dtwd[i, j] = c + bc # dtw_candidates[best]
        path_indices[i, j, 0] = path_candidates[best, 0]
        path_indices[i, j, 1] = path_candidates[best, 1]

    # Backtrack
    cdef list path = []
    while not (m == n == 0):
        path.append((m - 1, n - 1))
        m = path_indices[m, n, 0]
        n = path_indices[m, n, 1]
        
    return path, dtwd[M, N]

@cython.boundscheck(False)
@cython.wraparound(False)
cpdef int[:, :] get_full_window(Py_ssize_t len_X, Py_ssize_t len_Y):
    """
    Helper method for initializing a full window
    """
    cdef int[:, :] window = np.zeros((len_X * len_Y, 2), dtype=np.int32)
    cdef int k
    for i in range(len_X):
        for j in range(len_Y):
            k = len_Y * i + j
            window[k, 0] = i
            window[k, 1] = j

    return window
