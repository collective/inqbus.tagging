
import exifread
from StringIO import StringIO

from plone.registry.interfaces import IRegistry
from zope.component import getUtility
from inqbus.tagging.config import ORIENTATIONS, HORIZONTAL_MIRROR, \
    VERTICAL_MIRROR, USED_EXIF_SETTINGS_KEY, USED_IPTC_SETTINGS_KEY
from inqbus.tagging.functions import add_tags

import PIL
from inqbus.tagging.subscriber.functions import image_to_meta


def exif_to_tag(context, event):

    meta = image_to_meta ( context)

    registry = getUtility(IRegistry)

    allowed_iptc = registry[USED_IPTC_SETTINGS_KEY]
    allowed_exif = registry[USED_EXIF_SETTINGS_KEY]

    iptc = meta['iptc']
    exif = meta['exif']

    tags = list(context.Subject())

    if allowed_iptc and iptc:
        iptc_fields = allowed_iptc.replace(' ', '').split('/n')
        for field in iptc_fields:
            if str(field) in iptc.data:
                field_tags = iptc.data[field]
                if isinstance(field_tags, list):
                    tags = tags + field_tags
                else:
                    tags.append(str(field_tags))

    if allowed_exif and exif:
        for field in allowed_exif.split('\r\n'):
            if field in exif:
                tags.append(str(exif[field]))

    add_tags(context, tags_to_add=tags)



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