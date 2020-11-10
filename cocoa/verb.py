# -*- coding: utf-8 -*-
"""Project : CoCoA - Copyright © CoCoa-team-17
Date :    april-june 2020
Authors : Olivier Dadoun, Julien Browaeys, Tristan Beau
License: See joint LICENSE file
About
-----
This is the CoCoA printing module for verbose or warning mode management.
The _verbose_mode should be set to 0 if no printing output needed. The
default value is 1 (print information to stdout)
"""

_verbose_mode = 1 # default

def info(*args):
    """Print to stdout with similar args as the builtin print function,
    if _verbose_mode > 0
    """
    if _verbose_mode > 0:
        print(*args)
        