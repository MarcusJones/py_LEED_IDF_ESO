#===============================================================================
#--- SETUP Config
#===============================================================================
from config.config import *
import unittest

#===============================================================================
#--- SETUP Logging
#===============================================================================
import logging.config
print(ABSOLUTE_LOGGING_PATH)
logging.config.fileConfig(ABSOLUTE_LOGGING_PATH)
myLogger = logging.getLogger()
myLogger.setLevel("DEBUG")

#===============================================================================
#--- SETUP Add parent module
#===============================================================================

#===============================================================================
#--- SETUP Standard modules
#===============================================================================
from collections import defaultdict


#===============================================================================
#--- SETUP Custom modules
#===============================================================================
import HTML_parse.parse_html as util_html
from ExergyUtilities.utility_excel_api import ExtendedExcelBookAPI
import ExergyUtilities.utility_path as util_paths
import ExergyUtilities.utility_jinja2 as util_jinja

from openpyxl import load_workbook

#===============================================================================
#--- Directories and files
#===============================================================================
#curr_dir = path.dirname(path.abspath(__file__))
#DIR_SAMPLE_IDF = path.abspath(curr_dir + "\..\.." + "\SampleIDFs")
#print(DIR_SAMPLE_IDF)
base_dir = r'M:\52_CES\16336_LEED_Lidl\5_Arbeit\Credits\05_EA\06_Optimize Energy Performance\\'
sample_html = base_dir + r'\\IDF Project\OUTPUT\Baseline-G000Table.html'
path_excel_template = r'C:\LOCAL_REPO\py_LEED_IDF_ESO\ExcelTemplates\LEED modify html.xlsx'
new_excel_path = base_dir + r'\\IDF Project\test_parsing.xlsx'


path_sample_excel = base_dir + r'\\IDF Project\test_parsing.xlsx'


def convert_html_excel(path_html):
    logging.debug("Processing {}".format(path_html))
    tree = util_html.parse_file2(path_html)
    raise
    util_paths.copy_file(path_excel_template,new_excel_path)

    with ExtendedExcelBookAPI(new_excel_path) as xl_book:
        for section_name in tree:
            print("------------", section_name, "------------")
            for table_name in tree[section_name]:
                #print(table_name,": ", end="")
                #print(tree[section_name][table_name])
                sheet_name = "{} | {}".format(section_name,table_name)
                #print(sheet_name)
                #table_rows = [['a','0'],['','nope']]
                #util_html.get_one_table(tree,section_name,table_name)
                table_rows = util_html.expand_table_node(tree[section_name][table_name])
                xl_book.write(sheet_name,table_rows,x=0,y=0)
                
                #print(table)
    logging.debug("Finished writing {}".format(new_excel_path))

def get_all_excel_table(wb, sht):
    return [[item.value for item in r] for r in sht.rows]
    
    


def get_table_html(wb, sht_name):
    sht = wb[sht_name]
    table = get_all_excel_table(wb, sht)
    
    #this_row = table[0]
    
    result = util_jinja.tmplt_table.render(rows=table, trim_blocks=True, lstrip_blocks=True)
    print(result)
    raise
    for this_row in table:
        result = util_jinja.tmplt_row.render(data=this_row, trim_blocks=True, lstrip_blocks=True)
        
        
        print(result)
    #raise    
    
def convert_excel_html(excel_path):
    
    wb = load_workbook(excel_path, read_only=True)
    #print(excel_path)
    #print()
    #tables = defaultdict(dict)
    
    
    
    
    
    for sht_name in wb.get_sheet_names():
        #print(sht_name)
        #sheet_name = "{} | {}".format(section_name,table_name)
        html_title = util_jinja.tmplt_title.render(_title=sht_name, _full_name = "")
        
        #trim_blocks and lstrip_blocks
        #print(html_title)        
        
        get_table_html(wb, 'Annual Building Util')
        raise
#        Annual Building Utility Performance Summary
#Entire Facility_End Uses

        
        
        sht = wb[sht_name]
        #print(sht)

        
        
        #print
    #worksheet = wb.get_sheet_by_name(first_sheet)
    #get_all_excel_table()

    if 0:
        with ExtendedExcelBookAPI(excel_path) as xl_book:
            #print(xl_book)
            sheet_names=xl_book.get_sheet_names()
            #print(sheet_names)
            for sht in sheet_names:
                #print(sht)
                xl_book.get_sheet(sht)
                #get_table_all
                this_table = xl_book.get_table_all(sht, dataType="str")
            #util_jinja
 

    
if __name__ == "__main__":
    print(ABSOLUTE_LOGGING_PATH)
    logging.config.fileConfig(ABSOLUTE_LOGGING_PATH)
    
    myLogger = logging.getLogger()
    myLogger.setLevel("DEBUG")
    
    
    
    logging.info("Started script")
    
    convert_html_excel(sample_html)
    #convert_excel_html(path_sample_excel)

    logging.info("Finished script")                
    