# flake8: noqa

from distutils.core import setup

import numpy
from Cython.Build import cythonize

setup(ext_modules=cythonize("boxscript/utils.pyx"), include_dirs=[numpy.get_include()])
