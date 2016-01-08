from collective.z3cform.datagridfield import DataGridFieldFactory, DictRow
from collective.z3cform.datagridfield import DataGridField

from plone.supermodel import model
from plone.autoform import directives
from plone.autoform.form import AutoExtensibleForm

from zope import schema
from z3c.form import field, button, form


class ITableRowSchema(model.Schema):
    one = schema.TextLine(title=u"One")
    two = schema.TextLine(title=u"Two")
    three = schema.TextLine(title=u"Three")


class IFormSchema(model.Schema):
    four = schema.TextLine(title=u"Four")

    # directives.widget('functies', DataGridField)
    # directives.widget('functies', DataGridFieldFactory)
    functies = schema.List(
            title=u"Functies",
            default=[],
            value_type=DictRow(
                    title=u"Functies",
                    schema=ITableRowSchema,
                ),
            required=False,
        )


class MyForm(AutoExtensibleForm, form.Form):
    """ Define Form handling

    This form can be accessed as http://yoursite/@@my-form

    """
    schema = IFormSchema
    ignoreContext = True

    # fields = field.Fields(IFormSchema)
    # fields['functies'].widgetFactory = DataGridFieldFactory

    label = u"What's your name?"
    description = u"Simple, sample form"

    @button.buttonAndHandler(u'Ok')
    def handleApply(self, action):
        data, errors = self.extractData()
        if errors:
            self.status = self.formErrorsMessage
            return

        # Do something with valid data here

        # Set status on this form page
        # (this status message is not bind to the session and does not go thru redirects)
        self.status = "Thank you very much!"

    @button.buttonAndHandler(u"Cancel")
    def handleCancel(self, action):
        """User cancelled. Redirect back to the front page.
        """