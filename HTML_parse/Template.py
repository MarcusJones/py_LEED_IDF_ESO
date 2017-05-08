"""This is a regular module
"""

#===============================================================================
# Set up
#===============================================================================
# Standard:



# Logging
import logging

# External 
#import xxx

# Own
#from utility_inspect import get_self, get_parent

#===============================================================================
# Code
#===============================================================================
class MyClass(object):
    """This class does something for someone.
    """
    def __init__(self, aVariable):
        pass

class MySubClass(MyClass):
    """This class does

    """
    def __init__(self, aVariable):
        super(MySubClass,self).__init__(aVariable)
    def a_method(self):
        """Return the something to the something."""
        pass

def some_function():
    """Return the something to the something."""
    pass
