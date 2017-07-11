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

from config import *

import logging.config
import unittest

from utility_inspect import get_self, get_parent, list_object
import utility_inspect as util_insp
from UtilityLogger import loggerCritical
import idf_xml.IDF as idf
from utility_path import erase_dir_contents,count_files,count_dirs,split_up_path
import re
from UtilityGUI import simpleYesNo
import csv
import xlrd as xlrd
import utility_path as util_path

#===============================================================================
# Code
#===============================================================================

def split_cell_address(address):
    return address.split('$')[1:]

def parse_range(range_string):
    print(range_string),
    named_range = dict()
    named_range['formula'] =range_string
     
    sheet_name =  range_string.split('!')[0]
    # Strip the quotes
    #sheet_name = sheet_name[1:-1]
    named_range['sheet'] =sheet_name
    
    cell_ref = range_string.split('!')[1]
    named_range['address'] =cell_ref
    
    split_ref = cell_ref.split(':')
    
    if len(split_ref) == 1:
        single_cell_address = split_ref[0]
        single_cell_address = split_cell_address(single_cell_address) 
        #print('Single range', single_cell_address)
        named_range['type'] ='single'
        named_range['col'] =single_cell_address[0]
        named_range['row'] =single_cell_address[1]
        
    elif len(split_ref) == 2:
        named_range['type'] ='table'
        topleft = split_cell_address(split_ref[0])
        named_range['leftcol'] =topleft[0]
        named_range['toprow'] =topleft[1]

        botright = split_cell_address(split_ref[1])
        named_range['rightcol'] =botright[0]
        named_range['botrow'] =botright[1]
    
    return named_range

def get_named_range(path_excel):
    pass

#===============================================================================
# Unit testing
#===============================================================================

class allTests(unittest.TestCase):

    def setUp(self):
        print "**** TEST {} ****".format(get_self())

    def test010_SimpleCreation(self):
        print "**** TEST {} ****".format(get_self())
        path_input_file = r'D:\Projects\081_Central_Admin2\06 Project'
        excel_path = util_path.get_latest_rev(path_input_file, r"^Input Data", ext_pat = "xlsx")
        
        #path_input_file = r'C:\Users\jon\Desktop\Energy Efficiency Kosovo\038-PRI-Ministry_of_culture\3 Analysis'
        #excel_path = util_path.get_latest_rev(path_input_file, r"^038", ext_pat = "xlsx")

        
        print(excel_path)
        #logging.info("Wrote the {0} variants to the group simulation file at: {1}".format(len(variantsList),groupFilePath))
        #print(xlrd)
        wb = xlrd.open_workbook(excel_path)
        logging.info("Opened book at {} ".format(excel_path))        
        print(wb.name_map)
        for name,name_list in wb.name_map.iteritems():
            if len(name_list) > 1:
                print("Skip {}".format(name))
            name_obj = name_list[0]
            this_name = name_obj.name

            target_range = parse_range(name_obj.formula_text)
            print("Name: {}, target: {} ".format(name_obj.name, name_obj.formula_text,target_range,))
            #print(name_obj.area2d())
            #raise
            
            
            #col_name = cell_ref.split('$')
            
            
            #print(name_obj.result)

            #attrs = vars(name_obj)
            # {'kids': 0, 'name': 'Dog', 'color': 'Spotted', 'age': 10, 'legs': 2, 'smell': 'Alot'}
            # now dump this in some way or another
            #attr_list  = ["{} : {}".format(*item) for item in attrs.items()]
            #print(attr_list)
            #raise
            #print(["{} : {}".format(item) for item in attrs.items()])
            #print(', '.join("%s: %s" % item for item in attrs.items()))
                        
                        
            #print(name,name_obj, 
            #      name_obj.book,
            #      
            #      )
        #print(wb.name_and_scope_map)
        #print(wb.name_obj_list)
        #name_map
#===============================================================================
# Main
#===============================================================================
if __name__ == "__main__":
    print ABSOLUTE_LOGGING_PATH

    logging.config.fileConfig(ABSOLUTE_LOGGING_PATH)


    myLogger = logging.getLogger()
    myLogger.setLevel("DEBUG")

    logging.debug("Started _main".format())


    path_input_file = r"C:\Projects2\081_Central_Hotel2\06 Project"

    #excel_project_dir = get_latest_rev(path_input_file, r"^Input Data", ext_pat = "xlsx")

    #process_out_dir()

    unittest.main()

    logging.debug("Finished _main".format())
