# -*- coding: utf-8 -*-
"""Test Setup of inqbus.tagging."""

# python imports
try:
    import unittest2 as unittest
except ImportError:
    import unittest

# zope imports
from plone import api
from plone.browserlayer.utils import registered_layers

# local imports
from inqbus.tagging.config import PROJECT_NAME
from inqbus.tagging.interfaces import ILayer
from inqbus.tagging.testing import INQBUS_TAGGING_INTEGRATION_TESTING


class TestFunctions(unittest.TestCase):
    layer = INQBUS_TAGGING_INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']

    def test_sample(self):
        pass


# class TestSetup(unittest.TestCase):
#     """Validate setup process for inqbus.tagging."""
#
#     layer = INQBUS_TAGGING_INTEGRATION_TESTING
#
#     def setUp(self):
#         """Additional test setup."""
#         self.portal = self.layer['portal']
#
#     def test_product_is_installed(self):
#         """Validate that our product is installed."""
#         qi = api.portal.get_tool('portal_quickinstaller')
#         self.assertTrue(qi.isProductInstalled(PROJECT_NAME))
#
#     def test_addon_layer(self):
#         """Validate that the browserlayer for our product is installed."""
#         self.assertIn(ILayer, registered_layers())
#
#     def test_collective_z3cform_datagridfield_installed(self):
#         """Validate that collective.z3cform.datagridfield is installed."""
#         qi = self.portal.portal_quickinstaller
#         self.assertTrue(
#             qi.isProductInstalled('collective.z3cform.datagridfield')
#         )
#
#
# class UninstallTestCase(unittest.TestCase):
#     """Validate uninstall process for inqbus.tagging."""
#
#     layer = INQBUS_TAGGING_INTEGRATION_TESTING
#
#     def setUp(self):
#         """Additional test setup."""
#         self.portal = self.layer['portal']
#
#         qi = self.portal.portal_quickinstaller
#         with api.env.adopt_roles(['Manager']):
#             qi.uninstallProducts(products=[PROJECT_NAME])
#
#     def test_product_is_uninstalled(self):
#         """Validate that our product is uninstalled."""
#         qi = self.portal.portal_quickinstaller
#         self.assertFalse(qi.isProductInstalled(PROJECT_NAME))
#
#     def test_addon_layer_removed(self):
#         """Validate that the browserlayer is removed."""
#         self.assertNotIn(ILayer, registered_layers())
