# Help on cocoa.error (cocoa release 1.0)

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
import cocoa.error as ce
help(ce)
```

    Help on module cocoa.error in cocoa:
    
    NAME
        cocoa.error
    
    DESCRIPTION
        Project : CoCoA
        Date :    april-november 2020
        Authors : Olivier Dadoun, Julien Browaeys, Tristan Beau
        Copyright © CoCoa-team-17
        License: See joint LICENSE file
        
        Module : cocoa.error
        About : 
        
        Main class definitions for error management within the cocoa framework.
        All Cocoa exceptions should derive from the main CocoaError class.
    
    CLASSES
        builtins.Exception(builtins.BaseException)
            CocoaError
                CocoaConnectionError(CocoaError, builtins.ConnectionError)
                CocoaDbError
                CocoaKeyError(CocoaError, builtins.KeyError)
                CocoaLookupError(CocoaError, builtins.LookupError)
                CocoaNotManagedError
                CocoaTypeError(CocoaError, builtins.TypeError)
                CocoaWhereError(CocoaError, builtins.IndexError)
        
        class CocoaConnectionError(CocoaError, builtins.ConnectionError)
         |  CocoaConnectionError(message)
         |  
         |  Exception raised for connection errors.
         |  
         |  Attributes:
         |      message -- explanation of the error
         |  
         |  Method resolution order:
         |      CocoaConnectionError
         |      CocoaError
         |      builtins.ConnectionError
         |      builtins.OSError
         |      builtins.Exception
         |      builtins.BaseException
         |      builtins.object
         |  
         |  Methods defined here:
         |  
         |  __init__(self, message)
         |      Initialize self.  See help(type(self)) for accurate signature.
         |  
         |  ----------------------------------------------------------------------
         |  Data descriptors defined here:
         |  
         |  __weakref__
         |      list of weak references to the object (if defined)
         |  
         |  ----------------------------------------------------------------------
         |  Methods inherited from builtins.OSError:
         |  
         |  __reduce__(...)
         |      Helper for pickle.
         |  
         |  __str__(self, /)
         |      Return str(self).
         |  
         |  ----------------------------------------------------------------------
         |  Static methods inherited from builtins.OSError:
         |  
         |  __new__(*args, **kwargs) from builtins.type
         |      Create and return a new object.  See help(type) for accurate signature.
         |  
         |  ----------------------------------------------------------------------
         |  Data descriptors inherited from builtins.OSError:
         |  
         |  characters_written
         |  
         |  errno
         |      POSIX exception code
         |  
         |  filename
         |      exception filename
         |  
         |  filename2
         |      second exception filename
         |  
         |  strerror
         |      exception strerror
         |  
         |  ----------------------------------------------------------------------
         |  Methods inherited from builtins.BaseException:
         |  
         |  __delattr__(self, name, /)
         |      Implement delattr(self, name).
         |  
         |  __getattribute__(self, name, /)
         |      Return getattr(self, name).
         |  
         |  __repr__(self, /)
         |      Return repr(self).
         |  
         |  __setattr__(self, name, value, /)
         |      Implement setattr(self, name, value).
         |  
         |  __setstate__(...)
         |  
         |  with_traceback(...)
         |      Exception.with_traceback(tb) --
         |      set self.__traceback__ to tb and return self.
         |  
         |  ----------------------------------------------------------------------
         |  Data descriptors inherited from builtins.BaseException:
         |  
         |  __cause__
         |      exception cause
         |  
         |  __context__
         |      exception context
         |  
         |  __dict__
         |  
         |  __suppress_context__
         |  
         |  __traceback__
         |  
         |  args
        
        class CocoaDbError(CocoaError)
         |  CocoaDbError(message)
         |  
         |  Exception raised for database errors.
         |  
         |  Attributes:
         |      message -- explanation of the error
         |  
         |  Method resolution order:
         |      CocoaDbError
         |      CocoaError
         |      builtins.Exception
         |      builtins.BaseException
         |      builtins.object
         |  
         |  Methods defined here:
         |  
         |  __init__(self, message)
         |      Initialize self.  See help(type(self)) for accurate signature.
         |  
         |  ----------------------------------------------------------------------
         |  Data descriptors inherited from CocoaError:
         |  
         |  __weakref__
         |      list of weak references to the object (if defined)
         |  
         |  ----------------------------------------------------------------------
         |  Static methods inherited from builtins.Exception:
         |  
         |  __new__(*args, **kwargs) from builtins.type
         |      Create and return a new object.  See help(type) for accurate signature.
         |  
         |  ----------------------------------------------------------------------
         |  Methods inherited from builtins.BaseException:
         |  
         |  __delattr__(self, name, /)
         |      Implement delattr(self, name).
         |  
         |  __getattribute__(self, name, /)
         |      Return getattr(self, name).
         |  
         |  __reduce__(...)
         |      Helper for pickle.
         |  
         |  __repr__(self, /)
         |      Return repr(self).
         |  
         |  __setattr__(self, name, value, /)
         |      Implement setattr(self, name, value).
         |  
         |  __setstate__(...)
         |  
         |  __str__(self, /)
         |      Return str(self).
         |  
         |  with_traceback(...)
         |      Exception.with_traceback(tb) --
         |      set self.__traceback__ to tb and return self.
         |  
         |  ----------------------------------------------------------------------
         |  Data descriptors inherited from builtins.BaseException:
         |  
         |  __cause__
         |      exception cause
         |  
         |  __context__
         |      exception context
         |  
         |  __dict__
         |  
         |  __suppress_context__
         |  
         |  __traceback__
         |  
         |  args
        
        class CocoaError(builtins.Exception)
         |  CocoaError(message)
         |  
         |  Base class for exceptions in CoCoa.
         |  
         |  Method resolution order:
         |      CocoaError
         |      builtins.Exception
         |      builtins.BaseException
         |      builtins.object
         |  
         |  Methods defined here:
         |  
         |  __init__(self, message)
         |      Initialize self.  See help(type(self)) for accurate signature.
         |  
         |  ----------------------------------------------------------------------
         |  Data descriptors defined here:
         |  
         |  __weakref__
         |      list of weak references to the object (if defined)
         |  
         |  ----------------------------------------------------------------------
         |  Static methods inherited from builtins.Exception:
         |  
         |  __new__(*args, **kwargs) from builtins.type
         |      Create and return a new object.  See help(type) for accurate signature.
         |  
         |  ----------------------------------------------------------------------
         |  Methods inherited from builtins.BaseException:
         |  
         |  __delattr__(self, name, /)
         |      Implement delattr(self, name).
         |  
         |  __getattribute__(self, name, /)
         |      Return getattr(self, name).
         |  
         |  __reduce__(...)
         |      Helper for pickle.
         |  
         |  __repr__(self, /)
         |      Return repr(self).
         |  
         |  __setattr__(self, name, value, /)
         |      Implement setattr(self, name, value).
         |  
         |  __setstate__(...)
         |  
         |  __str__(self, /)
         |      Return str(self).
         |  
         |  with_traceback(...)
         |      Exception.with_traceback(tb) --
         |      set self.__traceback__ to tb and return self.
         |  
         |  ----------------------------------------------------------------------
         |  Data descriptors inherited from builtins.BaseException:
         |  
         |  __cause__
         |      exception cause
         |  
         |  __context__
         |      exception context
         |  
         |  __dict__
         |  
         |  __suppress_context__
         |  
         |  __traceback__
         |  
         |  args
        
        class CocoaKeyError(CocoaError, builtins.KeyError)
         |  CocoaKeyError(message)
         |  
         |  Exception raised for errors in used key option.
         |  
         |  Attributes:
         |      message -- explanation of the error
         |  
         |  Method resolution order:
         |      CocoaKeyError
         |      CocoaError
         |      builtins.KeyError
         |      builtins.LookupError
         |      builtins.Exception
         |      builtins.BaseException
         |      builtins.object
         |  
         |  Methods defined here:
         |  
         |  __init__(self, message)
         |      Initialize self.  See help(type(self)) for accurate signature.
         |  
         |  ----------------------------------------------------------------------
         |  Data descriptors inherited from CocoaError:
         |  
         |  __weakref__
         |      list of weak references to the object (if defined)
         |  
         |  ----------------------------------------------------------------------
         |  Methods inherited from builtins.KeyError:
         |  
         |  __str__(self, /)
         |      Return str(self).
         |  
         |  ----------------------------------------------------------------------
         |  Static methods inherited from builtins.LookupError:
         |  
         |  __new__(*args, **kwargs) from builtins.type
         |      Create and return a new object.  See help(type) for accurate signature.
         |  
         |  ----------------------------------------------------------------------
         |  Methods inherited from builtins.BaseException:
         |  
         |  __delattr__(self, name, /)
         |      Implement delattr(self, name).
         |  
         |  __getattribute__(self, name, /)
         |      Return getattr(self, name).
         |  
         |  __reduce__(...)
         |      Helper for pickle.
         |  
         |  __repr__(self, /)
         |      Return repr(self).
         |  
         |  __setattr__(self, name, value, /)
         |      Implement setattr(self, name, value).
         |  
         |  __setstate__(...)
         |  
         |  with_traceback(...)
         |      Exception.with_traceback(tb) --
         |      set self.__traceback__ to tb and return self.
         |  
         |  ----------------------------------------------------------------------
         |  Data descriptors inherited from builtins.BaseException:
         |  
         |  __cause__
         |      exception cause
         |  
         |  __context__
         |      exception context
         |  
         |  __dict__
         |  
         |  __suppress_context__
         |  
         |  __traceback__
         |  
         |  args
        
        class CocoaLookupError(CocoaError, builtins.LookupError)
         |  CocoaLookupError(message)
         |  
         |  Exception raised for type lookup errors.
         |  
         |  Attributes:
         |      message -- explanation of the error
         |  
         |  Method resolution order:
         |      CocoaLookupError
         |      CocoaError
         |      builtins.LookupError
         |      builtins.Exception
         |      builtins.BaseException
         |      builtins.object
         |  
         |  Methods defined here:
         |  
         |  __init__(self, message)
         |      Initialize self.  See help(type(self)) for accurate signature.
         |  
         |  ----------------------------------------------------------------------
         |  Data descriptors inherited from CocoaError:
         |  
         |  __weakref__
         |      list of weak references to the object (if defined)
         |  
         |  ----------------------------------------------------------------------
         |  Static methods inherited from builtins.LookupError:
         |  
         |  __new__(*args, **kwargs) from builtins.type
         |      Create and return a new object.  See help(type) for accurate signature.
         |  
         |  ----------------------------------------------------------------------
         |  Methods inherited from builtins.BaseException:
         |  
         |  __delattr__(self, name, /)
         |      Implement delattr(self, name).
         |  
         |  __getattribute__(self, name, /)
         |      Return getattr(self, name).
         |  
         |  __reduce__(...)
         |      Helper for pickle.
         |  
         |  __repr__(self, /)
         |      Return repr(self).
         |  
         |  __setattr__(self, name, value, /)
         |      Implement setattr(self, name, value).
         |  
         |  __setstate__(...)
         |  
         |  __str__(self, /)
         |      Return str(self).
         |  
         |  with_traceback(...)
         |      Exception.with_traceback(tb) --
         |      set self.__traceback__ to tb and return self.
         |  
         |  ----------------------------------------------------------------------
         |  Data descriptors inherited from builtins.BaseException:
         |  
         |  __cause__
         |      exception cause
         |  
         |  __context__
         |      exception context
         |  
         |  __dict__
         |  
         |  __suppress_context__
         |  
         |  __traceback__
         |  
         |  args
        
        class CocoaNotManagedError(CocoaError)
         |  CocoaNotManagedError(message)
         |  
         |  Exception raised when the error is unknown and not managed.
         |  
         |  Attributes:
         |      message -- explanation of the error
         |  
         |  Method resolution order:
         |      CocoaNotManagedError
         |      CocoaError
         |      builtins.Exception
         |      builtins.BaseException
         |      builtins.object
         |  
         |  Methods defined here:
         |  
         |  __init__(self, message)
         |      Initialize self.  See help(type(self)) for accurate signature.
         |  
         |  ----------------------------------------------------------------------
         |  Data descriptors inherited from CocoaError:
         |  
         |  __weakref__
         |      list of weak references to the object (if defined)
         |  
         |  ----------------------------------------------------------------------
         |  Static methods inherited from builtins.Exception:
         |  
         |  __new__(*args, **kwargs) from builtins.type
         |      Create and return a new object.  See help(type) for accurate signature.
         |  
         |  ----------------------------------------------------------------------
         |  Methods inherited from builtins.BaseException:
         |  
         |  __delattr__(self, name, /)
         |      Implement delattr(self, name).
         |  
         |  __getattribute__(self, name, /)
         |      Return getattr(self, name).
         |  
         |  __reduce__(...)
         |      Helper for pickle.
         |  
         |  __repr__(self, /)
         |      Return repr(self).
         |  
         |  __setattr__(self, name, value, /)
         |      Implement setattr(self, name, value).
         |  
         |  __setstate__(...)
         |  
         |  __str__(self, /)
         |      Return str(self).
         |  
         |  with_traceback(...)
         |      Exception.with_traceback(tb) --
         |      set self.__traceback__ to tb and return self.
         |  
         |  ----------------------------------------------------------------------
         |  Data descriptors inherited from builtins.BaseException:
         |  
         |  __cause__
         |      exception cause
         |  
         |  __context__
         |      exception context
         |  
         |  __dict__
         |  
         |  __suppress_context__
         |  
         |  __traceback__
         |  
         |  args
        
        class CocoaTypeError(CocoaError, builtins.TypeError)
         |  CocoaTypeError(message)
         |  
         |  Exception raised for type mismatch errors.
         |  
         |  Attributes:
         |      message -- explanation of the error
         |  
         |  Method resolution order:
         |      CocoaTypeError
         |      CocoaError
         |      builtins.TypeError
         |      builtins.Exception
         |      builtins.BaseException
         |      builtins.object
         |  
         |  Methods defined here:
         |  
         |  __init__(self, message)
         |      Initialize self.  See help(type(self)) for accurate signature.
         |  
         |  ----------------------------------------------------------------------
         |  Data descriptors inherited from CocoaError:
         |  
         |  __weakref__
         |      list of weak references to the object (if defined)
         |  
         |  ----------------------------------------------------------------------
         |  Static methods inherited from builtins.TypeError:
         |  
         |  __new__(*args, **kwargs) from builtins.type
         |      Create and return a new object.  See help(type) for accurate signature.
         |  
         |  ----------------------------------------------------------------------
         |  Methods inherited from builtins.BaseException:
         |  
         |  __delattr__(self, name, /)
         |      Implement delattr(self, name).
         |  
         |  __getattribute__(self, name, /)
         |      Return getattr(self, name).
         |  
         |  __reduce__(...)
         |      Helper for pickle.
         |  
         |  __repr__(self, /)
         |      Return repr(self).
         |  
         |  __setattr__(self, name, value, /)
         |      Implement setattr(self, name, value).
         |  
         |  __setstate__(...)
         |  
         |  __str__(self, /)
         |      Return str(self).
         |  
         |  with_traceback(...)
         |      Exception.with_traceback(tb) --
         |      set self.__traceback__ to tb and return self.
         |  
         |  ----------------------------------------------------------------------
         |  Data descriptors inherited from builtins.BaseException:
         |  
         |  __cause__
         |      exception cause
         |  
         |  __context__
         |      exception context
         |  
         |  __dict__
         |  
         |  __suppress_context__
         |  
         |  __traceback__
         |  
         |  args
        
        class CocoaWhereError(CocoaError, builtins.IndexError)
         |  CocoaWhereError(message)
         |  
         |  Exception raised for location errors.
         |  
         |  Attributes:
         |      message -- explanation of the error
         |  
         |  Method resolution order:
         |      CocoaWhereError
         |      CocoaError
         |      builtins.IndexError
         |      builtins.LookupError
         |      builtins.Exception
         |      builtins.BaseException
         |      builtins.object
         |  
         |  Methods defined here:
         |  
         |  __init__(self, message)
         |      Initialize self.  See help(type(self)) for accurate signature.
         |  
         |  ----------------------------------------------------------------------
         |  Data descriptors inherited from CocoaError:
         |  
         |  __weakref__
         |      list of weak references to the object (if defined)
         |  
         |  ----------------------------------------------------------------------
         |  Static methods inherited from builtins.IndexError:
         |  
         |  __new__(*args, **kwargs) from builtins.type
         |      Create and return a new object.  See help(type) for accurate signature.
         |  
         |  ----------------------------------------------------------------------
         |  Methods inherited from builtins.BaseException:
         |  
         |  __delattr__(self, name, /)
         |      Implement delattr(self, name).
         |  
         |  __getattribute__(self, name, /)
         |      Return getattr(self, name).
         |  
         |  __reduce__(...)
         |      Helper for pickle.
         |  
         |  __repr__(self, /)
         |      Return repr(self).
         |  
         |  __setattr__(self, name, value, /)
         |      Implement setattr(self, name, value).
         |  
         |  __setstate__(...)
         |  
         |  __str__(self, /)
         |      Return str(self).
         |  
         |  with_traceback(...)
         |      Exception.with_traceback(tb) --
         |      set self.__traceback__ to tb and return self.
         |  
         |  ----------------------------------------------------------------------
         |  Data descriptors inherited from builtins.BaseException:
         |  
         |  __cause__
         |      exception cause
         |  
         |  __context__
         |      exception context
         |  
         |  __dict__
         |  
         |  __suppress_context__
         |  
         |  __traceback__
         |  
         |  args
    
    FILE
        /home/beau/Dropbox/Git/dev_versions/CoCoA/cocoa/error.py
    
    



```python

```
