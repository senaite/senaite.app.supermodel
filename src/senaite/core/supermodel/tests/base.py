# -*- coding: utf-8 -*-
#
# This file is part of SENAITE.CORE.SUPERMODEL.
#
# SENAITE.CORE.SUPERMODEL is free software: you can redistribute it and/or
# modify it under the terms of the GNU General Public License as published by
# the Free Software Foundation, version 2.
#
# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE. See the GNU General Public License for more
# details.
#
# You should have received a copy of the GNU General Public License along with
# this program; if not, write to the Free Software Foundation, Inc., 51
# Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.
#
# Copyright 2018-2020 by it's authors.
# Some rights reserved, see README and LICENSE.

import sys

import transaction
import unittest2 as unittest
from plone.app.testing import PLONE_FIXTURE
from plone.app.testing import TEST_USER_ID
from plone.app.testing import FunctionalTesting
from plone.app.testing import PloneSandboxLayer
from plone.app.testing import applyProfile
from plone.app.testing import setRoles
from plone.testing import zope


class SimpleTestLayer(PloneSandboxLayer):
    """Setup Plone with installed AddOn only
    """
    defaultBases = (PLONE_FIXTURE,)

    def setUpZope(self, app, configurationContext):
        super(SimpleTestLayer, self).setUpZope(app, configurationContext)

        import Products.TextIndexNG3
        import bika.lims
        import senaite.core
        import senaite.core.listing
        import senaite.impress
        import senaite.core.spotlight

        # XXX HACK
        # The `senaite.core` module refers to the `senaite.core.supermodel`
        # middle namespace package because of the `sys.path` order of the
        # `bin/test` script:
        #
        # <module 'senaite.core' from 'senaite.core.listing/src/senaite/core/__init__.pyc'>   # noqa
        #
        # Maybe we should move all senaite.core.* packages into a new namespace
        # which is unused, e.g. `senaite.app.*`?
        senaite.core.__path__ = filter(
            lambda p: p.endswith("senaite.core/src"), sys.path)

        # Load ZCML
        self.loadZCML(package=Products.TextIndexNG3)
        self.loadZCML(package=bika.lims)
        self.loadZCML(package=senaite.core)
        self.loadZCML(package=senaite.core.listing)
        self.loadZCML(package=senaite.impress)
        self.loadZCML(package=senaite.core.spotlight)

        # Install product and call its initialize() function
        zope.installProduct(app, "Products.TextIndexNG3")
        zope.installProduct(app, "bika.lims")
        zope.installProduct(app, "senaite.core")
        zope.installProduct(app, "senaite.core.listing")
        zope.installProduct(app, "senaite.impress")
        zope.installProduct(app, "senaite.core.spotlight")

    def setUpPloneSite(self, portal):
        super(SimpleTestLayer, self).setUpPloneSite(portal)
        applyProfile(portal, "senaite.core:default")
        transaction.commit()


###
# Use for simple tests (w/o contents)
###
SIMPLE_FIXTURE = SimpleTestLayer()
SIMPLE_TESTING = FunctionalTesting(
    bases=(SIMPLE_FIXTURE, ),
    name="senaite.core.supermodel:SimpleTesting"
)


class SimpleTestCase(unittest.TestCase):
    layer = SIMPLE_TESTING

    def setUp(self):
        super(SimpleTestCase, self).setUp()

        self.app = self.layer["app"]
        self.portal = self.layer["portal"]
        self.request = self.layer["request"]
        self.request["ACTUAL_URL"] = self.portal.absolute_url()
        setRoles(self.portal, TEST_USER_ID, ["LabManager", "Manager"])


class FunctionalTestCase(unittest.TestCase):
    layer = SIMPLE_TESTING

    def setUp(self):
        super(FunctionalTestCase, self).setUp()

        self.app = self.layer["app"]
        self.portal = self.layer["portal"]
        self.request = self.layer["request"]
        self.request["ACTUAL_URL"] = self.portal.absolute_url()
        setRoles(self.portal, TEST_USER_ID, ["LabManager", "Member"])
