from zope.interface import Interface
from zope import schema
from plone.supermodel import model
from inqbus.tagging import MessageFactory as _
from plone.app.vocabularies.catalog import CatalogSource
from z3c.relationfield.schema import RelationChoice


class ILayer(Interface):
    pass


class ITagSettings(model.Schema):
    """ Define settings data structure """

    ignored_tags = schema.Text(title=_(u"Ignored Tags"),
                               description=_(u"Define Tags which should be " +
                                    u"ignored by Auto-Tag-Generation.\n" +
                                    u"Enter one tag per line."),
                               required=False,
    )

    used_exif = schema.Text(title=_(u"Use these Exif Fields"),
                            description=_(u"Define Fields which should be " +
                                    u"used by Auto-Tag-Generation.\n" +
                                    u"Enter one field per line.\n" +
                                    u"Read more about the fields on " +
                                    u"exifread-Documentation."
                                ),
                            required=False,
                            )

    used_iptc = schema.Text(title=_(u"Use these IPTC Fields"),
                            description=_(u"Define Fields which should be " +
                                    u"used by Auto-Tag-Generation.\n" +
                                    u"Enter one field per line.\n" +
                                    u"Read more about the fields on " +
                                    u"IPTCInfo-Documentation."
                                ),
                            required=False,
                            )

    test_image = schema.Text(title=_(u"Select EXIF-Tags from Image"),
                               description=_(u"Here you can select an image to pick EXIF tags for the whitelists"),
                               )


class ITagSettingsView(ITagSettings):
    test_image = RelationChoice(title=_(u"Select EXIF-Tags from Image"),
                               description=_(u"Here you can select an image to pick EXIF tags for the whitelists"),
                               vocabulary="plone.app.vocabularies.Catalog",
                               required=True,
                               )

