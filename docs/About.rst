.. image:: https://raw.githubusercontent.com/senaite/senaite.core.supermodel/master/static/logo_pypi.png
   :target: https://github.com/senaite/senaite.core.supermodel#readme
   :alt: senaite.core.supermodel
   :height: 128

*A beautiful content wrapper for SENAITE that you will love*
============================================================

.. image:: https://img.shields.io/pypi/v/senaite.core.supermodel.svg?style=flat-square
   :target: https://pypi.python.org/pypi/senaite.core.supermodel

.. image:: https://img.shields.io/github/issues-pr/senaite/senaite.core.supermodel.svg?style=flat-square
   :target: https://github.com/senaite/senaite.core.supermodel/pulls

.. image:: https://img.shields.io/github/issues/senaite/senaite.core.supermodel.svg?style=flat-square
   :target: https://github.com/senaite/senaite.core.supermodel/issues

.. image:: https://img.shields.io/badge/README-GitHub-blue.svg?style=flat-square
   :target: https://github.com/senaite/senaite.core.supermodel#readme

.. image:: https://img.shields.io/badge/Built%20with-%E2%9D%A4-brightgreen.svg
   :target: https://github.com/senaite/senaite.core.supermodel/blob/master/src/senaite/core/supermodel/docs/SUPERMODEL.rst

.. image:: https://img.shields.io/badge/Made%20for%20SENAITE-%E2%AC%A1-lightgrey.svg
   :target: https://www.senaite.com


About
=====

The SENAITE CORE SUPERMODEL is a content wrapper for objects and catalog brains
in SENAITE and provides a unified dictionary interface to access the schema
fields, methods and metadata.


For what is it needed?
======================

The purpose of the SUPERMODEL is to help coders to access the data from content
objects. It also ensures that the most effective and efficient method is used to
achieve a task.


How does it work?
-----------------

A `SuperModel` can be instantiated with an `UID` of a content object::

    >>> from senaite.core.supermodel import SuperModel
    >>> supermodel = SuperModel('e37c1b659137414e872c08af410f09b4')

This will give transparent access to all schema fields of the wrapped object as
well to all the metadata columns of the primary catalog of this object::

    >>> supermodel.MySchemaField'
    'Value of MySchemaField'

Please read the `full functional doctest`_ to see the super powers of the
`SuperModel` in action.


Installation
============

SENAITE.CORE.SUPERMODEL is a dependency of SENAITE.CORE and therefore no
additional installation steps are required.


.. _full functional doctest: https://github.com/senaite/senaite.core.supermodel/blob/master/src/senaite/core/supermodel/docs/SUPERMODEL.rst
