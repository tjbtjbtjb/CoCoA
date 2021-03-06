# -*- coding: utf-8 -*-
"""Project : CoCoA - Copyright © CoCoa-team-17
Date :    april-november 2020
Authors : Olivier Dadoun, Julien Browaeys, Tristan Beau
License: See joint LICENSE file
About
-----
This is the CoCoA tools module to be considered as a swiss knife list of functions.
One find function for 
 - verbose or warning mode management.
 - kwargs analysis 

The _verbose_mode variable should be set to 0 if no printing output needed. The
default value is 1 (print information to stdout). The 2 value grants a debug level information
printing.
"""

from cocoa.error import CocoaKeyError

_verbose_mode = 1 # default

def info(*args):
    """Print to stdout with similar args as the builtin print function,
    if _verbose_mode > 0
    """
    if _verbose_mode > 0:
        print(*args)
        
def verb(*args):
    """Print to stdout with similar args as the builtin print function,
    if _verbose_mode > 1
    """
    if _verbose_mode > 1:
        print(*args)
        
def kwargs_test(given_args,expected_args,error_string):
    """Test that the list of kwargs is compatible with expected args. If not
    it raises a CocoaKeyError with error_string.
    """

    if type(given_args)!=dict:
        raise CocoaKeyError("kwargs_test error, the given args are not a dict type.")
    if type(expected_args)!=list:
        raise CocoaKeyError("kwargs_test error, the expected args are not a list type")

    bad_kwargs=[a for a in list(given_args.keys()) if a not in expected_args ]
    if len(bad_kwargs) != 0 :
        raise CocoaKeyError(error_string+' Unrecognized args are '+str(bad_kwargs)+'.')

    return True