"""
Created on Aug 3, 2011

@author: Marcus Jones

Template demonstrates how to run the IDF script to create variants from excel file
"""
#--- SETUP Config
from config.config import *
#import unittest

#--- SETUP Logging
import logging.config
print(ABSOLUTE_LOGGING_PATH)
logging.config.fileConfig(ABSOLUTE_LOGGING_PATH)
myLogger = logging.getLogger()
myLogger.setLevel("DEBUG")

#--- SETUP Standard modules
import os
import re
import csv
from pprint import pprint
#from collections import defaultdict
#from shutil import copyfile

#--- SETUP 3rd party modules

#--- SETUP Custom modules
#from utility_inspect import get_self
#import utilities_idf as util_idf
from idf.idf_parser import IDF as IDF 
import idf.utilities_idf_xml as util_xml
from idf.kept_classes import kept_classes_dict
#from utility_print_table import PrettyTable,printTable
from ExergyUtilities.utility_logger import LoggerCritical, LoggerDebug
from ExergyUtilities.utility_path import get_files_by_ext_recurse, get_latest_rev, copy_file
#from utility_excel_api import ExtendedExcelBookAPI
from ExergyUtilities.utility_excel import ExcelBookRead2

#from ExergyUtilities.utility_inspect import list_attrs, list_object

from ExergyUtilities.util_pretty_print import print_table



path_idf_file = r"C:\Dropbox\16336 LIDL\IDF Project\IDF\trunk.idf"


if __name__ == "__main__":
    print(ABSOLUTE_LOGGING_PATH)
    logging.config.fileConfig(ABSOLUTE_LOGGING_PATH)
    
    myLogger = logging.getLogger()
    myLogger.setLevel("DEBUG")
    
    logging.info("Start")
    this_IDF = IDF.from_IDF_file(path_idf_file)
    obj_table = util_xml.get_table_object_count(this_IDF)
    print_table(obj_table)
    #util_xml.print_table(obj_table)
    
    #process_project()
    #rename_zones()
    logging.info("End")                
    