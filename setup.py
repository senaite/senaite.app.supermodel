# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

version = "1.0.0"


setup(
    name="senaite.core.supermodel",
    version=version,
    description="SENAITE CORE SUPERMODEL",
    long_description="",
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
    author="SENAITE Foundation",
    author_email="hello@senaite.com",
    url="https://github.com/senaite/senaite.core.supermodel",
    license="GPLv2",
    packages=find_packages("src", exclude=["ez_setup"]),
    package_dir={"": "src"},
    namespace_packages=["senaite", "senaite.core"],
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        "setuptools",
        "senaite.api",
        "senaite.core",
    ],
    extras_require={
        "test": [
            "Products.PloneTestCase",
            "plone.app.testing",
            "robotsuite",
            "unittest2",
        ]
    },
    entry_points="""
      # -*- Entry points: -*-
      [z3c.autoinclude.plugin]
      target = plone
      """,
)
