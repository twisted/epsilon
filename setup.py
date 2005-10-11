
from distutils.core import setup

setup(
    name="Epsilon",
    version="0.1",
    maintainer="Divmod, Inc.",
    maintainer_email="support@divmod.org",
    url="http://divmod.org/trac/wiki/EpsilonProject",
    license="MIT",
    platforms=["any"],
    description="A set of utility modules used by Divmod projects",
    classifiers=[
        "Intended Audience :: Developers",
        "Programming Language :: Python",
        "Development Status :: 2 - Pre-Alpha",
        "Topic :: Utilities"],

    packages=['epsilon',
              'epsilon.test'])
