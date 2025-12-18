from setuptools import setup, Extension
import pybind11

ext_modules = [
    Extension(
        "connect4_core",
        ["services/connect4_core.cpp"],
        include_dirs=[pybind11.get_include()],
        language='c++'
    ),
]

setup(
    name="connect4_core",
    ext_modules=ext_modules,
)