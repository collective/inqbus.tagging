from Products.Five.browser import BrowserView
from plone.app.registry.browser.controlpanel import ControlPanelFormWrapper
from plone.autoform.form import AutoExtensibleForm
from plone.supermodel import model
from plone.z3cform import layout
from z3c.form import field, button, form
from z3c.relationfield.schema import RelationChoice
from zope import schema
from zope.component import getUtility

from collective.z3cform.datagridfield import DataGridFieldFactory, DictRow
from inqbus.tagging.configuration.utilities import ITaggingConfig
from inqbus.tagging.functions import get_ignored_tags_form, get_test_image, \
    image_to_meta, get_tagging_config

from inqbus.tagging import MessageFactory as _


class ITableRowFieldSchema(model.Schema):
    field = schema.TextLine(title=_(u"EXIF Field"), required=True,
                            description=_(u'Add the name of the field.'))
    format = schema.TextLine(title=_(u"Format String"), required=False,
                             description=_(u'Add a format string to format the value or the cut out portion. Use unchanged value if nothing is set.'))
    regex = schema.TextLine(title=_(u"Regular Expression"), required=False,
                            description=_(u'Add Regular Expression to cut out a portion of the field value. Use all if nothing is set.'))


class ITableRowIgnoredSchema(model.Schema):
    tag = schema.TextLine(title=_(u"Tag"), required=True)


class FieldFactory(object):

    def __init__(self, field):
        self.field = field

    def __call__(self, *args, **kwargs):
        config_store = get_tagging_config()
        if config_store:
            return  getattr(config_store, self.field, None)
        return None


class ITaggingFormSchema(model.Schema):

    use_exif = schema.Bool(title = _(u"Use Exif"),
                           defaultFactory=FieldFactory('use_exif'),
                           description=_(u"Select if tags based on exif should be added."))

    use_iptc = schema.Bool(title = _(u"Use IPTC"),
                           defaultFactory=FieldFactory('use_iptc'),
                           description=_(u"Select if tags based on iptc should be added."))

    use_title = schema.Bool(title = u"Use Title",
                           defaultFactory=FieldFactory('use_title'),
                           description=_(u"Select if tags based on title should be added."))

    use_lowercase = schema.Bool(title = _(u"Use lowercased Title"),
                           defaultFactory=FieldFactory('use_lowercase'),
                           description=_(u"Select if field names should be compared lowercased."))

    exif_fields = schema.List(
            title=_(u"Exif Fields"),
            description=_(u"""List of the EXIF fields that are transformed into tags. You may specify a regular expression to cut out one or more portions of the EXIF value. Also you may specify a new style format string to shape the output of the exif value or the cut out portions.
Example: Value is "Newton, Issac", regex = "(\w+), (\w+)", format = "{1} {0}" -> Issac Newton"""),
            defaultFactory=FieldFactory('exif_fields'),
            value_type=DictRow(
                    title=_(u"Fields"),
                    schema=ITableRowFieldSchema,
                ),
            required=False,
        )

    iptc_fields = schema.List(
            title=_(u"IPTC Fields"),
            description=_(u"""List of the IPTC fields that are transformed into tags. You may specify a regular expression to cut out a portion of the IPTC value. Also you may specify a format string to shape the output of the exif value or the cut out portion."""),
            defaultFactory=FieldFactory('iptc_fields'),
            value_type=DictRow(
                    title=_(u"Fields"),
                    schema=ITableRowFieldSchema,
                ),
            required=False,
        )

    ignored_tags = schema.List(
            title=_(u"Ignored Title Tags"),
            description=_(u"List of Tags that are ignored, if importing the title to tags."),
            defaultFactory=get_ignored_tags_form,
            value_type=DictRow(
                    title=_(u"Tags"),
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

    label = _(u"Inqbus.tagging EXIF Config")
    description = _(u"Here you can specify if and which exif information is tranlated into tags")

    @button.buttonAndHandler(u'Ok')
    def handleApply(self, action):
        data, errors = self.extractData()
        if errors:
            self.status = self.formErrorsMessage
            return

        config_store = get_tagging_config()

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
    test_image = RelationChoice(title=_(u"Select EXIF-Tags from Image"),
                               description=_(u"Here you can select an image to pick EXIF tags for the whitelists"),
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
    label = _(u"Inqbus Tagging Settings - Import Tags")


    def __init__(self, context, request):
        super(TagImportExifEditForm, self).__init__(context, request)

    def updateFields(self):
        super(TagImportExifEditForm, self).updateFields()
        config_store = get_tagging_config()
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
        config_store = get_tagging_config()
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
    test_image = RelationChoice(title=_(u"Select IPTC-Tags from Image"),
                               description=_(u"Here you can select an image to pick IPTC tags for the whitelists"),
                               vocabulary="plone.app.vocabularies.Catalog",
                               required=False,
                               defaultFactory=get_test_image
                               )


class TagImportIptcEditForm(TagImportExifEditForm):

    schema = ITagImportIptc
    label = _(u"Inqbus Tagging Settings - Import Tags")

    def __init__(self, context, request):
        super(TagImportExifEditForm, self).__init__(context, request)

    def updateFields(self):
        super(TagImportExifEditForm, self).updateFields()
        config_store = get_tagging_config()
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
        config_store = get_tagging_config()
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