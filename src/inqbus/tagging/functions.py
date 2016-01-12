import exifread
from iptcinfo import IPTCInfo

from StringIO import StringIO

from zope.component import getUtility

from inqbus.tagging.configuration.utilities import ITaggingConfig


def get_use_exif():
    config_store = getUtility(ITaggingConfig)
    return config_store.use_exif


def get_use_iptc():
    config_store = getUtility(ITaggingConfig)
    return config_store.use_iptc


def get_use_title():
    config_store = getUtility(ITaggingConfig)
    return config_store.use_title


def get_use_lowercase():
    config_store = getUtility(ITaggingConfig)
    return config_store.use_lowercase


def get_exif_fields():
    config_store = getUtility(ITaggingConfig)
    return config_store.exif_fields


def get_iptc_fields():
    config_store = getUtility(ITaggingConfig)
    return config_store.iptc_fields


def get_exif_fields_lowercase():
    config_store = getUtility(ITaggingConfig)
    return config_store.exif_fields_lowercase


def get_iptc_fields_lowercase():
    config_store = getUtility(ITaggingConfig)
    return config_store.iptc_fields_lowercase


def get_ignored_tags():
    config_store = getUtility(ITaggingConfig)
    return config_store.ignored_tags


def get_ignored_tags_form():
    tags = get_ignored_tags()
    tag_list = []
    for tag in tags:
        tag_list.append({'tag': tag})
    return tag_list


def get_test_image():
    config_store = getUtility(ITaggingConfig)
    return config_store.test_image


def image_to_meta(context):

    meta = {}
    image = context.image
    data = image.data

    io = StringIO(data)
    io.seek(0)
    meta['iptc'] = IPTCInfo(io, force=True)
    io.seek(0)
    meta['exif'] = exifread.process_file(io)

    io.close()

    return meta


def add_tags(obj, tags_to_add=[]):
    if not hasattr(obj, 'Subject'):
        return

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
            clear_tag = unicode(tag)
        except UnicodeDecodeError:
            continue

        ignored_tags = get_ignored_tags()

        if len(clear_tag) < 100 and tag not in ignored_tags:
            clear_tags.append(clear_tag)

    obj.setSubject(clear_tags)
    obj.reindexObject()