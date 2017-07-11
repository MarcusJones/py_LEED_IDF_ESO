'''
Created on Aug 3, 2011

@author: Marcus Jones

Template demonstrates how to run the IDF script to create variants from excel file
'''
#--- SETUP Config
from config import *
import unittest

#--- SETUP Logging
import logging.config
print(ABSOLUTE_LOGGING_PATH)
logging.config.fileConfig(ABSOLUTE_LOGGING_PATH)
myLogger = logging.getLogger()
myLogger.setLevel("DEBUG")

#--- SETUP Standard modules
import os
import re

#--- SETUP Custom modules
from utility_inspect import get_self
import utilities_idf as util_idf
from idf_parser import IDF as IDF 
from utility_print_table import PrettyTable,printTable
from utility_logger import LoggerCritical, LoggerDebug
from utility_path import get_files_by_ext_recurse

def get_templates(templatePath, filter_regex_string = ".", flgExact = True):
    
    # Used to be a method on IDF class
    # This is just a filter for file names now...
    """Given a path, return a list of matching IDF files (by regex), and load into IDF objects
    """ 
    
    templates = list()
    
    
    if flgExact:
        filter_regex_string = "^" + filter_regex_string + "*$"

    with LoggerCritical():
        for path in get_files_by_ext_recurse(templatePath, "idf"):
            #print(path)
            base = os.path.basename(path)
            template_file_name = os.path.splitext(base)[0]
            #print(template_file_name)
            if  re.search(filter_regex_string,template_file_name):
                #print(path)
                template=IDF.from_IDF_file(path,template_file_name)
                #template.getTemplateInfo()
                templates.append(template)
    
    # No duplicates!
    assert(len(templates) == len(set(templates)))
    
    #print(len(templates))
    #print(len(set(templates)))
    
    #num_duplicates = len(templates) - len(set(templates))
    #assert len(templates), "{}, duplicate templates found in {}".format(num_duplicates,IDF_TEMPLATE_PATH)
    
#    assert(len(thisTemplate) == 1), "Template; {} found {} matches {}".format(templateDef['templateName'],
#                    len(thisTemplate),thisTemplate)
#    thisTemplate = thisTemplate[0]    
        
    
    logging.debug("Found {} templates in {} filtered {}".format(len(templates),IDF_TEMPLATE_PATH, filter_regex_string))
    
    return templates



#--- 
#--- 
#--- 
#--- 
#---  





def idf_assembly(projectFile,weatherFilePath,outputDirPath,groupName):
    
    """
    A wrapper utility script to automate everything
    """
    
    templatesList = IDF.loadTemplates(IDF_TEMPLATE_PATH)
    raise
    groupFilePath = outputDirPath + r"\\" + groupName + ".epg"
    
    #===============================================================================
    # Load variants
    #===============================================================================
    variantFileAbsPath = os.path.abspath(projectFile)
    outputTargetAbsDir = os.path.normpath(outputDirPath)
    variantsList = IDF.loadVariants(inputExcelPath=variantFileAbsPath,
                             targetAbsDirStem=outputTargetAbsDir,
                             )
    
    
    
    
    for variant in variantsList:
        
        #===========================================================================
        # Create a new IDF from the variant
        #===========================================================================
       
        thisIDF = IDF(
            pathIdfInput=variant.sourceFileAbsPath, 
            XML=None, 
            IDFstring = None, 
            IDstring = None, 
            description = None, 
            pathIdfOutput = variant.targetDirAbsPath
            )
        
        # Call the load        
        thisIDF.loadIDF()
        # Call convert
        thisIDF.parseIDFtoXML()
        #thisIDF.cleanOutObject()
        thisIDF.cleanOutObject(keptClassesDict['onlyGeometry'])
        
        thisIDF.applyDefaultConstructions()
        
        # Apply unique templates
        for template in variant.templateDescriptions:
            thisIDF.applyTemplateNewStyle(template,templatesList)
            
        # Apply changes
        if variant.changesList:
            for change in variant.changesList:
                thisIDF.selectCommentedAttrInNamedObjectAndChange(change)

        thisIDF.convertXMLtoIDF()
        
        thisIDF.writeIdf(thisIDF.pathIdfOutput)
    
    #===============================================================================
    # Write the group file
    #===============================================================================
        
    csvout = csv.writer(open(groupFilePath, 'wb'))
    
    for variant in variantsList:
        thisRow = [variant.targetDirAbsPath,weatherFilePath,variant.targetDirAbsPath,"1"]
        csvout.writerow(thisRow)
        
    logging.info("Wrote the {0} variants to the group simulation file at: {1}".format(len(variantsList),groupFilePath))     
 


def process_project():
    #===========================================================================
    # directories
    #===========================================================================
    projectFile = r"C:\Eclipse\PyIDF\ExcelTemplates\Input Data Tower SO03 r06.xlsx"
    weatherFilePath = FREELANCE_DIR + r"\WEA\ARE_Abu.Dhabi.412170_IWEC.epw"
    outputDirPath = FREELANCE_DIR + r"\Simulation"    
    groupName = "00myGroup"
    
    


    #--- Get templates from directory     
    get_templates(IDF_TEMPLATE_PATH)
    #===========================================================================
    # Assemble!
    #===========================================================================
    #    idfAssembly(projectFile,weatherFilePath,outputDirPath,groupName)
    
if __name__ == "__main__":
    print(ABSOLUTE_LOGGING_PATH)
    logging.config.fileConfig(ABSOLUTE_LOGGING_PATH)
    
    myLogger = logging.getLogger()
    myLogger.setLevel("DEBUG")
    
    logging.info("Started IDF test script")
    
    process_project()

    logging.info("Finished IDF test script")                
    