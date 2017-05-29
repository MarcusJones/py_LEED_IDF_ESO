#===============================================================================
# Title of this Module
# Authors; MJones, Other
# 00 - 2012FEB05 - First commit
# 01 - 2012MAR17 - Update to ...
#===============================================================================

"""This module does A and B.
Etc.
"""

#===============================================================================
# Set up
#===============================================================================
# Standard:
from __future__ import division
from __future__ import print_function

from config import *

import logging.config
import unittest

from utility_inspect import get_self, get_parent, list_object
from utility_excel_api import ExtendedExcelBookAPI
#===============================================================================
# Code
#===============================================================================
def wrap_cell(item):
    """Return the something to the something."""
    pad = 12

    if not item:
        item = '&nbsp;'
        pad = 0

    if type(item) == str or type(item) == unicode:
        return '    <td align="right">{:>{}}</td>'.format(item,pad)

    #print(type(item))
    item = '{:.2f}'.format(item)
    return '    <td align="right">{:>{}}</td>'.format(item,pad)


#===============================================================================
# Main
#===============================================================================
if __name__ == "__main__":
    print(ABSOLUTE_LOGGING_PATH)
    logging.config.fileConfig(ABSOLUTE_LOGGING_PATH)


    myLogger = logging.getLogger()
    myLogger.setLevel("DEBUG")

    logging.debug("Started _main".format())

    #print FREELANCE_DIR

    unittest.main()

    logging.debug("Finished _main".format())
