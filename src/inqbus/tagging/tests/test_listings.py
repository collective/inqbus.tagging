try:
    import unittest2 as unittest
except ImportError:
    import unittest

# zope imports
from Products.CMFPlone.utils import getToolByName
from plone.app.testing import TEST_USER_ID, setRoles
from zope.component import getMultiAdapter
# local imports
from inqbus.tagging.testing import INQBUS_TAGGING_INTEGRATION_TESTING


class TestContentListings(unittest.TestCase):

    layer = INQBUS_TAGGING_INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        self.request = self.layer['request']
        setRoles(self.portal, TEST_USER_ID, ['Manager'])

        self.portal.invokeFactory('Folder', 'test-folder')

        self.folder = self.portal['test-folder']


    def test_available_actions(self):
        view = getMultiAdapter(
            (self.folder, self.request),
            name="folder_contents"
        )
        view = view.__of__(self.folder)
        results = view()

        self.assertTrue('Retag' in results)

    def test_available_columns(self):
        view = getMultiAdapter(
            (self.folder, self.request),
            name='folder_contents'
        )
        view = view.__of__(self.folder)
        results = view()
        self.assertTrue('tags' in results)
        self.assertTrue('preview' in results)