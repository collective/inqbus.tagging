import exifread
from iptcinfo import IPTCInfo
from StringIO import StringIO

def image_to_meta(context):

    meta = {}
    image = context.image
    data = image.data
    try:
        io = StringIO(data)
        io.seek(0)
        meta['iptc'] = IPTCInfo(io, force=True)
        io.seek(0)
        meta['exif'] = exifread.process_file(io)
    except:
        pass
    finally:
        io.close()

    return meta