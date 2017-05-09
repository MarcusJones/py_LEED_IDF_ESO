'''
Created on Aug 3, 2011

@author: Marcus Jones
'''

import logging.config
from config import *
#import idf_xml.IDF.IDF as IDF
import idf_xml.IDF as idf
#from idf_xml.IDF import IDF,loadVariants,assembleVariants,printXML
#from idf_xml.IDF import treeGetClass,getPositionOfATTR,cleanOutObject,xpathRE
#from idf_xml.IDF import keptClassesDict
#from idf_xml.IDF import idfGetZoneNameList,IDDboolMatchField, IDDgetMatchedPosition, applyTemplate, applyChange
import idf_xml.VRV_Support as vrv
#from idf_xml.VRV_Support import addZoneHVAC,addTerminals
#from idf_xml.IDF import keptClassesDict
from UtilityPathsAndDirs import splitUpPath
#from idf_xml.Utilities import idStr
#from copy import deepcopy
#import re
import csv
from UtilityLogger import loggerCritical
from UtilityPathsAndDirs import erase_dir_contents,count_files,count_dirs,getLatestRev
from xls_preprocess.preprocess import process_project


import re

#from UtilityUserInput import query_yes_no
from UtilityGUI import simpleYesNo

    
if __name__ == "__main__":
    # Load the logging configuration
    logging.config.fileConfig(ABSOLUTE_LOGGING_PATH)
    
    logging.info("Started IDF test script")
    
    # Path to XLS definition 
    #excelProjectPath = thisProjDefRoot + relativePath
    #excelProjectPath = os.path.abspath(excelProjectPath)
    
    #excelProjectPath = r"C:\Projects\081_CentralTowerFinal2\Project2\Input Data Tower SO03 r16.xlsx"
    # = r"C:\Projects2\081_CentralTowerFinal\Project2\Input Data Tower SO03 r13.xlsx"
    excelProjectDir = r"C:\Projects2\081_CentralTowerFinal\Project2\\"
    excelName = r"^Input Data Tower SO03"
    excelExt = "xlsx"
    #print trialDir
    
    #getLatestRevisionFullPath(trialDir)
    excelProjectPath = getLatestRev(excelProjectDir,excelName,excelExt)
    
    
    if count_files(PATH_IDF_OUT) or count_dirs(PATH_IDF_OUT):
        if simpleYesNo("Delete from {} \n {} files \n {} directories".format(PATH_IDF_OUT,count_files(PATH_IDF_OUT),
                                                                            count_dirs(PATH_IDF_OUT),
                                                                            )):
            erase_dir_contents(PATH_IDF_OUT)
        else:
            pass
    process_project(excelProjectPath)

    logging.info("Finished IDF test script")                
    