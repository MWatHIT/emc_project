#-*- coding: UTF-8 -*-
from five import grok
from zope.interface import implements
from zope.component import adapts
from Products.CMFCore.utils import getToolByName
from zope.interface import alsoProvides, Interface
from plone.directives import form
from zope import schema

from plone.formwidget.autocomplete.widget import AutocompleteMultiFieldWidget

from borg.localrole.interfaces import ILocalRoleProvider
from plone.indexer.interfaces import IIndexer
from Products.ZCatalog.interfaces import IZCatalog

from emc.project import  _

class Ilocalroles(form.Schema):
    """
    Description of the localroles
    source 字段不能有缺省值的
    """
    form.widget(emc_designer=AutocompleteMultiFieldWidget)    
    emc_designer = schema.Tuple(
        title=_(u"EMC Designer"),
        value_type=schema.Choice(title=_(u"User id"),
                                  source=u"plone.principalsource.Users"),
        required=False,
        missing_value=(), # important!
    )    
    form.widget(designer=AutocompleteMultiFieldWidget)
    designer = schema.Tuple(
        title=_(u"Product Designer"),
        value_type=schema.Choice(title=_(u"User id"),
                                  source=u"plone.principalsource.Users"),
        required=False,
        missing_value=(), # important!
    )
    form.widget(reader1=AutocompleteMultiFieldWidget)    
    reader1 = schema.Tuple(
        title=_(u"Commander"),
        value_type=schema.Choice(title=_(u"User id"),
                                  source=u"plone.principalsource.Users"),
        required=False,
        missing_value=(), # important!
    )
    form.widget(reader2=AutocompleteMultiFieldWidget)    
    reader2 = schema.Tuple(
        title=_(u"Deputy Commander"),
        value_type=schema.Choice(title=_(u"User id"),
                                  source=u"plone.principalsource.Users"),
        required=False,
        missing_value=(), # important!
    )
    form.widget(reader3=AutocompleteMultiFieldWidget)    
    reader3 = schema.Tuple(
        title=_(u"Chief Designer"),
        value_type=schema.Choice(title=_(u"User id"),
                                  source=u"plone.principalsource.Users"),
        required=False,
        missing_value=(), # important!
    )     
    form.widget(reader4=AutocompleteMultiFieldWidget)    
    reader4 = schema.Tuple(
        title=_(u"Deputy Chief Designer"),
        value_type=schema.Choice(title=_(u"User id"),
                                  source=u"plone.principalsource.Users"),
        required=False,
        missing_value=(), # important!
    )    
    form.widget(reader5=AutocompleteMultiFieldWidget)    
    reader5 = schema.Tuple(
        title=_(u"Chief quality engineer"),
        value_type=schema.Choice(title=_(u"User id"),
                                  source=u"plone.principalsource.Users"),
        required=False,
        missing_value=(), # important!
    ) 
    form.widget(reader6=AutocompleteMultiFieldWidget)    
    reader6 = schema.Tuple(
        title=_(u"Deputy Chief quality engineer"),
        value_type=schema.Choice(title=_(u"User id"),
                                  source=u"plone.principalsource.Users"),
        required=False,
        missing_value=(), # important!
    )
    form.widget(reader7=AutocompleteMultiFieldWidget)    
    reader7 = schema.Tuple(
        title=_(u"Deputy Chief Process"),
        value_type=schema.Choice(title=_(u"User id"),
                                  source=u"plone.principalsource.Users"),
        required=False,
        missing_value=(), # important!
    )       
    form.widget(reader8=AutocompleteMultiFieldWidget)    
    reader8 = schema.Tuple(
        title=_(u"process staff"),
        value_type=schema.Choice(title=_(u"User id"),
                                  source=u"plone.principalsource.Users"),
        required=False,
        missing_value=(), # important!
    )   
    form.widget(reader9=AutocompleteMultiFieldWidget)    
    reader9 = schema.Tuple(
        title=_(u"quality manage staff"),
        value_type=schema.Choice(title=_(u"User id"),
                                  source=u"plone.principalsource.Users"),
        required=False,
        missing_value=(), # important!
    )   
    form.widget(reader10=AutocompleteMultiFieldWidget)    
    reader10 = schema.Tuple(
        title=_(u"dispatch staff"),
        value_type=schema.Choice(title=_(u"User id"),
                                  source=u"plone.principalsource.Users"),
        required=False,
        missing_value=(), # important!
    )                               
 
    form.widget(reader11=AutocompleteMultiFieldWidget)    
    reader11 = schema.Tuple(
        title=_(u"EMC expert"),
        value_type=schema.Choice(title=_(u"User id"),
                                  source=u"plone.principalsource.Users"),
        required=False,
        missing_value=(), # important!
    )        
    form.fieldset(
                  'first',
                  label=_(u'The first members'),
                  fields=['reader1','reader2','reader3','reader4','reader5','reader6','reader7'],
                  )
    form.fieldset(
                  'second',
                  label=_(u'The second members'),
                  fields=['emc_designer','designer'],
                  ) 
    # the third members will be assigned EMCExpert role     
    form.fieldset(
                  'third',
                  label=_(u'The third members'),
                  fields=['reader8','reader9','reader10','reader11'],
                  )    

alsoProvides(Ilocalroles, form.IFormFieldProvider)
       
class IlocalrolesMarker(Interface):
    """Marker interface that will be provided by instances using the
    Ilocalroles behavior. The ILocalRoleProvider adapter is registered for
    this marker.
    """
    
class AddLocalRoles(grok.Adapter):
    
    grok.implements(ILocalRoleProvider)
    grok.context(IlocalrolesMarker)
    
    
    def __init__(self, context):
        self.context = context
        self.readers = set()
    
    def getreaders(self,start,end):
#         if self.readers != set(): return self.readers
        localrole = Ilocalroles(self.context, None)
        if localrole == None:return set()
        tp = set()
        for i in xrange(start,end):
            attrname = 'reader%s' % i

            item = getattr(localrole , attrname, ())
            if type(item) == type(''):
                tp.add(item)
            else:
            # set join set
                tp = set(getattr(localrole , attrname, ())) | tp

        return tp         
        
        
    def getRoles(self, principal_id):
        """If the user is in the list of Reviewers for this item, grant
        the reader, Editor and Contributor local roles.
        """
#        import pdb
#        pdb.set_trace()
        localrole = Ilocalroles(self.context, None)

        roles = set()
# the EMC designer will be assigned Manager role  
        if principal_id in localrole.emc_designer:
            roles.add('Manager')
            
# the product designer will be assigned Contributor and Editor roles
        if principal_id in localrole.designer:
            roles.add('Manager')
#             roles.add('Editor')
          
# the first members will be assigned Reader role            
        if principal_id in self.getreaders(1,8):
            roles.add('Reader')
# the third members will be assigned EMCExpert role            

        if principal_id in self.getreaders(8,12):
            roles.add('Reader')            
        return roles
        
    def getAllRoles(self):
        """Return a list of tuples (principal_id, roles), where roles is a
        list of roles for the given user id.
        """

        localrole = Ilocalroles(self.context, None)

        if localrole is None  or (not localrole.emc_designer  \
                                   and not localrole.designer and not self.getreaders(1,12)):
            return       


        for principal_id in localrole.emc_designer:
            yield (principal_id, ('Manager',),)

        for principal_id in localrole.designer:
            yield (principal_id, ('Manager',),)
        for principal_id in self.getreaders(1,8):
            yield (principal_id, ('Reader',),)
        for principal_id in self.getreaders(8,12):
            yield (principal_id, ('Reader',),)            

            
# class localrolesIndexer(grok.MultiAdapter):
#     """Catalog indexer for the 'localroles' index.
#     """
#     grok.implements(IIndexer)
#     grok.adapts(IlocalrolesMarker, IZCatalog)
#     grok.name('localManager')
#    
#     def __init__(self, context, catalog):
#         self.localroles = Ilocalroles(context)
#    
#     def __call__(self):
#         Manager = self.localroles.Manager or ()
#         return tuple(set(Manager))