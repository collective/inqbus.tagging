from iptcinfo import IPTCInfo
import cStringIO


def exif_to_tag(context, event):
    pass

def exif_to_orientation(context, event):
    image = context.image

    data = image.data
    io = cStringIO.StringIO(data)

    info = IPTCInfo(io, force=True)

    print info.keywords