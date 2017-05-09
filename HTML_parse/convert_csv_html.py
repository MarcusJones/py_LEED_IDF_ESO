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

from utility_inspect import whoami, whosdaddy, listObject
from utility_excel import ExcelBookAPI
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
# Unit testing
#===============================================================================

class allTests(unittest.TestCase):

    def setUp(self):
        print("**** TEST {} ****".format(whoami()))

        curr_path = os.path.dirname(os.path.realpath(__file__))
        curr_path = os.path.abspath(curr_path + "\..\..\ExcelTemplates\Table test.xlsx")
        with ExcelBookAPI(curr_path) as this_excel:

            sheet_names = this_excel.get_sheet_names()

            for name in sheet_names:
                this_table = this_excel.getTable(name)
                if not this_table:
                    continue



                this_name = this_table.pop(0).pop(0)
                print('<b>{}</b><br><br>'.format(this_name))
                this_fullname = this_table.pop(0).pop(0)
                print('<!-- FullName:{}-->'.format(this_fullname))
                print('<table border="1" cellpadding="4" cellspacing="0">')
                print('  <tr><td></td>')
                #this_table = zip(*this_table)
                flg_first = True
                for col in this_table:
                    if not flg_first:
                        print("  <tr>")
                    for item in col:
                        if not flg_first:
                            print(wrap_cell(item))
                        flg_first = False
                    print("  </tr>")
                print('</table>')
                #print(this_table)
        #print(this_excel.get_sheet_names())

        #print(curr_path)
        #raise
        #print(os.path.dirname(os.path.realpath(__file__)))

        print(wrap_cell(6))
        print(wrap_cell("hi"))


    def test010_SimpleCreation(self):
        print("**** TEST {} ****".format(whoami()))

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
