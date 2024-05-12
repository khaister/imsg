import io

from setuptools import find_packages, setup

from imessage_reader import constants

with io.open("README.md", "rt", encoding="utf8") as f:
    LONG_DESC = f.read()


setup(
    name="imessage_reader",
    version=constants.VERSION,
    license="MIT",
    description="A library for reading iMessage data",
    long_description=LONG_DESC,
    long_description_content_type="text/markdown",
    author="Khai Nguyen, Bodo Schönfeld",
    author_email="bodo.schoenfeld@niftycode.de",
    url="https://github.com/khaister/imsg",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Operating System :: MacOS",
        "Operating System :: POSIX :: Linux",
        "Programming Language :: Python :: 3.12",
    ],
    packages=find_packages(exclude=("tests", "docs")),
    python_requires=">=3.12",
    entry_points={
        "console_scripts": ["imessage_reader=imessage_reader.cli:main"],
    },
    install_requires=["openpyxl"],
    tests_require=["pytest"],
)
