from setuptools import setup, find_packages
import re

versionPattern = re.compile(r"""^__version__ = ['"](.*?)['"]$""", re.M)
with open("epsilon/_version.py", "rt") as f:
    version = versionPattern.search(f.read()).group(1)

setup(
    name="Epsilon",
    version=version,
    description="A set of utility modules used by Divmod projects",

    maintainer="divmod-dev",
    maintainer_email="divmod-dev@lists.launchpad.net",
    url="https://launchpad.net/divmod.org",

    install_requires=[
        "Twisted>=13.2.0",
        "PyOpenSSL>=0.13"
    ],
    packages=find_packages(),
    scripts=['bin/benchmark'],

    license="MIT",
    platforms=["any"],

    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Framework :: Twisted",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python",
        "Topic :: Internet",
        "Topic :: Security",
        "Topic :: Utilities"])
