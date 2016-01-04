from StringIO import StringIO

from iptcinfo import IPTCInfo
from plone.registry.interfaces import IRegistry
from zope.component import getUtility
from inqbus.tagging.config import ORIENTATIONS, HORIZONTAL_MIRROR, \
    VERTICAL_MIRROR, USED_EXIF_SETTINGS_KEY, USED_IPTC_SETTINGS_KEY
from inqbus.tagging.functions import add_tags
import exifread
import PIL


def exif_to_tag(context, event):
    image = context.image

    data = image.data

    io = StringIO(data)
    io.seek(0)

    info_iptc = IPTCInfo(io, force=True)

    io.seek(0)

    exif_tags = exifread.process_file(io)

    tags = list(context.Subject())

    registry = getUtility(IRegistry)

    used_iptc = registry[USED_IPTC_SETTINGS_KEY]
    used_exif = registry[USED_EXIF_SETTINGS_KEY]

    print info_iptc.data

    if used_iptc:
        iptc_fields = used_iptc.replace(' ', '').split('/n')
        for field in info_iptc.data:
            if str(field) not in iptc_fields:
                continue
            field_tags = info_iptc.data[field]
            if isinstance(field_tags, list):
                tags = tags + field_tags
            else:
                tags.append(str(field_tags))

    if used_exif:
        for field in exif_tags:
            if field not in used_exif:
                continue
            tags.append(str(exif_tags[field]))

    add_tags(context, tags_to_add=tags)

    io.close()


def exif_to_orientation(context, event):
    image = context.image
    data = image.data

    io = StringIO(data)
    io.seek(0)

    exif_tags = exifread.process_file(io)
    orientation = get_orientation(exif_tags)

    io.seek(0)

    pil_image = PIL.Image.open(io)
    converted_img_io = StringIO()

    if orientation:
        rotation = ORIENTATIONS[orientation][1]
        mirror = ORIENTATIONS[orientation][2]

        rotated_image = pil_image.rotate(360-rotation,
                                         resample=PIL.Image.BICUBIC,
                                         expand=True)
        if mirror == HORIZONTAL_MIRROR:
            rotated_image = rotated_image.transpose(PIL.Image.FLIP_LEFT_RIGHT)
        elif mirror == VERTICAL_MIRROR:
            rotated_image = rotated_image.transpose(PIL.Image.FLIP_TOP_BOTTOM)

        rotated_image.save(converted_img_io, 'JPEG', quality=100)

        context.image.data = converted_img_io.getvalue()

        context.reindexObject()

    converted_img_io.close()
    io.close()


def get_orientation(tags):
    if 'Image Orientation' in tags:
        rot_index = tags['Image Orientation'].values[0]
        return rot_index
    else:
        return None