#!/usr/bin/env python3

"""The setup script."""

import pathlib
from setuptools import setup, find_packages

here = pathlib.Path(__file__).parent

with open(here / "yaqd_edaq" / "VERSION") as version_file:
    version = version_file.read().strip()


with open("README.md") as readme_file:
    readme = readme_file.read()


requirements = ["yaqd-core>=2020.05.1", "yaqc", "pyserial"]

extra_requirements = {"dev": ["black", "pre-commit"]}

extra_files = {"yaqd_edaq": ["VERSION"]}

setup(
    author="Curtis Green",
    author_email="cmgreen3@wisc.edu",
    python_requires=">=3.7",
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: GNU Lesser General Public License v3 (LGPLv3)",
        "Natural Language :: English",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Topic :: Scientific/Engineering",
    ],
    description="yaq daemons for edaq sensor recording systems",
    entry_points={
        "console_scripts": [
            "yaqd-quadmf=yaqd_edaq._quadmf:QuadMF.main",
        ],
    },
    install_requires=requirements,
    extras_require=extra_requirements,
    license="GNU Lesser General Public License v3 (LGPL)",
    long_description=readme,
    long_description_content_type="text/markdown",
    include_package_data=True,
    package_data=extra_files,
    keywords="yaqd-edaq",
    name="yaqd-edaq",
    packages=find_packages(include=["yaqd-edaq", "yaqd-edaq.*"]),
    url="https://gitlab.com/yaq/yaqd-edaq",
    version=version,
    zip_safe=False,
)
