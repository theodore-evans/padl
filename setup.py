import setuptools
import pkg_resources
import pathlib
from distutils.util import convert_path

versions = {}
ver_path = convert_path('lf/version.py')
with open(ver_path) as ver_file:
    exec(ver_file.read(), versions)

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()


def parse_requirements(filename):
    with pathlib.Path(filename).open() as requirements_txt:
        return [str(requirement) for requirement in pkg_resources.parse_requirements(requirements_txt)]


setuptools.setup(
    name="lf",
    version=versions['__version__'],
    author="LF1",
    author_email="contact@lf1.io",
    description="Abstractions and base classes for AI models based on Pytorch.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/lf1-io/lf",
    packages=setuptools.find_packages(),
    setup_requires=[],
    license="Apache 2.0",
    classifiers=[
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "License :: Apache 2.0",
        'Topic :: Scientific/Engineering',
        'Topic :: Scientific/Engineering :: Artificial Intelligence',
    ],
    python_requires='>=3.8',
    install_requires=parse_requirements('requirements.txt'),
    test_suite="tests",
    tests_require=parse_requirements('requirements-test.txt'),
)