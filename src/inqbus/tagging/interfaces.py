from zope.interface import Interface
from zope import schema
from plone.supermodel import model
from inqbus.tagging import MessageFactory as _


class ILayer(Interface):
    pass


class ITagSettings(model.Schema):
    """ Define settings data structure """

    ignored_tags = schema.Text(title=_(u"Ignored Tags"),
                               description=_(u"Define Tags which should be " +
                                    u"ignored by Auto-Tag-Generation.\n" +
                                    u"Enter one tag per line.")
    )

    ignored_exif = schema.Text(title=_(u"Ignored Exif Fields"),
                               description=_(u"Define Fields which should be " +
                                    u"ignored by Auto-Tag-Generation.\n" +
                                    u"Enter one field per line.\n" +
                                    u"Read more about the fields on " +
                                    u"exifread-Documentation."
                                )
    )

    ignored_iptc = schema.Text(title=_(u"Ignored IPTC Fields"),
                               description=_(u"Define Fields which should be " +
                                    u"ignored by Auto-Tag-Generation.\n" +
                                    u"Enter one field per line.\n" +
                                    u"Read more about the fields on " +
                                    u"IPTCInfo-Documentation."
                                )
    )
