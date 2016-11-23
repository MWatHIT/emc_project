#-*- coding: UTF-8 -*-
import json
import hmac
from hashlib import sha1 as sha
from Products.CMFCore.utils import getToolByName
from emc.memberArea.testing import FUNCTIONAL_TESTING  

from zope.component import getUtility
from zope.interface import alsoProvides
from plone.keyring.interfaces import IKeyManager

from plone.app.testing import TEST_USER_ID, login, TEST_USER_NAME, \
    TEST_USER_PASSWORD, setRoles
from plone.testing.z2 import Browser
import unittest
from plone.namedfile.file import NamedImage
import os

def getFile(filename):
    """ return contents of the file with the given name """
    filename = os.path.join(os.path.dirname(__file__), filename)
    return open(filename, 'r')

class TestView(unittest.TestCase):
    
    layer = FUNCTIONAL_TESTING

    def setUp(self):
        portal = self.layer['portal']
        setRoles(portal, TEST_USER_ID, ('Manager',))
        portal.invokeFactory('emc.memberArea.workspace', 'work1')
        portal['work1'].invokeFactory('emc.memberArea.messagebox', 'folder1')
        portal['work1'].invokeFactory('emc.memberArea.myfolder', 'my1')
        portal['work1'].invokeFactory('emc.memberArea.todo', 'to1',title="todo items")
        portal['work1'].invokeFactory('emc.memberArea.favorite', 'fa1',title="favorite items")                
        portal['work1']['folder1'].invokeFactory('emc.memberArea.inputbox', 'input1')
        portal['work1']['folder1'].invokeFactory('emc.memberArea.outputbox', 'output1')
        portal['work1']['folder1']['input1'].invokeFactory('emc.memberArea.message', 'message1')
        portal['work1']['folder1']['output1'].invokeFactory('emc.memberArea.message', 'message1')                      

        self.portal = portal   
        
    def test_ajax_search(self):
        request = self.layer['request']
        from emc.theme.interfaces import IThemeSpecific
        alsoProvides(request, IThemeSpecific)        
        keyManager = getUtility(IKeyManager)
        secret = keyManager.secret()
        auth = hmac.new(secret, TEST_USER_NAME, sha).hexdigest()
        request.form = {
                        '_authenticator': auth,
                        'start': 0,
                        'size':10 ,
                        'datetype':'1',                                                
                        'province': '1',
                        'type': '1',
                        'sortcolumn':'created',
                        'sortdirection':'reverse',
                        'searchabletext':'orgnization1',
                                                                       
                        }
# Look up and invoke the view via traversal
        box = self.portal['work1']['folder1']
        view = box.restrictedTraverse('@@message_ajax')
        result = view()
        self.assertEqual(json.loads(result)['total'],2)
        
    def test_load_more(self):
        request = self.layer['request']
        from emc.theme.interfaces import IThemeSpecific
        alsoProvides(request, IThemeSpecific)        
        keyManager = getUtility(IKeyManager)
        secret = keyManager.secret()
        auth = hmac.new(secret, TEST_USER_NAME, sha).hexdigest()
        request.form = {
                        '_authenticator': auth,
                        'formstart':0,
                        'start': 0,
                        'size':10 ,
                        'datetype':'1',                                                
                        'province': '1',
                        'type': '1',
                        'sortcolumn':'created',
                        'sortdirection':'reverse',
                        'searchabletext':'orgnization1',
                                                                       
                        }
# Look up and invoke the view via traversal
        box = self.portal['work1']['folder1']
        view = box.restrictedTraverse('@@more')
        result = view()
        self.assertEqual(json.loads(result)['ifmore'],1)        

    def test_message_status_switch(self):
        request = self.layer['request']
        from emc.theme.interfaces import IThemeSpecific
        alsoProvides(request, IThemeSpecific)        
        keyManager = getUtility(IKeyManager)
        secret = keyManager.secret()
        auth = hmac.new(secret, TEST_USER_NAME, sha).hexdigest()
        request.form = {
                        '_authenticator': auth,
                        'id':'message1',
                        'state': "unreaded",                                                                       
                        }
# Look up and invoke the view via traversal
        box = self.portal['work1']['folder1']['input1']['message1']
        view = box.restrictedTraverse('@@ajaxmessagestate')
        result = view()
        self.assertEqual(json.loads(result),True)  
             

