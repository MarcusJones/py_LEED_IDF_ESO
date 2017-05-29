#===============================================================================
# Title of this Module
# Authors; MJones, Other
# 00 - 2012FEB05 - First commit
# 01 - 2012MAR17 - Update to ...
#===============================================================================

"""This module does A and B. 
Etc.
"""

#===============================================================================
# Set up
#===============================================================================
from __future__ import division    
import logging.config
from utility_inspect import get_self, get_parent
import unittest
from config import *
import re
import idf_xml.IDF as idf
import os
import subprocess
import time
import datetime
import subprocess
from utility_path import split_up_path
from UtilityLogger import loggerCritical


#===============================================================================
# Code
#===============================================================================
def getLatestNumberedRevison(sourceFileDir, extensionFilter):
    
    """
    sourceFileDir = r"D:\Freelancing\001_Kalisky\SKP_OSM\\"
    
    extensionFilter = ".osm"
    
    print getLatestRevison(sourceFileDir, extensionFilter)
    """
    
    fileRevisionList = list()
    for filename in os.listdir(sourceFileDir):

        #basename, extension = filename.split('.')
        base, extension = os.path.splitext(filename)
        #print base, extension
        if extension == ".osm":
            revisionTextList = re.findall("r[\d]+", base)
            if revisionTextList: 
                revisionText = re.findall("r[\d]+", base)[0]
                #print revisionText
                revisionNumber = int(re.findall("[\d]+",revisionText)[0])
                
                fileRevisionList.append((revisionNumber, filename))


    # Sort, and pop the most recent (last) filename
    finalFileAndTime = (sorted(fileRevisionList)).pop()

    
    latestRevisionFileNamePath = os.path.join(sourceFileDir, latestRevisionFileName)
    
    logging.debug("Latest revision in '{}' is '{}'".format(sourceFileDir,latestRevisionFileName))
    
    return latestRevisionTime, latestRevisionFileNamePath

def openTheErrorFile(theDir):
    
    """
    sourceFileDir = r"D:\Freelancing\001_Kalisky\SKP_OSM\\"
    
    extensionFilter = ".osm"
    
    print getLatestRevison(sourceFileDir, extensionFilter)
    """
    logging.debug("Trying to open an error file in {}".format(theDir))

    for filename in os.listdir(theDir):

        #basename, extension = filename.split('.')
        base, extension = os.path.splitext(filename)
        #print base, extension
        if extension == ".err":
            thePath = os.path.normpath(theDir + filename)
            theEXE = r"D:\apps\notepad++.exe"
            logging.debug("Trying to open an error file {}".format(thePath))
            logging.debug("Opening with {}".format(theEXE))
            
            subprocess.Popen([theEXE, thePath])


    # Sort, and pop the most recent (last) filename
    #latestRevisionFileName = (sorted(fileRevisionList)).pop()[1]
    
    #latestRevisionFileNamePath = os.path.join(sourceFileDir, latestRevisionFileName)
    
    #logging.debug("Latest revision in '{}' is '{}'".format(sourceFileDir,latestRevisionFileName))

    
    #return latestRevisionFileNamePath
 
    
def getLatestChangedFile(sourceFileDir, extensionFilter):
    
    """
    sourceFileDir = r"D:\Freelancing\001_Kalisky\SKP_OSM\\"
    
    extensionFilter = ".osm"
    
    print getLatestRevison(sourceFileDir, extensionFilter)
    """
    
    fileRevisionList = list()
    for filename in os.listdir(sourceFileDir):

        #basename, extension = filename.split('.')
        base, extension = os.path.splitext(filename)
        #print base, extension
        if extension == extensionFilter:
            #fullPath = sourceFileDir + filename
            fullPath = os.path.join(sourceFileDir,filename)
            mtime = os.path.getmtime(fullPath)
            fileRevisionList.append((mtime, filename))            

    # Sort, and pop the most recent (last) filename
    finalFileAndTime = (sorted(fileRevisionList)).pop()
    
    latestRevisionFileName = finalFileAndTime[1]
    latestRevisionTime = finalFileAndTime[0]
    latestRevisionFileNamePath = os.path.join(sourceFileDir, latestRevisionFileName)
    
    formattedTime = datetime.datetime.fromtimestamp(latestRevisionTime)
    
    logging.debug("Latest change at {} for '{}' ".format(formattedTime,latestRevisionFileNamePath))
    
    return latestRevisionTime, latestRevisionFileNamePath

def applyPreflightDef(IDFpath,variant,IDDobj):
    IDFobj = idf.IDF.fromIdfFile(IDFpath)

    #=======================================================================
    # CLEAN OUT
    #=======================================================================
    idf.cleanOutObject(IDFobj,idf.keptClassesDict['onlyGeometry'])
    idf.applyDefaultConstNames(IDFobj, IDDobj)


    #=======================================================================
    # APPLY TEMPLATES
    #=======================================================================
    for templateDef in variant["templates"]:
        #print templateDef
        
        with loggerCritical():
            templatePath = idf.getTemplatePath(IDF_TEMPLATE_PATH,templateDef['templateName'])
            templateIDF = idf.IDF.fromIdfFile(templatePath)
        #thisTemplate = loadTemplates(IDF_TEMPLATE_PATH, templateDef['templateName']) # Get the template IDF
        
        #logging.info("Working on template {}".format())
        idf.applyTemplate(IDFobj,IDDobj,templateIDF,templateDef['zones'],templateDef['templateName'],templateDef['uniqueName'] ) # Apply it
        
    #=======================================================================
    # APPLY CHANGES
    #=======================================================================
    for change in variant["changes"]:
        #pass
        #print change
        idf.applyChange(IDFobj, IDDobj, change)
    
    #outputFileName = "output.idf"
    #fullOutputPath = monitorDir + "\\" + outputFileName
    
    return IDFobj


def executeIDF(IDFobj,ePlusEXEpath,monitorDir,weatherFilePath,pathIdfOutput,varName):

    executionCommand = [ePlusEXEpath, monitorDir, "Main_r05", monitorDir + "\\", weatherFilePath]
    #print IDFobj
    #print executionCommand
    #"inputfilepath" "outputfilepath" "weatherfilepath"
    
    fullInputPath= pathIdfOutput + "\\" + varName + ".idf"
    fullOutputPath = pathIdfOutput + "\\" + varName
    IDFobj.writeIdf(fullInputPath)            
    
    if 0:
#                logging.debug("Executing the batch file {}".format(ePlusEXEpath))
        logging.debug("Executing command {}".format(executionCommand))
        logging.debug("File {}".format(IDFobj))

        #os.system(executionCommand)
        subprocess.call(executionCommand)

        openTheErrorFile(monitorDir)


def getIDDobject():
    # Path to IDD XML (In the SVN repo)
    thisProjRoot = split_up_path(os.getcwd())[:4] 
    path_IDD_XML = thisProjRoot + ["SampleIDFs"] + ["Energy+idd.xml"]
    path_IDD_XML = os.path.join(*path_IDD_XML)
    IDDobj = idf.IDF.fromXmlFile(path_IDD_XML)
        
    return IDDobj

def getPreflightVariantDef():
    thisProjDefRoot = FREELANCE_DIR
    
    preFlightDefinitionPath = PYTHON_ECLIPSE + r"\PyIDF\ExcelTemplates\PreFlight.xlsx"
    thisExcelProjPath = os.path.abspath(preFlightDefinitionPath)

    variant = idf.loadVariants(thisExcelProjPath)
    return variant['Preflight']
    
def monitorStandard(monitorDir,
                    ePlusEXEpath,
                    weatherFilePath,
                    preFlightDefinitionPath,
                    templatesFileAbsPath,
                    templatesFileDirStem):
    
    logging.debug("RUNNING ")
    
    if re.search(r"\s",monitorDir):
        raise Exception("No spaces allowed in path names!")
    getPreflightVariantDef()
    

    # Path to output dir
    pathIdfOutput = FREELANCE_DIR + r"\\IDFout\\"
    
    # Weather file
    pathWeather = thisProjDefRoot + r"\\081_CentralTowerFinal\WEA\SVK_Bratislava.118160_IWEC.epw"
    
    # All variants
    logging.info("Getting project definition: {}".format(thisExcelProjPath))
    
    # Get the definition
    
    #print variant
    for x,y in variant.iteritems():
        varName =  x
        variant = y
        
    sourceFileDir = monitorDir
    
    targetRunDir = sourceFileDir + "out\\"
    
    extensionFilter = ".idf"
    
    while(1):
        
        time.sleep(1)
        
        (latestRevisionTime, latestRevisionPath) = getLatestChangedFile(sourceFileDir, extensionFilter)
        
        lastRevTime = 0 
       
        if latestRevisionTime > lastRevTime:
            
            logging.debug("Change found! Wait for write")
            
            time.sleep(1)

            lastRevTime = latestRevisionTime
            variant['source'] = latestRevisionPath
            
            # Apply the pre-flight project definition to the IDF
            
            IDFobj = applyPreflightDef(IDFobj,variant,IDDobj)
        
            executeIDF(ePlusEXEpath,monitorDir,weatherFilePath)
            
        else:
            logging.debug("No new IDF files found!")

#===============================================================================
# Unit testing
#===============================================================================

class allTests(unittest.TestCase):
    @unittest.skip("")
    def test010_SimpleCreation(self):
        print "**** TEST {} ****".format(get_self())
        monitorDir = r"C:\Users\Anonymous2\Desktop\SKPOSM"
        ePlusEXEpath = r"C:\EnergyPlusV7-2-0\RunEPlus MINE Version 2.bat"
        
        weatherFilePath = PYTHON_ECLIPSE + r"\PyIDF\ExcelTemplates\SVK_Bratislava.118160_IWEC.epw"
        preFlightDefinitionPath = PYTHON_ECLIPSE + r"\PyIDF\ExcelTemplates\PreFlight.xlsx"
        templatesFileAbsPath = ""
        templatesFileDirStem =""
        
        
        monitorStandard(monitorDir,
                    ePlusEXEpath,
                    weatherFilePath,
                    preFlightDefinitionPath,
                    templatesFileAbsPath,
                    templatesFileDirStem)
        
    def test020_simpleCentral(self):
        IDDobj = getIDDobject()
        variant = getPreflightVariantDef()
        
        #for k,v in variant.iteritems():
        #    print k,v
        
        IDFpath = r"C:\Projects2\081_CentralTowerFinal\OSM2\Proposed r00.idf"
        pathIdfOutput = r"C:\Projects2\IDFout\output.idf"
        IDFobj = applyPreflightDef(IDFpath,variant,IDDobj)
        IDFobj.writeIdf(pathIdfOutput)
        
        
        
#========================================================
# Main
#===============================================================================
if __name__ == "__main__":
    print ABSOLUTE_LOGGING_PATH
    logging.config.fileConfig(ABSOLUTE_LOGGING_PATH)
    
    
    myLogger = logging.getLogger()
    myLogger.setLevel("DEBUG")

    logging.debug("Started _main".format())
    
    unittest.main()
        
    logging.debug("Finished _main".format())
    
    
    
    
    
    
    
    
            

def OLDmonitorStandard(monitorDir,
                    ePlusEXEpath,
                    weatherFilePath,
                    preFlightDefinitionPath,
                    templatesFileAbsPath,
                    templatesFileDirStem):
    logging.debug("RUNNING ")
    
    if re.search(r"\s",monitorDir):
        raise Exception("No spaces allowed in path names!")

    #===============================================================================
    # Template file, weather, group, variants
    #===============================================================================

    templatesList = IDF.loadTemplates(templatesFileAbsPath, templatesFileDirStem)
                          
    preFlightDefinition = IDF.loadVariants(os.path.abspath(preFlightDefinitionPath),"",)[0]
    
    sourceFileDir = monitorDir
    
    targetRunDir = sourceFileDir + "out\\"
    
    extensionFilter = ".idf"
    
    outputDirRel = "\CleanedOut\\"

    writtenCleanedFileRelPath = outputDirRel + "in.idf"

    outputDirAbs = sourceFileDir + outputDirRel
    
    lastRevTime = 0 
    
    while(1):
        
        time.sleep(1)
        
        (latestRevisionTime, latestRevisionPath) = getLatestChangedFile(sourceFileDir, extensionFilter)

        if latestRevisionTime > lastRevTime:
            
            logging.debug("Change found! Wait for write")
            
            time.sleep(5)
            
            lastRevTime = latestRevisionTime
            
            thisIDF = IDF.IDF(
                pathIdfInput=latestRevisionPath, 
                XML=None, 
                IDFstring = None, 
                IDstring = None, 
                description = None, 
                pathIdfOutput = sourceFileDir + writtenCleanedFileRelPath
                )
        
            # Call the load        
            thisIDF.loadIDF()
            # Call convert
            thisIDF.parseIDFtoXML()
            #thisIDF.cleanOutObject()    
            #print preFlightDefinition.templateDescriptions
            
            thisIDF.cleanOutObject(IDF.keptClassesDict['geometryAndSpaceLoads'])
        
            #thisIDF.DeleteOrphanedZones()
            
            #thisIDF.applyDumbConstructions()
            thisIDF.applyDefaultConstructions()
            #thisIDF.applyFenestrationConstruction()

            for template in preFlightDefinition.templateDescriptions:
                #print template, templatesList
                thisIDF.applyTemplateNewStyle(template,templatesList)
            
            thisIDF.convertXMLtoIDF()
        
            thisIDF.writeIdf(thisIDF.pathIdfOutput)  

            #print latestChangedFilePath
            #executionCommand = ePlusEXEpath + ' "' + thisIDF.pathIdfOutput + '" ' + '"'+weatherFilePath+'"'
            executionCommand = ePlusEXEpath + " " + thisIDF.pathIdfOutput + " " + weatherFilePath + " " + targetRunDir
            executionCommand = ePlusEXEpath + " " + thisIDF.pathIdfOutput + " " + weatherFilePath
            print executionCommand
            
            

            #fh = open("NUL","w")
            #subprocess.Popen(executionCommand, stdout = fh, stderr = fh, shell=False)
            #fh.close()
            
            if 1:
                logging.debug("Executing the batch file {}".format(ePlusEXEpath))
                os.system(executionCommand)
                
                openTheErrorFile(outputDirAbs)
                
        else:
            logging.debug("No new IDF files found!")



def OLD_monitorIDFdirectoryWithoutLoads(monitorDir):
    logging.debug("RUNNING ")
    
    if re.search(r"\s",monitorDir):
        raise Exception("No spaces allowed in path names!")
    
    
    ePlusEXEpath = r"D:\Apps\EnergyPlusV7-0-0\RunEPlusMine.bat"
    weatherFilePath = r"D:\Freelancing\WEA\ARE_Abu.Dhabi.412170_IWEC.epw"
        
    #===============================================================================
    # Template file, weather, group, variants
    #===============================================================================
    templatesFile = r"D:\Freelancing\IDF_Library\Templates.xlsx"
    templatesFileAbsPath = os.path.abspath(templatesFile)
    templatesFileDirStem = r"D:\Freelancing\IDF_Library\\" 
    templatesList = IDF.loadTemplates(templatesFileAbsPath, templatesFileDirStem)
    preFlightDefinitionPath = r"D:\EclipseSpace2\EclipsePython\EvolveDesign\XLS Projects\PreFlight.xlsx"
                          
    preFlightDefinition = IDF.loadVariants(os.path.abspath(preFlightDefinitionPath),"",)[0]
    
    sourceFileDir = monitorDir
    
    targetRunDir = sourceFileDir + "out\\"
    
    extensionFilter = ".idf"
    
    outputDirRel = "\CleanedOut\\"

    writtenCleanedFileRelPath = outputDirRel + "in.idf"

    outputDirAbs = sourceFileDir + outputDirRel
    
    lastRevTime = 0 
    
    while(1):
        
        time.sleep(1)
        
        (latestRevisionTime, latestRevisionPath) = getLatestChangedFile(sourceFileDir, extensionFilter)

        if latestRevisionTime > lastRevTime:
            
            logging.debug("Change found! Wait for write")
            
            time.sleep(5)
            
            lastRevTime = latestRevisionTime
            
            thisIDF = IDF.IDF(
                pathIdfInput=latestRevisionPath, 
                XML=None, 
                IDFstring = None, 
                IDstring = None, 
                description = None, 
                pathIdfOutput = sourceFileDir + writtenCleanedFileRelPath
                )
        
            # Call the load        
            thisIDF.loadIDF()
            # Call convert
            thisIDF.parseIDFtoXML()
            #thisIDF.cleanOutObject()    
            #print preFlightDefinition.templateDescriptions
            
            thisIDF.cleanOutObject(IDF.keptClassesDict['onlyGeometry'])
        
            #thisIDF.DeleteOrphanedZones()
            
            #thisIDF.applyDumbConstructions()
            thisIDF.applyDefaultConstructions()
            #thisIDF.applyFenestrationConstruction()

            for template in preFlightDefinition.templateDescriptions:
                #print template, templatesList
                thisIDF.applyTemplateNewStyle(template,templatesList)
            
            thisIDF.convertXMLtoIDF()
        
            thisIDF.writeIdf(thisIDF.pathIdfOutput)  

            #print latestChangedFilePath
            #executionCommand = ePlusEXEpath + ' "' + thisIDF.pathIdfOutput + '" ' + '"'+weatherFilePath+'"'
            executionCommand = ePlusEXEpath + " " + thisIDF.pathIdfOutput + " " + weatherFilePath + " " + targetRunDir
            executionCommand = ePlusEXEpath + " " + thisIDF.pathIdfOutput + " " + weatherFilePath
            print executionCommand
            
            
            #fh = open("NUL","w")
            #subprocess.Popen(executionCommand, stdout = fh, stderr = fh, shell=False)
            #fh.close()
            
            if 1:
                os.system(executionCommand)
                
                openTheErrorFile(outputDirAbs)
                
        else:
            logging.debug("No new IDF files found!")



def OLD_monitorIDFdirectoryKeepLoads(monitorDir):
    logging.debug("RUNNING ")
    
    if re.search(r"\s",monitorDir):
        raise Exception("No spaces allowed in path names!")
    
    
    ePlusEXEpath = r"D:\Apps\EnergyPlusV7-0-0\RunEPlusMine.bat"
    weatherFilePath = r"D:\Freelancing\WEA\ARE_Abu.Dhabi.412170_IWEC.epw"
        
    #===============================================================================
    # Template file, weather, group, variants
    #===============================================================================
    templatesFile = r"D:\Freelancing\IDF_Library\Templates.xlsx"
    templatesFileAbsPath = os.path.abspath(templatesFile)
    templatesFileDirStem = r"D:\Freelancing\IDF_Library\\" 
    templatesList = IDF.loadTemplates(templatesFileAbsPath, templatesFileDirStem)
    preFlightDefinitionPath = r"D:\EclipseSpace2\EclipsePython\EvolveDesign\XLS Projects\PreFlight.xlsx"
                          
    preFlightDefinition = IDF.loadVariants(os.path.abspath(preFlightDefinitionPath),"",)[0]
    
    sourceFileDir = monitorDir
    
    targetRunDir = sourceFileDir + "out\\"
    
    extensionFilter = ".idf"
    
    outputDirRel = "\CleanedOut\\"

    writtenCleanedFileRelPath = outputDirRel + "in.idf"

    outputDirAbs = sourceFileDir + outputDirRel
    
    lastRevTime = 0 
    
    while(1):
        
        time.sleep(1)
        
        (latestRevisionTime, latestRevisionPath) = getLatestChangedFile(sourceFileDir, extensionFilter)

        if latestRevisionTime > lastRevTime:
            
            logging.debug("Change found! Wait for write")
            
            time.sleep(5)
            
            lastRevTime = latestRevisionTime
            
            thisIDF = IDF.IDF(
                pathIdfInput=latestRevisionPath, 
                XML=None, 
                IDFstring = None, 
                IDstring = None, 
                description = None, 
                pathIdfOutput = sourceFileDir + writtenCleanedFileRelPath
                )
        
            # Call the load        
            thisIDF.loadIDF()
            # Call convert
            thisIDF.parseIDFtoXML()
            #thisIDF.cleanOutObject()    
            #print preFlightDefinition.templateDescriptions
            
            thisIDF.cleanOutObject(IDF.keptClassesDict['geometryAndSpaceLoads'])
        
            #thisIDF.DeleteOrphanedZones()
            
            #thisIDF.applyDumbConstructions()
            thisIDF.applyDefaultConstructions()
            #thisIDF.applyFenestrationConstruction()

            for template in preFlightDefinition.templateDescriptions:
                #print template, templatesList
                thisIDF.applyTemplateNewStyle(template,templatesList)
            
            thisIDF.convertXMLtoIDF()
        
            thisIDF.writeIdf(thisIDF.pathIdfOutput)  

            #print latestChangedFilePath
            #executionCommand = ePlusEXEpath + ' "' + thisIDF.pathIdfOutput + '" ' + '"'+weatherFilePath+'"'
            executionCommand = ePlusEXEpath + " " + thisIDF.pathIdfOutput + " " + weatherFilePath + " " + targetRunDir
            executionCommand = ePlusEXEpath + " " + thisIDF.pathIdfOutput + " " + weatherFilePath
            print executionCommand
            
            
            #fh = open("NUL","w")
            #subprocess.Popen(executionCommand, stdout = fh, stderr = fh, shell=False)
            #fh.close()
            
            if 1:
                os.system(executionCommand)
                
                openTheErrorFile(outputDirAbs)
                
        else:
            logging.debug("No new IDF files found!")
    
    