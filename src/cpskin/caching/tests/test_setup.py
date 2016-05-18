# -*- coding: utf-8 -*-
"""Setup tests for this package."""
from cpskin.caching.testing import CPSKIN_CACHING_INTEGRATION_TESTING  # noqa
from plone import api

import unittest


class TestSetup(unittest.TestCase):
    """Test that cpskin.caching is properly installed."""

    layer = CPSKIN_CACHING_INTEGRATION_TESTING

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.portal = self.layer['portal']
        self.installer = api.portal.get_tool('portal_quickinstaller')

    def test_product_installed(self):
        """Test if cpskin.caching is installed."""
        self.assertTrue(self.installer.isProductInstalled(
            'cpskin.caching'))

    def test_browserlayer(self):
        """Test that ICpskinCachingLayer is registered."""
        from cpskin.caching.interfaces import (
            ICpskinCachingLayer)
        from plone.browserlayer import utils
        self.assertIn(ICpskinCachingLayer, utils.registered_layers())


class TestUninstall(unittest.TestCase):

    layer = CPSKIN_CACHING_INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        self.installer = api.portal.get_tool('portal_quickinstaller')
        self.installer.uninstallProducts(['cpskin.caching'])

    def test_product_uninstalled(self):
        """Test if cpskin.caching is cleanly uninstalled."""
        self.assertFalse(self.installer.isProductInstalled(
            'cpskin.caching'))
