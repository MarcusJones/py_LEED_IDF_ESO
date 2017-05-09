'''
Created on 2012-10-07

@author: mjones
'''
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

    monitorDir = FREELANCE_DIR + r"\\0811_CentralTower\\SKP_OSM\\"
    
    ePlusEXEpath = os.path.split(os.path.realpath(__file__))[0] + r"\\..\\..\\MonitorBat\\RunEPlusMINE.bat"
    ePlusEXEpath = os.path.normpath(ePlusEXEpath )
    weatherFilePath = FREELANCE_DIR + r"\0811_CentralTower\WEA\SVK_Bratislava.118160_IWEC\SVK_Bratislava.118160_IWEC.epw"
    preFlightPath = os.path.split(os.path.realpath(__file__))[0] + r"\\..\\..\\ExcelTemplates\\PreFlight.xlsx"
    preFlightPath = os.path.normpath(preFlightPath )
    
    templatesFile = FREELANCE_DIR + r"\IDF_Library\Templates.xlsx"
    templatesFileAbsPath = os.path.abspath(templatesFile)
    templatesFileDirStem = FREELANCE_DIR + r"\IDF_Library\\" 
    
    monitorStandard(monitorDir,
                        ePlusEXEpath,
                        weatherFilePath,
                        preFlightPath,
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