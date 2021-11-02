import numpy as np
import setuptools
from setuptools import setup
from distutils.extension import Extension
from Cython.Build import cythonize
import os

include_dirs = [np.get_include()]

extensions = [
    Extension("utils.distances",
              # ["utils/distances.pyx"],
              [os.path.join("utils", "distances.pyx")],
              include_dirs=include_dirs,
    ),
    Extension("alignment.cy_dtw",
              # ["alignment/cy_dtw.pyx"],
              [os.path.join("alignment", "cy_dtw.pyx")],
              include_dirs=include_dirs,
              )
]


setup(
    name='musical_informatics',
    version='0.1.5',
    description='Framework for Musical Informatics',
    packages=setuptools.find_packages(),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research",
        "Programming Language :: Python :: 3",
        "Topic :: Scientific/Engineering :: MusicInformationRetrieval",
    ],
    author='Carlos Cancino-Chacón and Silvan Peter',
    ext_modules=cythonize(
        extensions,
        language_level=3
    ),
)
