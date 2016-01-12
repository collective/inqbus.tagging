from persistent import Persistent
from zope.interface import Attribute
from zope.interface import implements
from zope.interface.interface import Interface


class ITaggingConfig(Interface):
    use_exif = Attribute("Boolean describing if exif should be converted to tags")

    use_iptc = Attribute("Boolean describing if iptc should be converted to tags")

    use_title = Attribute("Boolean describing if title should be converted to tags")

    use_lowercase = Attribute("Boolean describing if tag-names should be used lowercase or uppercase")

    exif_fields = Attribute("List holding information for converting exif")

    iptc_fields = Attribute("List holding information for converting iptc")

    ignored_tags = Attribute("List holding information for ignoring tags")


class TaggingConfig(Persistent):
    implements(ITaggingConfig)

    def __init__(self):
        self.use_exif = True
        self.use_iptc = True
        self.use_title = True
        self.use_lowercase = True
        self._exif_fields = []
        self._iptc_fields = []
        self.iptc_fields_lowercase = []
        self.exif_fields_lowercase = []
        self._ignored_tags = []
        self._test_image = None

    @property
    def exif_fields(self):
        return self._exif_fields

    @exif_fields.setter
    def exif_fields(self, value):
        self._exif_fields = value
        self.exif_fields_lowercase = []
        for dict in value:
            self.exif_fields_lowercase.append({
                'regex': dict['regex'],
                'field': dict['field'].lower(),
                'format': dict['format']
            })
        self._p_changed = True

    @property
    def iptc_fields(self):
        return self._iptc_fields

    @iptc_fields.setter
    def iptc_fields(self, value):
        self._iptc_fields = value
        self.iptc_fields_lowercase = []
        for dict in value:
            self.iptc_fields_lowercase.append({
                'regex': dict['regex'],
                'field': dict['field'].lower(),
                'format': dict['format']
            })
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
        return self._test_image

    @test_image.setter
    def test_image(self, value):
        self._test_image = value
        self._p_changed = True

    def add_exif_tag(self, tag):
        self.exif_fields.append({
            'regex': None,
            'field': unicode(tag),
            'format': None
        })
        self.exif_fields_lowercase.append(
            {
            'regex': None,
            'field': unicode(tag).lower(),
            'format': None
            }
        )
        self._p_changed = True

    def add_iptc_tag(self, tag):
        self.iptc_fields.append({
            'regex': None,
            'field': unicode(tag),
            'format': None
        })
        self.iptc_fields_lowercase.append(
            {
            'regex': None,
            'field': unicode(tag).lower(),
            'format': None
            }
        )
        self._p_changed = True

