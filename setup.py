# ===========================================================
# DOCS
# ===========================================================

"""PINNACLE: 

"""

# ===========================================================
# IMPORTS
# ===========================================================

import pathlib
import os

from ez_setup import use_setuptools
use_setuptools()

from setuptools import setup, find_packages

# ===========================================================
# CONSTANTS
# ===========================================================

PATH = pathlib.Path(os.path.abspath(os.path.dirname(__file__)))
print(PATH)

REQUIREMENTS = [
    "ads",
    "numpy",
    "pandas",
    "pytest",
    "openpyxl"]

with open(PATH / "README.rst") as fp:
    LONG_DESCRIPTION = fp.read()
 
DESCRIPTION = (
    "Tools to analyze publication metrics from an institution"
    )

with open(PATH / "pinnacle" / "__init__.py") as fp:
    VERSION = [
        l for l in fp.readlines() if l.startswith("__version__")
    ][0].split("=", 1)[-1].strip().replace('"', "")

# ===========================================================
# FUNCTIONS
# ===========================================================

# setup(name="hearsay", packages=find_packages())

def do_setup():
    setup(
        name="pinnacle_pub",
        version=VERSION,
        description=DESCRIPTION,
        long_description=LONG_DESCRIPTION,
        long_description_content_type='text/markdown',

        author=[
            "Marcelo Lares"],
        author_email="marcelo.lares@unc.edu.ar",
        url="https://github.com/IATE-CONICET-UNC/pinnacle",
        license="MIT",

        keywords=["publications"],

        classifiers=[
            "Development Status :: 4 - Beta",
            "Intended Audience :: Education",
            "Intended Audience :: Science/Research",
            "License :: OSI Approved :: MIT License",
            "Operating System :: OS Independent",
            "Programming Language :: Python",
            "Programming Language :: Python :: 3.8",
            "Programming Language :: Python :: Implementation :: CPython",
            "Topic :: Scientific/Engineering"],

        packages=["pinnacle"],
        py_modules=["ez_setup"],

        install_requires=REQUIREMENTS)


if __name__ == "__main__":
    do_setup()
