import json
from plone import api
from plone.app.content.browser.contents import FolderContentsView
from plone.app.content.browser.file import TUS_ENABLED
from plone.app.content.utils import json_dumps
from plone.app.registry.browser.controlpanel import RegistryEditForm, \
    ControlPanelFormWrapper
from plone.autoform.form import AutoExtensibleForm
from plone.namedfile.interfaces import IImage

from plone.registry.interfaces import IRegistry
from plone.uuid.interfaces import IUUID
from Products.CMFCore.utils import getToolByName
from Products.CMFPlone import PloneMessageFactory as _
from Products.Five.browser import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from Products.PloneKeywordManager.browser.prefs_keywords_view import PrefsKeywordsView
from zope import schema
from zope.component import getUtility
from zope.component.hooks import getSite
from zope.i18n import translate
from plone.z3cform import layout
from z3c.form import form, field

from inqbus.tagging import logger
from inqbus.tagging.config import TEST_IMAGE_SETTINGS_KEY
from inqbus.tagging.interfaces import ITagSettingsView
from inqbus.tagging.subscriber.functions import image_to_meta


class OwnFolderContentsView(FolderContentsView):

    def __call__(self):
        site = getSite()
        base_url = site.absolute_url()
        base_vocabulary = '%s/@@getVocabulary?name=' % base_url
        site_path = site.getPhysicalPath()
        context_path = self.context.getPhysicalPath()
        options = {
            'vocabularyUrl': '%splone.app.vocabularies.Catalog' % (
                base_vocabulary),
            'urlStructure': {
                'base': base_url,
                'appended': '/folder_contents'
            },
            'moveUrl': '%s{path}/fc-itemOrder' % base_url,
            'indexOptionsUrl': '%s/@@qsOptions' % base_url,
            'contextInfoUrl': '%s{path}/@@fc-contextInfo' % base_url,
            'setDefaultPageUrl': '%s{path}/@@fc-setDefaultPage' % base_url,
            'availableColumns': {
                'id': translate(_('ID'), context=self.request),
                'preview': translate(_('Preview'), context=self.request),
                'ModificationDate': translate(_('Last modified'), context=self.request),  # noqa
                'EffectiveDate': translate(_('Publication date'), context=self.request),  # noqa
                'CreationDate': translate(_('Created on'), context=self.request),  # noqa
                'review_state': translate(_('Review state'), context=self.request),  # noqa
                'Subject': translate(_('Tags'), context=self.request),
                'Type': translate(_('Type'), context=self.request),
                'is_folderish': translate(_('Folder'), context=self.request),
                'exclude_from_nav': translate(_('Excluded from navigation'), context=self.request),  # noqa
                'getObjSize': translate(_('Object Size'), context=self.request),  # noqa
                'last_comment_date': translate(_('Last comment date'), context=self.request),  # noqa
                'total_comments': translate(_('Total comments'), context=self.request),  # noqa
            },
            'buttons': self.get_actions(),
            'rearrange': {
                'properties': {
                    'id': translate(_('Id'), context=self.request),
                    'sortable_title': translate(_('Title'), context=self.request),  # noqa
                    'modified': translate(_('Last modified'), context=self.request),  # noqa
                    'created': translate(_('Created on'), context=self.request),  # noqa
                    'effective': translate(_('Publication date'), context=self.request),  # noqa
                    'Type': translate(_('Type'), context=self.request)
                },
                'url': '%s{path}/@@fc-rearrange' % base_url
            },
            'basePath': '/' + '/'.join(context_path[len(site_path):]),
            'upload': {
                'relativePath': 'fileUpload',
                'baseUrl': base_url,
                'initialFolder': IUUID(self.context, None),
                'useTus': TUS_ENABLED
            }
        }
        self.options = json_dumps(options)
        return super(FolderContentsView, self).__call__()

    def json_response(self, data):
        self.request.response.setHeader("Content-type", "application/json")
        return json.dumps(data)

    def image_html(self):

        image_uid = self.request.get('uid')

        image = api.content.get(UID=image_uid)
        if image:
            html = '<img src=%s />' % (
                image.absolute_url()+"/@@images/image/mini")
        else:
            html = ''

        return self.json_response({'html': html})


class KeywordManagerView(PrefsKeywordsView):

    template = ViewPageTemplateFile('templates/keyword_manager_view.pt')

    def doReturn(self, message='', msg_type='', field=''):
        """
        set the message and return
        """
        if message and msg_type:
            pu = getToolByName(self.context, "plone_utils")
            pu.addPortalMessage(message, type=msg_type)

        logger.info(self.context.translate(message))
        portal_url = self.context.portal_url()
        url = "%s/keyword_manager_view" % portal_url

        field = self.request.get('field', '')
        limit = self.request.get('limit', '')
        search = self.request.get('search', '')

        if field or limit or search:
            url = "%s?field=%s&search=%s&limit=%s" % (url, field, search,
                                                      limit)

        self.request.RESPONSE.redirect(url)


# class TagSettingsEditForm(RegistryEditForm):
#     """
#     Define form logic
#     """
#     schema = ITagSettings
#     label = u"Inqbus Tagging Settings"

class TagSettingsEditForm(AutoExtensibleForm, form.EditForm):
    """
    Define form logic
    """
    ignoreContext = True
    schema = ITagSettingsView
    label = u"Inqbus Tagging Settings"


    def __init__(self, context, request):
        super(TagSettingsEditForm, self).__init__(context, request)

    def updateFields(self):
        super(TagSettingsEditForm, self).updateFields()
        registry = getUtility(IRegistry)
        if registry[TEST_IMAGE_SETTINGS_KEY]:
            obj_uid = registry[TEST_IMAGE_SETTINGS_KEY]
            obj = api.content.get(UID=obj_uid)
            if obj.portal_type and obj.portal_type == 'Image':
                exif = image_to_meta(obj)['exif']
                exif_keys = exif.keys()
                exif_keys.sort()
                for exif_key in exif_keys:
                    if exif_key :
                        exif_field = exif[exif_key]
                        if str(exif_field) and len(str(exif_field)) < 100 :
                            try:
                                self.fields += field.Fields(schema.Bool(
                                                        __name__ = exif_key,
                                                        title= _(exif_key + " : " +str(exif_field)),
                                                        required=False,
                                                        default=False))
                            except:
                                pass

    def applyChanges(self, data):
        registry = getUtility(IRegistry)
        registry[TEST_IMAGE_SETTINGS_KEY] = unicode(data['test_image'].UID())
        pass


class TagSettingsView(BrowserView):
    """
    View which wrap the settings form using ControlPanelFormWrapper to a
    HTML boilerplate frame.
    """

    def __call__(self, *args, **kwargs):
        view_factor = layout.wrap_form(TagSettingsEditForm,
                                       ControlPanelFormWrapper)
        view = view_factor(self.context, self.request)
        return view()