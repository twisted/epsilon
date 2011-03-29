
from epsilon import version, setuphelper

setuphelper.autosetup(
    name="Epsilon",
    version=version.short(),
    maintainer="divmod-dev",
    maintainer_email="divmod-dev@lists.launchpad.net",
    url="https://launchpad.net/divmod.org",
    license="MIT",
    platforms=["any"],
    description="A set of utility modules used by Divmod projects",
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Framework :: Twisted",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python",
        "Topic :: Internet",
        "Topic :: Security",
        "Topic :: Utilities"],
    scripts=['bin/benchmark'])
