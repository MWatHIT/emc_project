#-*- coding: UTF-8 -*-
from five import grok
from zope import schema
from plone.directives import form, dexterity
from plone.app.dexterity.behaviors.metadata import IBasic

from collective import dexteritytextindexer
from collective.dexteritytextindexer.behavior import IDexterityTextIndexer
from plone.formwidget.autocomplete.widget import AutocompleteMultiFieldWidget
from emc.memberArea import _
    
class IMessage(form.Schema):
    """
    emc project member area message content type
    """
#标准名称
    dexteritytextindexer.searchable('title')    
    title = schema.TextLine(title=_(u"site message title"),
            required=True)

    form.widget(text="plone.app.z3cform.wysiwyg.WysiwygFieldWidget")
    text = schema.Text(
        title=_(u"message text"),
        required=True)
    form.widget(sendto=AutocompleteMultiFieldWidget)    
    sendto = schema.Tuple(
        title=_(u"send to"),
        value_type=schema.Choice(title=_(u"send to"),
                                  source=u"plone.principalsource.Users"),
        required=True,
        missing_value=(), # important!
    )           

@form.validator(field=IMessage['text'])
def maxSize(value):
    if value is not None:
        if len(value)/1024 > 128:
            raise schema.ValidationError(_(u"message text must be smaller than 128KB"))
 
