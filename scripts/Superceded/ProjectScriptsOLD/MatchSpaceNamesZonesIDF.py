
import logging.config
#from UtilityInspect import whoami, whosdaddy
import IDF
import re
import os
#from UtilityPathsAndDirs import getLatestRevison
import subprocess
import time
import datetime

class MyClass(object):
    def __init__(self, aVariable): 
        pass
    
class MySubClass(MyClass):
    def __init__(self, aVariable): 
        super(MySubClass,self).__init__(aVariable)



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

    for filename in os.listdir(theDir):

        #basename, extension = filename.split('.')
        base, extension = os.path.splitext(filename)
        #print base, extension
        if extension == ".err":
            thePath = os.path.normpath(theDir + filename)
            theEXE = r"D:\Apps\Notepad++\notepad++.exe"
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
    
def _001_MoravcikOLD():
    logging.debug("RUNNING Moravcik ")
    
    sourceFileAbsPath = r"D:\Freelancing\002_Moravcik\SKP_OSM\r25 - Start naming_just numbers.osm"
    
    targetDirAbsPath = r"D:\Freelancing\OutputSpaceZoneConvert\test.osm"
    
    thisIDF = IDF(
        pathIdfInput=sourceFileAbsPath, 
        XML=None, 
        IDFstring = None, 
        IDstring = None, 
        description = None, 
        pathIdfOutput = targetDirAbsPath
        )
        
    # Call the load        
    thisIDF.loadIDF()
    # Call convert
    thisIDF.parseIDFtoXML()
    #thisIDF.cleanOutObject()

    thisIDF.convertXMLtoIDF()
    
    
    ### GET SPACES ###
    xpathSearch = "//CLASS[re:match(text(), '^OS:Space$')]/.."
    #xpathSearch = "//OBJECT/CLASS[re:match(text(), '" + className + "')]/"
    spaces = thisIDF.querySelfRE(xpathSearch)
    logging.debug("Loaded {} spaces".format(len(spaces)))

    
    ### GET ZONES ###
    xpathSearch = "//CLASS[re:match(text(), '^OS:ThermalZone')]/.."
    #xpathSearch = "//OBJECT/CLASS[re:match(text(), '" + className + "')]/"
    zones = thisIDF.querySelfRE(xpathSearch)
    logging.debug("Loaded {} zones".format(len(zones)))
    
    for space in spaces:
        thisSpaceName = space.xpath("ATTR")[0].text
        thisSpacePointsToZoneName = space.xpath("ATTR")[9].text
        found = False
        for zone in zones:
            zoneName = zone.xpath("ATTR")[0].text
            if re.search("^"+zoneName+"$",thisSpacePointsToZoneName):
                print "Match"
                print "Space: {}, Space points to {}, Zone exists here: {}".format(thisSpaceName,thisSpacePointsToZoneName,zoneName)
                newZoneName =  "ZONE " + thisSpaceName
                print "New name:" + newZoneName
                found = True
                
                space.xpath("ATTR")[9].text = newZoneName
                zone.xpath("ATTR")[0].text =  newZoneName
        if not found:
            print "NO MATCH"
    
    
    thisIDF.convertXMLtoIDF()
            
    thisIDF.writeIdf(thisIDF.pathIdfOutput)    
    
    logging.debug("FINISHED Moravcik ")

def _001_KaliskyOLD():
    logging.debug("RUNNING Moravcik ")
    
    sourceFileAbsPath = r"D:\Freelancing\001_Kalisky\SKP_OSM\Kalisky r31 Floors Finished.osm"
    
    targetDirAbsPath = r"D:\Freelancing\OutputSpaceZoneConvert\Kalisky.osm"
    
    getLatestRevision()
    
    thisIDF = IDF(
        pathIdfInput=sourceFileAbsPath, 
        XML=None, 
        IDFstring = None, 
        IDstring = None, 
        description = None, 
        pathIdfOutput = targetDirAbsPath
        )
        
    # Call the load        
    thisIDF.loadIDF()
    # Call convert
    thisIDF.parseIDFtoXML()
    #thisIDF.cleanOutObject()

    thisIDF.convertXMLtoIDF()
    
    
    ### GET SPACES ###
    xpathSearch = "//CLASS[re:match(text(), '^OS:Space$')]/.."
    #xpathSearch = "//OBJECT/CLASS[re:match(text(), '" + className + "')]/"
    spaces = thisIDF.querySelfRE(xpathSearch)
    logging.debug("Loaded {} spaces".format(len(spaces)))

    
    ### GET ZONES ###
    xpathSearch = "//CLASS[re:match(text(), '^OS:ThermalZone')]/.."
    #xpathSearch = "//OBJECT/CLASS[re:match(text(), '" + className + "')]/"
    zones = thisIDF.querySelfRE(xpathSearch)
    logging.debug("Loaded {} zones".format(len(zones)))
    
    ### LOOP Both ###
    for space in spaces:
        thisSpaceName = space.xpath("ATTR")[0].text
        thisSpacePointsToZoneName = space.xpath("ATTR")[9].text
        found = False
        for zone in zones:
            zoneName = zone.xpath("ATTR")[0].text
            if re.search("^"+zoneName+"$",thisSpacePointsToZoneName):
                print "Match"
                print "Space: {}, Space points to {}, Zone exists here: {}".format(thisSpaceName,thisSpacePointsToZoneName,zoneName)
                newZoneName =  "ZONE " + thisSpaceName
                print "New name:" + newZoneName
                found = True
                
                space.xpath("ATTR")[9].text = newZoneName
                zone.xpath("ATTR")[0].text =  newZoneName
        if not found:
            print "NO MATCH"
            raise
    
    
    thisIDF.convertXMLtoIDF()
            
    thisIDF.writeIdf(thisIDF.pathIdfOutput)    
    
    logging.debug("FINISHED Moravcik ")

def _KaliskyHardCheckOLD():
    
    #sourceFileAbsPath = r"D:\Freelancing\001_Kalisky\SKP_OSM\Kalisky r31 Floors Finished.osm"
    
    targetDirAbsPath = r"D:\Freelancing\OutputSpaceZoneConvert\Kalisky.osm"

    sourceFileDir = r"D:\Freelancing\001_Kalisky\SKP_OSM\\"
    
    extensionFilter = ".osm"
    
    latestRevisionPath = getLatestRevison(sourceFileDir, extensionFilter)

    thisIDF = IDF(
        pathIdfInput=latestRevisionPath, 
        XML=None, 
        IDFstring = None, 
        IDstring = None, 
        description = None, 
        pathIdfOutput = targetDirAbsPath
        )
        
    # Call the load        
    thisIDF.loadIDF()
    # Call convert
    thisIDF.parseIDFtoXML()
    #thisIDF.cleanOutObject()


    thisIDF.DeleteOrphanedZones()

    
    #thisIDF.convertXMLtoIDF()
    #thisIDF.writeIdf(thisIDF.pathIdfOutput)    

def _monitorIDFdirectoryWithoutLoads(monitorDir):
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

def _monitorIDFdirectoryKeepLoads(monitorDir):
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

            
def _KaliskyForceClean():
    logging.debug("RUNNING ")
    
    
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
    
    #preFlightDefinition.sourceFileAbsPath = 
        
    
    sourceFileDir = r"D:\Freelancing\001_Kalisky\SKP_OSM\\"
    
    targetRunDir = sourceFileDir + "out\\"
    
    extensionFilter = ".idf"
    
    
    outputDirRel = "\CleanedOut\\"

    writtenCleanedFileRelPath = outputDirRel + "in.idf"

    outputDirAbs = sourceFileDir + outputDirRel
        
    (latestRevisionTime, latestRevisionPath) = getLatestRevison(sourceFileDir, extensionFilter)
    
    latestChangedFile = getLatestChangedFile(sourceFileDir, extensionFilter)
    
    latestChangedFilePath = os.path.join(sourceFileDir, latestChangedFile)
    
    #print 
    
    thisIDF = IDF.IDF(
        pathIdfInput=latestChangedFilePath, 
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
    
    thisIDF.applyDumbConstructions()
    
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
    
    time.sleep(1)
    
    #fh = open("NUL","w")
    #subprocess.Popen(executionCommand, stdout = fh, stderr = fh, shell=False)
    #fh.close()
    
    if 0:
        os.system(executionCommand)
        
        openTheErrorFile(outputDirAbs)
    
def orphanedZoneCleanup(osmDir):
    logging.debug("RUNNING ")
    
    #sourceFileDir = r"D:\Freelancing\001_Kalisky\SKP_OSM\\"
    sourceFileDir = osmDir
    extensionFilter = ".osm"
    
    #latestRevisionPath = getLatestRevison(sourceFileDir, extensionFilter)
    
    (latestRevisionTime, latestRevisionPath) = getLatestChangedFile(sourceFileDir, extensionFilter)
    
    thisIDF = IDF.IDF(
        pathIdfInput=latestRevisionPath, 
        XML=None, 
        IDFstring = None, 
        IDstring = None, 
        description = None, 
        pathIdfOutput = latestRevisionPath
        )
    
    
    # Call the load        
    thisIDF.loadIDF()
    # Call convert
    thisIDF.parseIDFtoXML()
    #thisIDF.cleanOutObject()
    
    thisIDF.DeleteOrphanedZones()
    
    thisIDF.convertXMLtoIDF()
    
    thisIDF.writeIdf(thisIDF.pathIdfOutput)    

def _testing():
    logging.debug("RUNNING TESTS {}")
    
    logging.debug("FINISHED TESTS {}")

if __name__ == "__main__":
    logging.config.fileConfig('..\\LoggingConfig\\loggingNofile.conf')
    logging.debug("Started _main".format())

    #_001_Moravcik()
    #_001_Kalisky()
       # CheckOrphanedZones(zones,spaces):
    #_KaliskyHardCheck()
    
    
    #_KaliskyOrphanedZoneCleanup()
    #_KaliskyForceClean()
    
    #orphanedZoneCleanup(r"D:\Freelancing\002_Moravcik\SKP_OSM\\")
    
    #_monitorIDFdirectory(r"D:\Freelancing\001_Kalisky\SKP_OSM\\")
    #_monitorIDFdirectory(r"D:\Freelancing\002_Moravcik\SKP_OSM\\")
    #_monitorIDFdirectory(r"D:\Freelancing\001_Kalisky_With_Atrium\SKP_OSM\\")
    #_monitorIDFdirectory(r"D:\Freelancing\002_Moravcik\SKP_OSM_Deleted_Atrium\\")
    #print re.search(r"\s",r"D:\Freelancing\RomaniTower\SKP_OSM")
    #_monitorIDFdirectoryWithoutLoads(r"D:\Freelancing\046_Al_Ain_Tech_Th\SKP_OSM")
    _monitorIDFdirectoryKeepLoads(r"D:\Freelancing\046_Al_Ain_Tech_Th\SKP_OSM")

    #_testing()
    
    logging.debug("Started _main".format())
    