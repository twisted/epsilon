
from epsilon import version, setuphelper

setuphelper.autosetup(
    name="Epsilon",
    version=version.short(),
    maintainer="Divmod, Inc.",
    maintainer_email="support@divmod.org",
    url="http://divmod.org/trac/wiki/DivmodEpsilon",
    license="MIT",
    platforms=["any"],
    description="A set of utility modules used by Divmod projects",
    classifiers=[
        "Intended Audience :: Developers",
        "Programming Language :: Python",
        "Development Status :: 2 - Pre-Alpha",
        "Topic :: Utilities"],
    )
