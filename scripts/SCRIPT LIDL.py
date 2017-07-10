'''
Created on Aug 3, 2011

@author: Marcus Jones

Template demonstrates how to run the IDF script to create variants from excel file


'''

import logging.config
from config import *

import utilities_idf as util_idf
from idf_parser import IDF as IDF 
from utility_print_table import PrettyTable,printTable

def idfAssembly(projectFile,weatherFilePath,outputDirPath,groupName):
    
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
    print(ABSOLUTE_LOGGING_PATH)
    logging.config.fileConfig(ABSOLUTE_LOGGING_PATH)
    
    
    myLogger = logging.getLogger()
    myLogger.setLevel("DEBUG")
    
    logging.info("Started IDF test script")
    
    templateProject()

    logging.info("Finished IDF test script")                
    