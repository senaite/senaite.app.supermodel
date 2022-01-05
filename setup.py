# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

version = "2.1.0"

with open("docs/About.rst", "r") as fh:
    long_description = fh.read()

with open("CHANGES.rst", "r") as fh:
    long_description += "\n\n"
    long_description += "Changelog\n"
    long_description += "=========\n\n"
    long_description += fh.read()

setup(
    name="senaite.app.supermodel",
    version=version,
    description="A beautiful content wrapper for SENAITE that you will love",
    long_description=long_description,
    # long_description_content_type="text/markdown",
    # Get more strings from
    # http://pypi.python.org/pypi?:action=list_classifiers
    classifiers=[
        "Framework :: Plone",
        "Framework :: Zope2",
        "Programming Language :: Python",
        "Development Status :: 5 - Production/Stable",
        "License :: OSI Approved :: GNU General Public License v2 (GPLv2)",
    ],
    keywords="",
    author="SENAITE Professional Service Providers",
    author_email="senaite@senaite.com",
    url="https://github.com/senaite/senaite.app.supermodel",
    license="GPLv2",
    packages=find_packages("src", exclude=["ez_setup"]),
    package_dir={"": "src"},
    namespace_packages=["senaite", "senaite.app"],
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        "setuptools",
        "senaite.core",
    ],
    extras_require={
        "test": [
            "unittest2",
            "plone.app.testing",
        ]
    },
    entry_points="""
      # -*- Entry points: -*-
      [z3c.autoinclude.plugin]
      target = plone
      """,
)
