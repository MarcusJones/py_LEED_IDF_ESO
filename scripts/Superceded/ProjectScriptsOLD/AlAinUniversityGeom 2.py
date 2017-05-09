import logging.config
import os
import sys
import IDF
import csv

# Load the logging configuration
logging.config.fileConfig('..\\LoggingConfig\\loggingNofile.conf')

logging.info("Started Al Ain Geometry Processing  script")

inputDirectoryPath = r"D:\Freelancing\046_Al_Ain_Tech_Two\SKP_OSM3"
#inputDirectoryPath = r"D:\Freelancing\000_TestProject\Simple geometry"
outputDirectoryPath = r"D:\Freelancing\046_Al_Ain_Tech_Two\SKP_OSM4"
#outputDirectoryPath = inputDirectoryPath

#fileDescriptions = [
#                    {
#                     "filename":"simple.osm",
#                     "outname":"simpleOut.osm",
#                     "tag":"Basement",
#                     },
#             ]

fileDescriptions = [
                    {
                     "filename":"Basement_r06.osm",
                     "outname":"Basement_TESTING.osm",
                     "tag":"Basement",
                     },
             ]

#for  in fileDescriptions:
#    print k,v
#    
#fullFilePaths = [os.path.normpath(os.path.join(directoryPath,name)) for name in fileNames]


for fileDesc in fileDescriptions:
    thisIDF = IDF.IDF(
        pathIdfInput=os.path.normpath(os.path.join(inputDirectoryPath,fileDesc["filename"])),
        XML=None, 
        IDFstring = None, 
        IDstring = None, 
        description = None, 
        pathIdfOutput = None,
        )
    
    # Call the load        
    thisIDF.loadIDF()
    # Call convert
    thisIDF.parseIDFtoXML()
    thisIDF.cleanOutObject(IDF.keptClassesDict['openStudioGeomNoZones'])
    #thisIDF.cleanOutObject()
    thisIDF.convertXMLtoIDF()
    
    thisIDF.deleteClasses("OS:ThermalZone")
    
    #thisIDF.addZonesToSpaces()
    thisIDF.renameSpaces(fileDesc["tag"])
    thisIDF.renameSurfaces(fileDesc["tag"])
    thisIDF.convertXMLtoIDF()
    thisIDF.writeIdf(os.path.normpath(os.path.join(outputDirectoryPath,fileDesc["outname"])))
    #print newIDF
    
#    if newIDF:
#        newIDF.merge(thisIDF)
#    else:
#        newIDF = thisIDF
#        
#print "Final Clean"
#
##newIDF.cleanOutObject()
##newIDF.cleanOutOpenStudio()
#newIDF.convertXMLtoIDF()
#newIDF.writeIdf(r"c:\Freelance\Simulation\test.osm")
#newIDF.writeXml(r"c:\Freelance\Simulation\test.xml")

logging.info("Finshed Al Ain Geometry Processing  script")
