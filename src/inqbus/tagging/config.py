# -*- coding: utf-8 -*-
"""Configuration options for inqbus.tagging"""

PROJECT_NAME = 'inqbus.tagging'
INSTALL_PROFILE = '{0}:default'.format(PROJECT_NAME)
UNINSTALL_PROFILE = '{0}:uninstall'.format(PROJECT_NAME)

IGNORED_TAGS_SETTINGS_KEY = 'inqbus.tagging.interfaces.ITagSettings.ignored_tags'
USED_EXIF_SETTINGS_KEY = 'inqbus.tagging.interfaces.ITagSettings.used_exif'
USED_IPTC_SETTINGS_KEY = 'inqbus.tagging.interfaces.ITagSettings.used_iptc'
TEST_IMAGE_SETTINGS_KEY = 'inqbus.tagging.interfaces.ITagSettings.test_image'
# configuration for image rotation

NO_MIRROR = 0
HORIZONTAL_MIRROR = 1
VERTICAL_MIRROR = 2

ORIENTATIONS = {
    1: ("Normal", 0, NO_MIRROR),
    2: ("Mirrored left-to-right", 0, HORIZONTAL_MIRROR),
    3: ("Rotated 180 degrees", 180, NO_MIRROR),
    4: ("Mirrored top-to-bottom", 0, VERTICAL_MIRROR),
    5: ("Mirrored along top-left diagonal", 90, HORIZONTAL_MIRROR),
    6: ("Rotated 90 degrees", 90, NO_MIRROR),
    7: ("Mirrored along top-right diagonal", 270, HORIZONTAL_MIRROR),
    8: ("Rotated 270 degrees", 270, NO_MIRROR)
}