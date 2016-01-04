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
                                    u"Enter one tag per line."),
                               required=False,
    )

    used_exif = schema.Text(title=_(u"Used Exif Fields"),
                            description=_(u"Define Fields which should be " +
                                    u"used by Auto-Tag-Generation.\n" +
                                    u"Enter one field per line.\n" +
                                    u"Read more about the fields on " +
                                    u"exifread-Documentation."
                                ),
                            required=False,
                            )

    used_iptc = schema.Text(title=_(u"Used IPTC Fields"),
                            description=_(u"Define Fields which should be " +
                                    u"used by Auto-Tag-Generation.\n" +
                                    u"Enter one field per line.\n" +
                                    u"Read more about the fields on " +
                                    u"IPTCInfo-Documentation."
                                ),
                            required=False,
                            )
