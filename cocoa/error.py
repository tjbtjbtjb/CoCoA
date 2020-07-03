# -*- coding: utf-8 -*-
""" Project : CoCoA
Date :    april-july 2020
Authors : Olivier Dadoun, Julien Browaeys, Tristan Beau
Copyright © CoCoa-team-17
License: See joint LICENSE file

Module : cocoa.error
About : 

Main class definitions for error management within the cocoa framework.
All Cocoa exceptions should derive from the main CocoaError class.
"""

class CocoaError(Exception):
    """Base class for exceptions in CoCoa."""
    def __init__(self, message):
        self.message = message
        Exception(message)

class CocoaKeyError(CocoaError, KeyError):
    """Exception raised for errors in used key option.

    Attributes:
        message -- explanation of the error
    """
    def __init__(self, message):
        self.message = message
        KeyError(message)
        CocoaError(message)

class CocoaDbError(CocoaError):
    """Exception raised for database errors.

    Attributes:
        message -- explanation of the error
    """
    def __init__(self, message):
        self.message = message
        CocoaError(message)
        
class CocoaWhereError(CocoaError, IndexError):
    """Exception raised for location errors.

    Attributes:
        message -- explanation of the error
    """
    def __init__(self, message):
        self.message = message
        IndexError(message)
        CocoaError(message)
        
class CocoaTypeError(CocoaError, TypeError):
    """Exception raised for type mismatch errors.

    Attributes:
        message -- explanation of the error
    """
    def __init__(self, message):
        self.message = message
        TypeError(message)
        CocoaError(message)    
