'''
Created on 2012-10-07

@author: mjones
'''

raise Exception("Needs update")
#===============================================================================
# Set up
#===============================================================================
from __future__ import division    

from monitor_idf_auto.Preflight import monitorStandard
import logging.config
from UtilityInspect import whoami, whosdaddy
from config import *
import idf_xml.IDF as IDF
import html_summary.ParseHTMLTables as htPr
import os

def runMonitor():

    monitorDir = FREELANCE_DIR + "\Simulation"
    
    
    ePlusEXEpath = r"D:\apps\EnergyPlusV7-1-0\RunEPlusMine.bat"
    weatherFilePath = r"D:\Freelancing\WEA\ARE_Abu.Dhabi.412170_IWEC.epw"
    preFlightDefinitionPath = r"D:\EclipseSpace2\EclipsePython\EvolveDesign\XLS Projects\PreFlight.xlsx"
    
    templatesFile = r"D:\Freelancing\IDF_Library\Templates.xlsx"
    templatesFileAbsPath = os.path.abspath(templatesFile)
    templatesFileDirStem = r"D:\Freelancing\IDF_Library\\" 
    
    monitorStandard(monitorDir,
                        ePlusEXEpath,
                        weatherFilePath,
                        preFlightDefinitionPath,
                        templatesFileAbsPath,
                        templatesFileDirStem)


#===============================================================================
# Main
#===============================================================================
if __name__ == "__main__":
    print ABSOLUTE_LOGGING_PATH
    logging.config.fileConfig(ABSOLUTE_LOGGING_PATH)
    
    
    myLogger = logging.getLogger()
    myLogger.setLevel("DEBUG")

    logging.debug("Started _main".format())
    
    #print FREELANCE_DIR
    
    runMonitor()
        
    logging.debug("Finished _main".format())        