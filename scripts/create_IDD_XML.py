"""
Created on Aug 3, 2011

@author: Marcus Jones

Template demonstrates how to run the IDF script to create variants from excel file
"""
#--- SETUP Config
from config import *
#import unittest

#--- SETUP Logging
import logging.config
print(ABSOLUTE_LOGGING_PATH)
logging.config.fileConfig(ABSOLUTE_LOGGING_PATH)
myLogger = logging.getLogger()
myLogger.setLevel("DEBUG")

#--- SETUP Standard modules
import os

#--- SETUP 3rd party modules

#--- SETUP Custom modules
from idf_parser import IDF as IDF 

PROJ_LIDL = {
                  'path_proj_excel' : r'C:\Dropbox\16336 LIDL\IDF Project\\',
                  'idf_base' : r'C:\Dropbox\16336 LIDL\IDF Project\IDF\\',
                  'weather_file' : r'C:\Dropbox\16336 LIDL\Weather\SVN_Ljubljana.130140_IWEC.epw',
                  'output_dir' : r"C:\IDF_OUT\\",
                  }

proj = PROJ_LIDL

def process_project():
    #===========================================================================
    # directories
    #===========================================================================
    
    outputDirPath = FREELANCE_DIR + r"\IDD\\"    
    output_idd_xml_path = outputDirPath + "output.xml"
    
    output_idd_xml_path = os.path.abspath(output_idd_xml_path)
    
    #--- Load IDD
    
    IDD_xml = IDF.from_IDD_file(IDD_FILE_PATH)
    
    #print(IDD_xml)
    print(output_idd_xml_path)
    print(type(output_idd_xml_path))
    
    IDD_xml.write_XML(output_idd_xml_path)
    
    print("Wrote {}".format(output_idd_xml_path))

if __name__ == "__main__":
    print(ABSOLUTE_LOGGING_PATH)
    logging.config.fileConfig(ABSOLUTE_LOGGING_PATH)
    
    myLogger = logging.getLogger()
    myLogger.setLevel("DEBUG")
    
    logging.info("Started IDF test script")
    
    process_project()

    logging.info("Finished IDF test script")                
    