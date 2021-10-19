# -*- coding: utf-8 -*-
"""
Utilities
"""
from .distances import (
    Euclidean,
    Cosine,
    L1,
    Manhattan,
    Lp,
    Linf
    )

# convenience access to cythonized metrics
euclidean = Euclidean()
cosine = Cosine()
l1 = L1()
manhattan = Manhattan()
linf = Linf()

# List of cythonized metrics
CYTHONIZED_METRICS = ['Euclidean',
                      'Cosine',
                      'L1',
                      'Manhattan',
                      'Lp',
                      'Linf'
                      ]
