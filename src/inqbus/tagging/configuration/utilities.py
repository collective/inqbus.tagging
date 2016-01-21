from persistent import Persistent
from persistent.list import PersistentList
from plone.api import content
from zope.interface import Attribute
from zope.interface import implements
from zope.interface.interface import Interface



class ITaggingConfig(Interface):
    use_exif = Attribute("Boolean describing if exif should be converted to tags")

    use_iptc = Attribute("Boolean describing if iptc should be converted to tags")

    use_xmp = Attribute("Boolean describing if XMP should be converted to tags")

    use_title = Attribute("Boolean describing if title should be converted to tags")

    exif_fields = Attribute("List holding information for converting exif")

    iptc_fields = Attribute("List holding information for converting iptc")

    xmp_fields = Attribute("List holding information for converting XMP")

    ignored_tags = Attribute("List holding information for ignoring tags")

    title_regex = Attribute("String holding a regex to filter title words")



class TaggingConfig(Persistent):
    implements(ITaggingConfig)

    use_exif = True
    use_iptc = True
    use_xmp = True
    # use_title should be false as default because there could be lots of unwanted
    # tags
    use_title = False
    title_regex = u""

    def __init__(self):
        self._exif_fields = []
        self._iptc_fields = []
        self._xmp_fields = []
        self._ignored_tags = []
        self._test_image = None

    @property
    def exif_fields(self):
        return self._exif_fields

    @exif_fields.setter
    def exif_fields(self, value):
        self._exif_fields = value
        self._p_changed = True

    @property
    def iptc_fields(self):
        return self._iptc_fields

    @iptc_fields.setter
    def iptc_fields(self, value):
        self._iptc_fields = value
        self._p_changed = True

    @property
    def xmp_fields(self):
        return self._xmp_fields

    @xmp_fields.setter
    def xmp_fields(self, value):
        self._xmp_fields = value
        self._p_changed = True

    @property
    def ignored_tags(self):
        return self._ignored_tags

    @ignored_tags.setter
    def ignored_tags(self, value):
        self._ignored_tags = []
        for dict in value:
            self._ignored_tags.append(dict['tag'])
        self._p_changed = True

    @property
    def test_image(self):
        try:
            result = content.get(UID=self._test_image)
        except Exception as e:
            return None
        return result

    @test_image.setter
    def test_image(self, value):
        self._test_image = value.UID()
        self._p_changed = True

    def add_exif_tag(self, tag):
        self.exif_fields.append({
            'regex': None,
            'field': unicode(tag),
            'format': None
        })
        self._p_changed = True

    def add_iptc_tag(self, tag):
        self.iptc_fields.append({
            'regex': None,
            'field': unicode(tag),
            'format': None
        })
        self._p_changed = True

    def add_xmp_tag(self, tag):
        self.xmp_fields.append({
            'regex': None,
            'field': unicode(tag),
            'format': None
        })
        self._p_changed = True
