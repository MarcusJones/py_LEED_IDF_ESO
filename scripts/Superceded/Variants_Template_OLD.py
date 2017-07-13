'''
Created on Aug 3, 2011

@author: Marcus Jones

Template demonstrates how to run the IDF script to create variants from excel file


'''

import logging.config
from config import *
import idf_xml.IDF as IX
#from UtilityExcel import ExcelBookRead


def templateProject():
    #===========================================================================
    # directories
    #===========================================================================
    projectFile = r"C:\Eclipse\PyIDF\ExcelTemplates\Input Data Tower SO03 r06.xlsx"
    weatherFilePath = FREELANCE_DIR + r"\WEA\ARE_Abu.Dhabi.412170_IWEC.epw"
    outputDirPath = FREELANCE_DIR + r"\Simulation"    
    groupName = "00myGroup"
    #===========================================================================
    # Assemble!
    #===========================================================================
    idfAssembly(projectFile,weatherFilePath,outputDirPath,groupName)
    

if __name__ == "__main__":
    print ABSOLUTE_LOGGING_PATH
    logging.config.fileConfig(ABSOLUTE_LOGGING_PATH)
    
    
    myLogger = logging.getLogger()
    myLogger.setLevel("DEBUG")
    
    logging.info("Started IDF test script")
    
    templateProject()

    logging.info("Finished IDF test script")                
    