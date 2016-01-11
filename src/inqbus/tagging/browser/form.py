from collective.z3cform.datagridfield import DataGridFieldFactory, DictRow
from plone.supermodel import model
from plone.autoform.form import AutoExtensibleForm
from plone.app.registry.browser.controlpanel import RegistryEditForm, \
    ControlPanelFormWrapper
from Products.Five.browser import BrowserView
from plone.z3cform import layout
from plone.registry.interfaces import IRegistry
from plone import api

from zope import schema
from z3c.form import field, button, form
from zope.component import getUtility
from z3c.relationfield.schema import RelationChoice


from inqbus.tagging.configuration.utilities import (ITaggingConfig, get_exif_fields,
    get_ignored_tags, get_iptc_fields, get_use_exif, get_use_iptc, get_use_title,
    get_test_image)
from inqbus.tagging.subscriber.functions import image_to_meta


class ITableRowFieldSchema(model.Schema):
    field = schema.TextLine(title=u"Field", required=True)
    format = schema.TextLine(title=u"Format String", required=False)
    regex = schema.TextLine(title=u"Regular Expression", required=False)


class ITableRowIgnoredSchema(model.Schema):
     tag = schema.TextLine(title=u"Tag", required=True)
     field = schema.TextLine(title=u"Field", required=False)


class ITaggingFormSchema(model.Schema):

    use_exif = schema.Bool(title = u"Use Exif",
                           defaultFactory=get_use_exif)

    use_iptc = schema.Bool(title = u"Use IPTC",
                           defaultFactory=get_use_iptc)

    use_title = schema.Bool(title = u"Use Title",
                            defaultFactory=get_use_title)

    exif_fields = schema.List(
            title=u"Exif Fields",
            defaultFactory=get_exif_fields,
            value_type=DictRow(
                    title=u"Fields",
                    schema=ITableRowFieldSchema,
                ),
            required=False,
        )

    iptc_fields = schema.List(
            title=u"IPTC Fields",
            defaultFactory=get_iptc_fields,
            value_type=DictRow(
                    title=u"Fields",
                    schema=ITableRowFieldSchema,
                ),
            required=False,
        )

    ignored_tags = schema.List(
            title=u"Ignored Tags",
            defaultFactory=get_ignored_tags,
            value_type=DictRow(
                    title=u"Tags",
                    schema=ITableRowIgnoredSchema,
                ),
            required=False,
        )

class TaggingForm(AutoExtensibleForm, form.Form):
    """ Define Form handling

    This form can be accessed as http://yoursite/@@my-form

    """
    schema = ITaggingFormSchema
    ignoreContext = True

    fields = field.Fields(ITaggingFormSchema)
    fields['exif_fields'].widgetFactory = DataGridFieldFactory
    fields['iptc_fields'].widgetFactory = DataGridFieldFactory
    fields['ignored_tags'].widgetFactory = DataGridFieldFactory

    label = u"What's your name?"
    description = u"Simple, sample form"

    @button.buttonAndHandler(u'Ok')
    def handleApply(self, action):
        data, errors = self.extractData()
        if errors:
            self.status = self.formErrorsMessage
            return

        config_store = getUtility(ITaggingConfig)

        for field in data:
            setattr(config_store, field, data[field])

        self.status = "Data was saved"

    @button.buttonAndHandler(u"Cancel")
    def handleCancel(self, action):
        """User cancelled. Redirect back to the front page.
        """


class TagSettingsView(BrowserView):
    """
    View which wrap the settings form using ControlPanelFormWrapper to a
    HTML boilerplate frame.
    """

    def __call__(self, *args, **kwargs):
        view_factor = layout.wrap_form(TaggingForm,
                                       ControlPanelFormWrapper)
        view = view_factor(self.context, self.request)
        return view()

class ITagImportExif(model.Schema):
    test_image = RelationChoice(title=u"Select EXIF-Tags from Image",
                               description=u"Here you can select an image to pick EXIF tags for the whitelists",
                               vocabulary="plone.app.vocabularies.Catalog",
                               required=False,
                               defaultFactory=get_test_image
                               )


class TagImportExifEditForm(AutoExtensibleForm, form.EditForm):
    """
    Define form logic
    """
    ignoreContext = True
    schema = ITagImportExif
    label = u"Inqbus Tagging Settings - Import Tags"


    def __init__(self, context, request):
        super(TagImportExifEditForm, self).__init__(context, request)

    def updateFields(self):
        super(TagImportExifEditForm, self).updateFields()
        config_store = getUtility(ITaggingConfig)
        test_image = config_store.test_image
        if test_image and test_image.portal_type and test_image.portal_type == 'Image':
            exif = image_to_meta(test_image)['exif']
            exif_keys = exif.keys()
            exif_keys.sort()
            for exif_key in exif_keys:
                exif_field = exif[exif_key]
                if str(exif_field) and len(str(exif_field)) < 100 :
                    self.fields += field.Fields(schema.Bool(
                                            __name__=exif_key,
                                            title=unicode(exif_key),
                                            description=unicode("Example: " +str(exif_field)),
                                            default=False))

    def applyChanges(self, data):
        config_store = getUtility(ITaggingConfig)
        for field in data:
            if field == 'test_image' and data['test_image']:
                config_store.test_image = data['test_image']
                self.context.REQUEST.RESPONSE.redirect(self.request["ACTUAL_URL"])
            elif data[field]:
                config_store.add_exif_tag(field)

    @button.buttonAndHandler(u'Ok')
    def handleApply(self, action):
        data, errors = self.extractData()
        if errors:
            self.status = self.formErrorsMessage
            return

        self.applyChanges(data)

        self.status = "Data was saved."

    @button.buttonAndHandler(u"Cancel")
    def handleCancel(self, action):
        """User cancelled. Redirect back to the front page."""


class TagImportExifView(BrowserView):
    """
    View which wrap the settings form using ControlPanelFormWrapper to a
    HTML boilerplate frame.
    """

    def __call__(self, *args, **kwargs):
        view_factor = layout.wrap_form(TagImportExifEditForm,
                                       ControlPanelFormWrapper)
        view = view_factor(self.context, self.request)
        return view()


class ITagImportIptc(ITagImportExif):
    test_image = RelationChoice(title=u"Select IPTC-Tags from Image",
                               description=u"Here you can select an image to pick IPTC tags for the whitelists",
                               vocabulary="plone.app.vocabularies.Catalog",
                               required=False,
                               defaultFactory=get_test_image
                               )


class TagImportIptcEditForm(TagImportExifEditForm):

    schema = ITagImportIptc
    def __init__(self, context, request):
        super(TagImportExifEditForm, self).__init__(context, request)

    def updateFields(self):
        super(TagImportExifEditForm, self).updateFields()
        config_store = getUtility(ITaggingConfig)
        test_image = config_store.test_image
        if test_image and test_image.portal_type and test_image.portal_type == 'Image':
            exif = image_to_meta(test_image)['iptc'].data
            exif_keys = exif.keys()
            exif_keys.sort()
            for exif_key in exif_keys:
                exif_field = exif[exif_key]
                if str(exif_field) and len(str(exif_field)) < 100 :
                    self.fields += field.Fields(schema.Bool(
                                            __name__=str(exif_key),
                                            title=unicode(exif_key),
                                            description=unicode("Example: " +str(exif_field)),
                                            default=False))

    def applyChanges(self, data):
        config_store = getUtility(ITaggingConfig)
        for field in data:
            if field == 'test_image' and data['test_image']:
                config_store.test_image = data['test_image']
                self.context.REQUEST.RESPONSE.redirect(self.request["ACTUAL_URL"])
            elif data[field]:
                config_store.add_iptc_tag(field)


class TagImportIptcView(BrowserView):
    """
    View which wrap the settings form using ControlPanelFormWrapper to a
    HTML boilerplate frame.
    """

    def __call__(self, *args, **kwargs):
        view_factor = layout.wrap_form(TagImportIptcEditForm,
                                       ControlPanelFormWrapper)
        view = view_factor(self.context, self.request)
        return view()