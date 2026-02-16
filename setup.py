from setuptools import setup, Extension
from Cython.Build import cythonize
import numpy

VERSION = "0.0.0"

# Write version file
with open("src/VERSION", "w") as f:
    f.write(VERSION)

# Define all extensions
extensions = [
    Extension(
        name="src.mod2sparse",
        sources=["src/include/mod2sparse.c", "src/mod2sparse.pyx"],
        include_dirs=[numpy.get_include(), "src/include"],
        extra_compile_args=["-std=c11"],
    ),
    Extension(
        name="src.c_util",
        sources=["src/c_util.pyx", "src/include/mod2sparse.c"],
        include_dirs=[numpy.get_include(), "src/include"],
        extra_compile_args=["-std=c11"],
    ),
    Extension(
        name="src.bp_guessing_decoder",
        sources=[
            "src/bp_guessing_decoder.pyx",
            "src/include/mod2sparse.c",
            "src/include/bpgd.cpp",
        ],
        language="c++",
        include_dirs=[numpy.get_include(), "src/include"],
        extra_compile_args=["-std=c11"],
    ),
    Extension(
        name="src.osd_window",
        sources=[
            "src/osd_window.pyx",
            "src/include/mod2sparse.c",
            "src/include/mod2sparse_extra.cpp",
            "src/include/bpgd.cpp",
        ],
        language="c++",
        include_dirs=[numpy.get_include(), "src/include"],
        extra_compile_args=["-std=c11"],
    ),
    Extension(
        name="src.bp4_osd",
        sources=[
            "src/bp4_osd.pyx",
            "src/include/mod2sparse.c",
            "src/include/mod2sparse_extra.cpp",
            "src/include/bpgd.cpp",
        ],
        language="c++",
        include_dirs=[numpy.get_include(), "src/include"],
        extra_compile_args=["-std=c11"],
    ),
]

setup(
    ext_modules=cythonize(extensions),
)
