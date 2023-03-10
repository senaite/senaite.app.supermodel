<div align="center">

  <a href="https://github.com/senaite/senaite.app.supermodel">
    <img src="static/logo.png" alt="senaite.app.supermodel" height="128" />
  </a>

  <p>A beautiful content wrapper for SENAITE that you will love</p>

  <div>
    <a href="https://pypi.python.org/pypi/senaite.app.supermodel">
      <img src="https://img.shields.io/pypi/v/senaite.app.supermodel.svg?style=flat-square" alt="pypi-version" />
    </a>
    <a href="https://travis-ci.org/senaite/senaite.app.supermodel">
      <img src="https://img.shields.io/travis/senaite/senaite.app.supermodel.svg?style=flat-square" alt="travis-ci" />
    </a>
    <a href="https://github.com/senaite/senaite.app.supermodel/pulls">
      <img src="https://img.shields.io/github/issues-pr/senaite/senaite.app.supermodel.svg?style=flat-square" alt="open PRs" />
    </a>
    <a href="https://github.com/senaite/senaite.app.supermodel/issues">
      <img src="https://img.shields.io/github/issues/senaite/senaite.app.supermodel.svg?style=flat-square" alt="open Issues" />
    </a>
    <a href="#">
      <img src="https://img.shields.io/badge/PRs-welcome-brightgreen.svg?style=flat-square" alt="pr" />
    </a>
    <a href="https://www.senaite.com">
      <img src="https://img.shields.io/badge/Made%20for%20SENAITE-%E2%AC%A1-lightgrey.svg" alt="Made for SENAITE" />
    </a>
  </div>
</div>


## About

The SENAITE.APP.SUPERMODEL is a content wrapper for objects and catalog brains
in SENAITE and provides a unified dictionary interface to access the schema
fields, methods and metadata.


## For what is it needed?

The purpose of the SUPERMODEL is to help coders to access the data from content
objects. It also ensures that the most effective and efficient method is used to
achieve a task.


## How does it work?

A `SuperModel` can be instantiated with an `UID` of a content object:

    >>> from senaite.app.supermodel import SuperModel
    >>> supermodel = SuperModel('e37c1b659137414e872c08af410f09b4')

This will give transparent access to all schema fields of the wrapped object as
well to all the metadata columns of the primary catalog of this object:

    >>> supermodel.MySchemaField'
    'Value of MySchemaField'

Please read the [full functional doctest](src/senaite.app.supermodel/docs/SUPERMODEL.rst)
to see the super powers of the `SuperModel` in action.


## Installation

SENAITE.APP.SUPERMODEL is a dependency of SENAITE.CORE and therefore no
additional installation steps are required.


## License

**SENAITE.APP.SUPERMODEL** Copyright (C) RIDING BYTES & NARALABS

This program is free software; you can redistribute it and/or modify it under
the terms of the [GNU General Public License version
2](https://github.com/senaite/senaite.app.supermodel/blob/master/LICENSE)
as published by the Free Software Foundation.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
GNU General Public License for more details.
