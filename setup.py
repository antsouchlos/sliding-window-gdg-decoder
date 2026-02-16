from setuptools import setup, Extension
from Cython.Build import cythonize
import numpy


# Define all extensions
extensions = [
    Extension(
        name="sw_gdg.c_util",
        sources=["sw_gdg/c_util.pyx", "sw_gdg/cpp/mod2sparse.c"],
        include_dirs=[numpy.get_include()],
        extra_compile_args=["-std=c11"],
    ),
    Extension(
        name="sw_gdg.mod2sparse",
        sources=["sw_gdg/cpp/mod2sparse.c", "sw_gdg/mod2sparse.pyx"],
        include_dirs=[numpy.get_include(), "sw_gdg/cpp"],
        extra_compile_args=["-std=c11"],
    ),
    Extension(
        name="sw_gdg.bp_guessing_decoder",
        sources=[
            "sw_gdg/bp_guessing_decoder.pyx",
            "sw_gdg/cpp/mod2sparse.c",
            "sw_gdg/cpp/bpgd.cpp",
        ],
        language="c++",
        include_dirs=[numpy.get_include(), "sw_gdg/cpp"],
        extra_compile_args=["-std=c11"],
    ),
    Extension(
        name="sw_gdg.osd_window",
        sources=[
            "sw_gdg/osd_window.pyx",
            "sw_gdg/cpp/mod2sparse.c",
            "sw_gdg/cpp/mod2sparse_extra.cpp",
            "sw_gdg/cpp/bpgd.cpp",
        ],
        language="c++",
        include_dirs=[numpy.get_include(), "sw_gdg/cpp"],
        extra_compile_args=["-std=c11"],
    ),
    Extension(
        name="sw_gdg.bp4_osd",
        sources=[
            "sw_gdg/bp4_osd.pyx",
            "sw_gdg/cpp/mod2sparse.c",
            "sw_gdg/cpp/mod2sparse_extra.cpp",
            "sw_gdg/cpp/bpgd.cpp",
        ],
        language="c++",
        include_dirs=[numpy.get_include(), "sw_gdg/cpp"],
        extra_compile_args=["-std=c11"],
    ),
]

setup(
    name="sw_gdg",
    ext_modules=cythonize(
        extensions, compiler_directives={"language_level": 3, "profile": False}
    ),
)
