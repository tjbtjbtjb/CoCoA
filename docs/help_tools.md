# Help on cocoa.tools (cocoa release 1.0)

## Making CoCoA available
If executed locally


```python
import sys
sys.path.insert(1, '..')
```

If executed on a server (e.g. Google Colab ), you should install cocoa via pip3


```python
!pip3 install -q git+https://github.com/tjbtjbtjb/CoCoA.git
```


```python
import cocoa.tools as ct
help(ct)
```

    Help on module cocoa.tools in cocoa:
    
    NAME
        cocoa.tools
    
    DESCRIPTION
        Project : CoCoA - Copyright © CoCoa-team-17
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
    
    FUNCTIONS
        info(*args)
            Print to stdout with similar args as the builtin print function,
            if _verbose_mode > 0
        
        kwargs_test(given_args, expected_args, error_string)
            Test that the list of kwargs is compatible with expected args. If not
            it raises a CocoaKeyError with error_string.
        
        verb(*args)
            Print to stdout with similar args as the builtin print function,
            if _verbose_mode > 1
    
    FILE
        /home/beau/Dropbox/Git/dev_versions/CoCoA/cocoa/tools.py
    
    



```python

```
