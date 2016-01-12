import re
from StringIO import StringIO

import PIL
import exifread

from inqbus.tagging.config import ORIENTATIONS, HORIZONTAL_MIRROR, \
    VERTICAL_MIRROR
from inqbus.tagging.functions import image_to_meta, get_iptc_fields, \
    get_exif_fields, get_use_iptc, get_use_exif, get_use_lowercase, \
    get_exif_fields_lowercase, get_iptc_fields_lowercase, add_tags


def get_tags(image_tags, tag_config):
    tags = []
    use_lower = get_use_lowercase()
    available_fields = []
    field_value = {}
    for key in image_tags.keys():
        if use_lower:
            available_fields.append(str(key).lower())
            field_value[str(key).lower()] = image_tags[key]
        else:
            available_fields.append(str(key))
            field_value[str(key)] = image_tags[key]
    allowed_fields = []
    field_info = {}
    for dict in tag_config:
        allowed_fields.append(dict['field'])
        field_info[dict['field']] = dict
    available_fields = set(available_fields)
    allowed_fields = set(allowed_fields)
    fields = available_fields.intersection(allowed_fields)

    for field in fields:
        regex = field_info[field]['regex']
        str_format = field_info[field]['format']
        value = field_value[field]

        if not regex or re.match(regex, value):
            if str_format:
                tags.append(format(str_format, value))
            else:
                tags.append(value)

    return tags


def exif_to_tag(context, event):

    meta = image_to_meta(context)

    use_lower = get_use_lowercase()

    if use_lower:
        allowed_iptc = get_iptc_fields_lowercase()
        allowed_exif = get_exif_fields_lowercase()
    else:
        allowed_exif = get_exif_fields()
        allowed_iptc = get_iptc_fields()

    iptc = meta['iptc'].data
    exif = meta['exif']

    tags = list(context.Subject())

    if get_use_iptc():
        tags = tags + get_tags(iptc, allowed_iptc)

    if get_use_exif():
        tags = tags + get_tags(exif, allowed_exif)

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