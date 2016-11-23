#-*- coding: UTF-8 -*-
from plone import api
from five import grok
from zope.interface import alsoProvides
from AccessControl import ClassSecurityInfo, getSecurityManager
from AccessControl.SecurityManagement import newSecurityManager, setSecurityManager
from emc.memberArea.interfaces import IMemberAreaCreatedEvent,IMessageCreatedEvent

from Products.CMFCore.utils import getToolByName
from plone.dexterity.utils import createContentInContainer
# from Products.PluggableAuthService.interfaces.authservice import IPropertiedUser
from zope.interface import Interface

from zope.lifecycleevent.interfaces import IObjectAddedEvent
from emc.memberArea.content.message import IMessage
from emc.memberArea.interfaces import IWorkspace
from emc.memberArea.utils import UnrestrictedUser

# @grok.subscribe(IPropertiedUser,IMemberAreaCreatedEvent)
@grok.subscribe(Interface,IMemberAreaCreatedEvent)
def create_messagebox(obj,event):
    """创建个人信箱"""
    pm = getToolByName(obj,'portal_membership')
    root = pm.getHomeFolder(pm.getAuthenticatedMember().getId())
    if root is None: return
# bypass permission check
    old_sm = getSecurityManager()
    portal = api.portal.get()

    tmp_user = UnrestrictedUser(old_sm.getUser().getId(),'', ['Manager'],'')        
    tmp_user = tmp_user.__of__(portal.acl_users)
    newSecurityManager(None, tmp_user)    
    id = 'workspace'
    fd = createContentInContainer(root,"emc.memberArea.workspace",checkConstraints=False,id=id)
    fd.title = u'个人工作区'.encode("utf-8")
                 
    id = 'messagebox'
    item = createContentInContainer(fd,"emc.memberArea.messagebox",checkConstraints=False,id=id)
    item.title = u'个人信箱'.encode("utf-8")
    item.reindexObject()
    inputbox = createContentInContainer(item,"emc.memberArea.inputbox",checkConstraints=False,id="inputbox")
#     inputbox.id = "inputbox"
    inputbox.title = u'收件箱'.encode("utf-8")
    inputbox.reindexObject()
    outputbox = createContentInContainer(item,"emc.memberArea.outputbox",checkConstraints=False,id="outputbox")
#     outputbox.id = "outputbox"
    outputbox.title = u'发件箱'.encode("utf-8")
    outputbox.reindexObject()
    id = 'myfolder'
    item = createContentInContainer(fd,"emc.memberArea.myfolder",checkConstraints=False,id=id)
    item.title = u'个人网盘'.encode("utf-8")
    item.reindexObject()
    id = 'todo'
    item = createContentInContainer(fd,"emc.memberArea.todo",checkConstraints=False,id=id)
    item.title = u'代办事宜'.encode("utf-8")
    item.reindexObject()  
    id = 'favorite'
    item = createContentInContainer(fd,"emc.memberArea.favorite",checkConstraints=False,id=id)
    item.title = u'我的收藏'.encode("utf-8")
    item.reindexObject()
    # recover old sm
    setSecurityManager(old_sm)               

def get_personal_inputbox_byid(obj,id):
    pm = getToolByName(obj,'portal_membership')
    hf = pm.getHomeFolder(id)
    box = hf['workspace']['messagebox']['inputbox']    
    return box

@grok.subscribe(IMessage,IMessageCreatedEvent)
def dispatch_message(obj,event):
    """This handler will deliver message to incoming box of receivers""" 
    receivers = obj.sendto

# bypass permission check
    old_sm = getSecurityManager()
    tmp_user = UnrestrictedUser(old_sm.getUser().getId(),'', ['Manager'],'')
    portal = api.portal.get()        
    tmp_user = tmp_user.__of__(portal.acl_users)
    newSecurityManager(None, tmp_user)    
    for i in receivers:
        inputbox = get_personal_inputbox_byid(obj,i)
        api.content.copy(source=obj, target=inputbox)
        id = obj.id

        # message init state is unreaded status
#         api.content.transition(obj=inputbox[id], transition='undo')
        inputbox[id].reindexObject()
    # recover old sm
    setSecurityManager(old_sm)

         

