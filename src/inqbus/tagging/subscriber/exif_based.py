import re
from StringIO import StringIO

import PIL
import exifread

from inqbus.tagging.config import ORIENTATIONS, HORIZONTAL_MIRROR, \
    VERTICAL_MIRROR
from inqbus.tagging.functions import image_to_meta, add_tags, get_tagging_config


def get_tags(image_tags, tag_config):
    tags = []
    available_fields = []
    field_value = {}
    for key in image_tags.keys():
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

        if regex:
           match = re.search(regex, value.printable)
           if match :
                if str_format:
                   tags.append(str_format.format(*match.groups()))
                else:
                   tags.append(match.group(0))
           continue

        if str_format:
            tags.append(str_format.format(value.printable))
        else:
            tags.append(value.printable)

    return tags


def exif_to_tag(context, event):

    tagging_config = get_tagging_config()

    meta = image_to_meta(context,
                         use_exif=tagging_config.use_exif,
                         use_iptc=tagging_config.use_iptc,
                         use_xmp=tagging_config.use_xmp)

    allowed_exif = tagging_config.exif_fields
    allowed_iptc = tagging_config.iptc_fields
    allowed_xmp = tagging_config.xmp_fields

    iptc = meta['iptc'].data
    exif = meta['exif']
    xmp = meta['xmp']

    tags = list(context.Subject())

    if tagging_config.use_iptc:
        tags = tags + get_tags(iptc, allowed_iptc)

    if tagging_config.use_exif:
        tags = tags + get_tags(exif, allowed_exif)

    if tagging_config.use_xmp:
        tags = tags + get_tags(xmp, allowed_xmp)

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