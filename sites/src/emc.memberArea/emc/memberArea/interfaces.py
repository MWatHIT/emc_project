#-*- coding: UTF-8 -*-
from zope.component.interfaces import IObjectEvent
from zope.interface import Interface

class IMemberAreaCreatedEvent(IObjectEvent):
    """pass"""

class IMessageCreatedEvent(IObjectEvent):
    """pass"""


class IAddFavoriteEvent(IObjectEvent):
    """ Event add item favorite"""
    

    
class ISendMessageEvent(IObjectEvent):
    """ Event add item favorite"""

class IFavoriteEvent(IObjectEvent):
    """pass"""
class IUnFavoriteEvent(IObjectEvent):
    """pass"""
    
# Adapter interface for favorite functions
class IFavoriting(Interface):

        
    def number():
            """ 被多少人收藏了"""
            
    def addfavorite(userToken): 
        """add favoriter """
        
    def delfavorite(userToken): 
        """del favorite"""       

class IWorkspace(Interface):
    """Marker interface for personal root folder,using it define
    default view for root folder
    """

class IFavoritableLayer(Interface):
    """Marker interface for the Browserlayer
    """

# IFavoritable is the marker interface for contenttypes how support this behavior
class IFavoritable(Interface):
    pass

# class IFavoriting(Interface):
#     """mark interface"""
        
    
 