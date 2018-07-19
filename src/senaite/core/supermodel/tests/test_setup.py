# -*- coding: utf-8 -*-

from .base import SimpleTestCase


class TestSetup(SimpleTestCase):
    """ Test Setup
    """


def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    suite.addTest(makeSuite(TestSetup))
    return suite
