# TEST MODULE
#===============================================================================
#--- SETUP Config
#===============================================================================
from config import *
import unittest

#===============================================================================
#--- SETUP Logging
#===============================================================================
import logging.config
import parse_html
print(ABSOLUTE_LOGGING_PATH)
logging.config.fileConfig(ABSOLUTE_LOGGING_PATH)
myLogger = logging.getLogger()
myLogger.setLevel("DEBUG")


#===============================================================================
#--- SETUP Add parent module
#===============================================================================
from os import sys, path
# Add parent to path
if __name__ == '__main__' and __package__ is None:
    this_path = path.dirname(path.dirname(path.abspath(__file__)))
    sys.path.append(this_path)
    logging.debug("ADDED TO PATH: ".format(this_path))


#===============================================================================
# SETUP Standard modules
#===============================================================================
from utility_inspect import get_self
import os

#===============================================================================
#--- SETUP Custom modules
#===============================================================================
from convert_csv_html import *

#===============================================================================
#--- Directories and files
#===============================================================================
#curr_dir = path.dirname(path.abspath(__file__))
#DIR_SAMPLE_IDF = path.abspath(curr_dir + "\..\.." + "\SampleIDFs")
#print(DIR_SAMPLE_IDF)



#===============================================================================
#--- Unit testing
#===============================================================================
# print("Test")
# class BasicTest(unittest.TestCase):
#     def setUp(self):
#         #print "**** TEST {} ****".format(get_self())
#         myLogger.setLevel("CRITICAL")
#         print("Setup")
#         
#         curr_path = os.path.dirname(os.path.realpath(__file__))
#         curr_path = os.path.abspath(curr_path + "\..\..\ExcelTemplates\Table test.xlsx")
#         
#         myLogger.setLevel("DEBUG")
#         
#         
#     def test010_SimpleCreation(self):
#         print("**** TEST {} ****".format(get_self()))
#       



class TestParseHTML(unittest.TestCase):

    def setUp(self):
        self.HTMLdataDir = os.path.abspath(os.getcwd() + r"\..\..\data")
        
        #csvPath = r"C:\Projects\tempOut\result.csv"
        print("Setup, HTML dir: {}".format(self.HTMLdataDir))

    def test_open(self):
        file_path = os.path.abspath(self.HTMLdataDir + "\SampleOutput.html")
        print(file_path)
        
        print(parse_html)
        
    def test910_SimpleCreation(self):
        print("**** TEST {} ****".format(get_self()))
        HTMLdataDir = os.getcwd() + r"\..\..\data"
        csvPath = r"C:\Projects\tempOut\result.csv"
        #run_project(HTMLdataDir, csvPath)

    def test920_processATable(self):
        print("**** TEST {} ****".format(get_self()))

        HTMLdataDir = os.getcwd() + r"\..\..\data"
        csvPath = r"C:\Projects\tempOut\result.csv"
        #run_project(HTMLdataDir, csvPath)
# 
#         htmlFilePaths =  filter_files_dir(HTMLdataDir,ext_pat="html$")
# 
#         table1 = parse_file(htmlFilePaths[0])
# 
#         oneTable = tables[0]
#         print oneTable
#         raise
#         finalTable = list()
# 
# 
#         table = flatten_table(table)
#         finalTable = finalTable + table
# 
#         for row in finalTable:
#             print row



  
class TestExcel_OLD(unittest.TestCase):

    def setUp(self):
        print("**** TEST {} ****".format(get_self()))

        curr_path = os.path.dirname(os.path.realpath(__file__))
        curr_path = os.path.abspath(curr_path + "\..\..\ExcelTemplates\Table test.xlsx")

        print("Current path: {}".format(curr_path))
        
        with ExtendedExcelBookAPI(curr_path) as this_excel:

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
        print("**** TEST {} ****".format(get_self()))






if __name__ == '__main__': 
    basic = unittest.TestSuite()
    basic.addTests( TestParseHTML )
    basic.addTests( TestExcel_OLD )
        
    unittest.main(basic)

