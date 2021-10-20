cimport numpy
import numpy as np
cimport cython

cdef class Metric:
    cdef double distance(self, double[:] X, double[:] Y) except? 0.0

cdef (int, double) cy_argmin(double[:] x)
