from Products.CMFPlone.utils import safe_unicode
from plone.registry.interfaces import IRegistry
from zope.component import getUtility

from inqbus.tagging.config import IGNORED_TAGS_SETTINGS_KEY


def add_tags(obj, tags_to_add=[]):

    tags = list(obj.Subject()) + tags_to_add
    tags = list(set(tags))

    clear_tags = []

    for tag in tags:

        try:
            int(tag)
        except ValueError:
            pass
        else:
            continue

        try:
            clear_tag = safe_unicode(tag)
        except UnicodeDecodeError:
            continue

        if len(clear_tag) < 100 and not check_ignored_tags(clear_tag):
            clear_tags.append(clear_tag)

    obj.setSubject(clear_tags)
    obj.reindexObject()


def check_ignored_tags(tag):
    registry = getUtility(IRegistry)

    ignored_tags = registry[IGNORED_TAGS_SETTINGS_KEY]

    if tag in ignored_tags:
        return True
    else:
        return False