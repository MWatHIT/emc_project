#-*- coding: UTF-8 -*-
from zope import interface
from zope.component.interfaces import ObjectEvent
from emc.memberArea.interfaces import IMemberAreaCreatedEvent
from emc.memberArea.interfaces import IAddFavoriteEvent
from emc.memberArea.interfaces import ISendMessageEvent,IMessageCreatedEvent
from emc.memberArea.interfaces import IFavoriteEvent,IUnFavoriteEvent
from zope.lifecycleevent import ObjectCreatedEvent

class MemberAreaCreatedEvent(ObjectEvent):
    interface.implements(IMemberAreaCreatedEvent)

class AddFavoriteEvent(ObjectEvent):
    interface.implements(IAddFavoriteEvent)

class SendMessageEvent(ObjectEvent):
    interface.implements(ISendMessageEvent)
 
class MessageCreatedEvent(ObjectCreatedEvent):
    interface.implements(IMessageCreatedEvent)
    
class FavoriteEvent(ObjectEvent):
    """收藏事件"""
    interface.implements(IFavoriteEvent)

class UnFavoriteEvent(ObjectEvent):
    """取消收藏事件"""    
    interface.implements(IUnFavoriteEvent)                 