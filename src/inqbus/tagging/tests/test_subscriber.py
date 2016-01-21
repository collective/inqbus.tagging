try:
    import unittest2 as unittest
except ImportError:
    import unittest

import os

# zope imports
from Products.CMFPlone import PloneMessageFactory as _
from plone.app.testing import TEST_USER_ID, setRoles
from zope.component import queryUtility
from zope.i18n import translate
from zope.component import getMultiAdapter
from zope.lifecycleevent import modified


# local imports
from inqbus.tagging.testing import INQBUS_TAGGING_INTEGRATION_TESTING
from inqbus.tagging.browser.actions import RetagAction, RetagActionView
from inqbus.tagging.configuration.utilities import ITaggingConfig
from inqbus.tagging.functions import get_tagging_config
from inqbus.tagging.tests.test_functions import image_by_path


class TestContentListings(unittest.TestCase):

    layer = INQBUS_TAGGING_INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        self.request = self.layer['request']
        setRoles(self.portal, TEST_USER_ID, ['Manager'])

        self.config = get_tagging_config()

        self.config.use_title = True

        self.config.title_regex = '(\w+)'

    def _get_token(self, context):
        authenticator = getMultiAdapter(
            (context, self.request), name='authenticator')

        return authenticator.token()

    def test_title(self):


        self.portal.invokeFactory('Folder', 'test-folder', title="Test Title")

        folder = self.portal['test-folder']

        subjects = folder.Subject()

        self.assertTrue('Test' in subjects)
        self.assertTrue('Title' in subjects)

    def test_rotation_and_filename_tags(self):
        self.portal.invokeFactory('Folder', 'test-folder', title="Test Title")

        folder = self.portal['test-folder']

        dirname, filename = os.path.split(os.path.abspath(__file__))

        path = os.path.join(dirname, "test_images", "Landscape_5.jpg")

        folder.invokeFactory('Image', 'testimage', image=image_by_path(path),
                             title="Different Title")

        image = folder['testimage']

        self.assertTrue(image.image._height < image.image._width)
        subjects = image.Subject()

        self.assertTrue('Different' in subjects)
        self.assertTrue('Title' in subjects)
        self.assertTrue('Landscape_5' in subjects)