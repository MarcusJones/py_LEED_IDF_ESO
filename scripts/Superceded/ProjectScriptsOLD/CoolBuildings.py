'''
Created on Aug 3, 2011

@author: UserXP
'''

import logging.config
import os
import sys
sys.path.insert(0, "c:\EclipsePython\EvolveDesign\src")
import IDF

# Load the logging configuration
logging.config.fileConfig('..\\LoggingConfig\\logging.conf')

logging.info("Started IDF test script")

# The templates
templatesFile = r"C:\Freelance\IDF_Library\Templates.xlsx"
templatesFileAbsPath = os.path.abspath(templatesFile)
templatesFileDirStem = r"C:\Freelance\IDF_Library\\" 
templatesList = IDF.loadTemplates(templatesFileAbsPath, templatesFileDirStem)

# The variants
#variantsFile = r"C:\Freelance\062_RasGhurabMos\RunControl\AllCredits.xlsx"
variantsFile = r"C:\Freelance\090_DewanVilla\RunControl\AllCredits.xlsx"
#inputFileDir = r"C:\Freelance\062_RasGhurabMos\Input Models"
inputFileDir = r"C:\Freelance\090_DewanVilla\IDF"

variantFileAbsPath = os.path.abspath(variantsFile)
inputFilesAbsDir = os.path.normpath(inputFileDir)
outputTargetAbsDir = os.path.normpath(r"C:\Freelance\Simulation\\")
variantsList = IDF.loadVariants(inputExcelPath=variantFileAbsPath,
                         inputAbsDirStem=inputFilesAbsDir,
                         targetAbsDirStem=outputTargetAbsDir,
                         )

#pathXmlOutput = '..\\XML Output\\Test IDF.xml' 

for variant in variantsList:
    
    #thisOSM = IDF.fromIdfFile(variant.path)
            
    #variant.ID = variantCount
    
    #variant.path =  "C:\\Freelance\\Simulation\\Variant" + variant.ID + ".idf"  
    
    #variantCount += 1
    
    # Create a new IDF from the variant
   
    thisIDF = IDF.IDF(
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
    thisIDF.convertIDFtoXML()
    thisIDF.cleanOutObject()
    
    # Apply standard templates
    #        thisIDF.applyTemplate(runControlType)
    #        thisIDF.applyTemplate('SizingParams')
    #        thisIDF.applyTemplate(outputType)
    #        thisIDF.selectCommentedAttrAndChange(["^Building$","Name",variant.ID])
    #        
    # Apply unique templates
    for template in variant.templateDescriptions:
        #print template
    
        thisIDF.applyTemplateNewStyle(template,templatesList)
        
    # Apply changes
    if variant.changesList:
        for change in variant.changesList:
            #print change
            #try:  
            thisIDF.selectCommentedAttrAndChange(change)
            #except:
            #    pass
                #raise NameError("{0},{1}".format(change,variant.name))
                
    
    thisIDF.convertXMLtoIDF()
    
    thisIDF.writeIdf(thisIDF.pathIdfOutput)
    
    #print thisIDF.listZonesWithName('Gym')
    
    #thisIDF.makeUniqueNames()

logging.info("Finished IDF test script")                
        