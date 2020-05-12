import versioneer
from setuptools import setup, find_packages

setup(
    version=versioneer.get_version(),
    cmdclass=versioneer.get_cmdclass(),
    name="Epsilon",
    description="A set of utility modules used by Divmod projects",

    url="https://github.com/twisted/epsilon",

    install_requires=[
        "six>=1.12.0",
        "zope.interface",
        "Twisted[tls]>=13.2.0",
    ],
    packages=find_packages(),
    scripts=['bin/benchmark', 'bin/certcreate'],

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
