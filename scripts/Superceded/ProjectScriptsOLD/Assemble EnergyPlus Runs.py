'''
Created on Aug 3, 2011

@author: UserXP
'''

import logging.config
import os
import sys
#sys.path.insert(0, "c:\EclipsePython\EvolveDesign\src")
import idf_xml.IDF as IDF
import csv
from config import *

def _decathlonAssembly():
    
    # Weather file
    weatherFilePath = r"D:\Freelancing\WEA\ARE_Abu.Dhabi.412170_IWEC.epw"
    
    # Group file
    groupFilePath = r"D:\Freelancing\Simulation\\00thisGroupFile.epg"
    
    # The assembly control file
    variantsFile = r"D:\Dropbox\\00 Decathlon Development\RunControl\Decathlon basic r01.xlsx"
    
    #===============================================================================
    # Load variants
    #===============================================================================
    variantFileAbsPath = os.path.abspath(variantsFile)
    #inputFilesAbsDir = os.path.normpath(inputFileDir)
    outputTargetAbsDir = os.path.normpath(r"D:\Freelancing\Simulation\\")
    print variantFileAbsPath
    variantsList = IDF.loadVariants(inputExcelPath=variantFileAbsPath,
                             targetAbsDirStem=outputTargetAbsDir,
                             )
    
    
    for variant in variantsList:
        
        #===========================================================================
        # Create a new IDF from the variant
        #===========================================================================
       
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
        thisIDF.parseIDFtoXML()
        #thisIDF.cleanOutObject()
        thisIDF.cleanOutObject(IDF.keptClassesDict['onlyGeometry'])
        
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
                #thisIDF.selectCommentedAttrAndChange(change)
                thisIDF.selectCommentedAttrInNamedObjectAndChange(change)
                #except:
                #    pass
                    #raise NameError("{0},{1}".format(change,variant.name))
                    
        
        #thisIDF.convertXMLtoIDF()
        
        thisIDF.writeIdf(thisIDF.pathIdfOutput)
        
        #print thisIDF.listZonesWithName('Gym')
        
        #thisIDF.makeUniqueNames()
    
    #csvout = open(groupFilePath,"w")
    
    #csvout = csv.writer(open(groupFilePath, 'wb'))
    
    #===============================================================================
    # Write the group file
    #===============================================================================
    
    #groupSimFilePath = 'C:\Freelance\Simulation\00eggs.epg'
    
    csvout = csv.writer(open(groupFilePath, 'wb'))
    
    for variant in variantsList:
        thisRow = [variant.targetDirAbsPath,weatherFilePath,variant.targetDirAbsPath,"1"]
        csvout.writerow(thisRow)
    
    

def _standardAssembly():
    
    # Weather file
    weatherFilePath = r"D:\Freelancing\WEA\ARE_Abu.Dhabi.412170_IWEC.epw"
    
    # Group file
    groupFilePath = r"D:\Freelancing\Simulation\\00thisGroupFile.epg"
    
    # The variants
    #variantsFile = r"C:\Freelance\062_RasGhurabMos\RunControl\\062 AllCredits r02.xlsx"
    #variantsFile = r"C:\Freelance\090_DewanVilla\RunControl\AllCredits6.xlsx"
    #variantsFile = r"C:\Freelance\055_ACECustomsHousing\Runcontrol\Variants r03.xlsx"
    #variantsFile = r"C:\Freelance\091_AceCustomsCommunity\Input Data\091 Input data r02.xlsx"
    #variantsFile = r"C:\Freelance\073_ACE_Bachelor\Runcontrol\Variants r03.xlsx"
    #variantsFile = r"C:\Freelance\090_DewanVilla\Input Data\090 Input data r03.xlsx"
    variantsFile = r"D:\Freelancing\096_AlBateen\Al Bateen Control r09.xlsx"
    #variantsFile = r"D:\Freelancing\046_Al_Ain_Tech_Two\Input Data\Input Data Al Ain Tech r05.xlsx"
    #===============================================================================
    # Load variants
    #===============================================================================
    variantFileAbsPath = os.path.abspath(variantsFile)
    #inputFilesAbsDir = os.path.normpath(inputFileDir)
    outputTargetAbsDir = os.path.normpath(r"D:\Freelancing\Simulation\\")
    variantsList = IDF.loadVariants(inputExcelPath=variantFileAbsPath,
                             targetAbsDirStem=outputTargetAbsDir,
                             )
    
    
    for variant in variantsList:
        
        #===========================================================================
        # Create a new IDF from the variant
        #===========================================================================
       
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
        thisIDF.parseIDFtoXML()
        #thisIDF.cleanOutObject()
        thisIDF.cleanOutObject(IDF.keptClassesDict['onlyGeometry'])
        
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
                #thisIDF.selectCommentedAttrAndChange(change)
                thisIDF.selectCommentedAttrInNamedObjectAndChange(change)
                #except:
                #    pass
                    #raise NameError("{0},{1}".format(change,variant.name))
                    
        
        thisIDF.convertXMLtoIDF()
        
        thisIDF.writeIdf(thisIDF.pathIdfOutput)
        
        #print thisIDF.listZonesWithName('Gym')
        
        #thisIDF.makeUniqueNames()
    
    #csvout = open(groupFilePath,"w")
    
    #csvout = csv.writer(open(groupFilePath, 'wb'))
    
    #===============================================================================
    # Write the group file
    #===============================================================================
    
    #groupSimFilePath = 'C:\Freelance\Simulation\00eggs.epg'
    
    csvout = csv.writer(open(groupFilePath, 'wb'))
    
    for variant in variantsList:
        thisRow = [variant.targetDirAbsPath,weatherFilePath,variant.targetDirAbsPath,"1"]
        csvout.writerow(thisRow)
        
    logging.info("Wrote the {0} variants to the group simulation file at: {1}".format(len(variantsList),groupFilePath))     



    weatherFilePath = r"D:\Freelancing\WEA\ARE_Abu.Dhabi.412170_IWEC.epw"

    
def idfAssembly(weatherFilePath,variantsFile,outputDirPath,groupName):
    groupFilePath = outputDirPath + r"\\" + groupName + ".epg"
    
    #===============================================================================
    # Load variants
    #===============================================================================
    variantFileAbsPath = os.path.abspath(variantsFile)
    outputTargetAbsDir = os.path.normpath(outputDirPath)
    variantsList = IDF.loadVariants(inputExcelPath=variantFileAbsPath,
                             targetAbsDirStem=outputTargetAbsDir,
                             )
    for variant in variantsList:
        
        #===========================================================================
        # Create a new IDF from the variant
        #===========================================================================
       
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
        thisIDF.parseIDFtoXML()
        #thisIDF.cleanOutObject()
        thisIDF.cleanOutObject(IDF.keptClassesDict['onlyGeometry'])
        
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

def idfAssemblyVersion2(weatherFilePath,variantsFile,outputDirPath,groupName):
    groupFilePath = outputDirPath + r"\\" + groupName + ".epg"
    
    #===============================================================================
    # Load variants
    #===============================================================================
    variantFileAbsPath = os.path.abspath(variantsFile)
    outputTargetAbsDir = os.path.normpath(outputDirPath)
    variantsList = IDF.loadVariants(inputExcelPath=variantFileAbsPath,
                             targetAbsDirStem=outputTargetAbsDir,
                             )
    for variant in variantsList:
        
        #===========================================================================
        # Create a new IDF from the variant
        #===========================================================================
       
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
        thisIDF.parseIDFtoXML()
        #thisIDF.cleanOutObject()
        thisIDF.cleanOutObject(IDF.keptClassesDict['geometryAndSpaceLoads'])
        
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
    
    
def _simpleTestGeom():
    # Weather file
    weatherFilePath = r"D:\Freelancing\002_Moravcik\WEA\SVK_Bratislava.118160_IWEC.epw"
    
    # Output file
    outputDirPath = r"D:\Freelancing\000_TestProject\Results"    
    
    # Variants file
    variantsFile = r"D:\Freelancing\000_TestProject\RunControl\Input Data.xlsx"
    
    # Execute!
    idfAssembly(weatherFilePath,variantsFile,outputDirPath)
        



def _Moravcik():
    # Weather file
    weatherFilePath = r"D:\Freelancing\002_Moravcik\WEA\SVK_Bratislava.118160_IWEC.epw"
    
    # Output file
    outputDirPath = r"D:\Freelancing\MediaSimNoAtrium"    
    groupName = "Moravcik"
    
    # Variants file
    variantsFile = r"D:\Dropbox\Company Development\02 Running\078 - LEED Media Center (e-Dome)\001_Moravcik\Input data\Input Data Media Moravcik r05.xlsx"
    
    # Execute!
    idfAssembly(weatherFilePath,variantsFile,outputDirPath,groupName)
        

def _KaliskyWithout():
    # Weather file
    weatherFilePath = r"D:\Freelancing\002_Moravcik\WEA\SVK_Bratislava.118160_IWEC.epw"
    
    # Output file
    outputDirPath = r"D:\Freelancing\MediaSim"    
    groupName = "Kalisky Without"

    # Variants file
    variantsFile = r"D:\Dropbox\Company Development\02 Running\078 - LEED Media Center (e-Dome)\001_Kalisky_Without\Input Data\Input Data Media Moravcik r05.xlsx"
    
    # Execute!
    idfAssembly(weatherFilePath,variantsFile,outputDirPath,groupName)

def _AlAinUniversity():
    # Weather file
    weatherFilePath = r"D:\Freelancing\WEA\ARE_Abu.Dhabi.412170_IWEC.epw"
    
    # Output file
    outputDirPath = r"D:\Freelancing\Simulation"    
    groupName = "00Group"


    # Variants file
    variantsFile = r"D:\Freelancing\046_Al_Ain_Tech_Th\RunControl\Input Data Al Ain Tech r12.xlsx"
    
    # Execute!
    idfAssemblyVersion2(weatherFilePath,variantsFile,outputDirPath,groupName)

        
def _KaliskyWithAtrium():
    # Weather file
    weatherFilePath = r"D:\Freelancing\002_Moravcik\WEA\SVK_Bratislava.118160_IWEC.epw"
    
    # Output file
    outputDirPath = r"D:\Freelancing\MediaSim"    
    groupName = "Kalisky With Atrium"

    # Variants file
    variantsFile = r"D:\Dropbox\Company Development\02 Running\078 - LEED Media Center (e-Dome)\001_Kalisky_With_Atrium\Input Data\Input Data Media Moravcik r05.xlsx"
    
    # Execute!
    idfAssembly(weatherFilePath,variantsFile,outputDirPath,groupName)
 
 
def _SkyTowerOLD():
    # Weather file
    weatherFilePath = r"D:\Freelancing\WEA\ARE_Abu.Dhabi.412170_IWEC.epw"
    
    # Output file
    outputDirPath = r"D:\Freelancing\Simulation"    
    groupName = "00AlBateen"

    # Variants file
    variantsFile = r"D:\Freelancing\096_AlBateen\Al Bateen Control r09.xlsx"
    
    # Execute!
    idfAssembly(weatherFilePath,variantsFile,outputDirPath,groupName)
  
def _AlBateen():
    # Weather file
    weatherFilePath = r"D:\Freelancing\WEA\ARE_Abu.Dhabi.412170_IWEC.epw"
    
    # Output file
    outputDirPath = r"D:\Freelancing\Simulation"    
    groupName = "00AlBateen"

    # Variants file
    variantsFile = r"D:\\Freelancing\\096_AlBateen\\Al Bateen Control r10.xlsx"
    
    
    #print variantsFile
    
    
    # Execute!
    idfAssembly(weatherFilePath,variantsFile,outputDirPath,groupName)
   

if __name__ == "__main__":
    # Load the logging configuration
    logging.config.fileConfig(ABSOLUTE_LOGGING_PATH)
    
    logging.info("Started IDF test script")

     
    templatesList = IDF.loadTemplates(IDF_TEMPLATE_FILE, IDF_TEMPLATE_PATH)

        
    #_decathlonAssembly()
    #_standardAssembly()

    
    #_SkyTower()
    #_AlBateen()
    #_AlAinUniversity()

    #_Moravcik()
    #_KaliskyWithout()
    #_KaliskyWithAtrium()
    #_simpleTestGeom()

    
    
    logging.info("Finished IDF test script")                
        