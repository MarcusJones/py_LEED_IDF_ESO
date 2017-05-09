'''
Created on Jan 11, 2012

@author: UserXP
'''
'''
Created on Aug 3, 2011

@author: UserXP
'''

import logging.config
import os
import sys
sys.path.insert(0, "c:\EclipsePython\EvolveDesign\src")
import IDF
print IDF
import sys
print sys.path
import csv


# Load the logging configuration
#logging.config.fileConfig('..\\LoggingConfig\\logging.conf')

logging.config.fileConfig('..\\LoggingConfig\\loggingNofile.conf')

directoryPath = r"D:\Freelancing\046_Al_Ain_Tech_Two\SKP_OSM3"

#fileNames = ["Basement_r01.osm",
#             "Ground_Floor_r04_diagnostic.osm",
#             "First_Floor_r01_diagnostic.osm",
#             "Second_Floor_r01.osm",
#             ]

fileNames = ["Basement_r05.osm",
             "Ground_Floor_r25.osm",
             "First_Floor_r19.osm",
             "Second_Floor_r21.osm",
             "Third_Floor_r26.osm",
             ]
fullFilePaths = [os.path.normpath(os.path.join(directoryPath,name)) for name in fileNames]



#blankIdfFile = IDF.IDF(
#        pathIdfInput="any", 
#        XML=None, 
#        IDFstring = None, 
#        IDstring = None, 
#        description = None, 
#        pathIdfOutput = r"c:\Freelance\Simulation\test.idf"
#        )

#newIDF = ""

tempCount = 0

for thisFilePath in fullFilePaths:
    thisIDF = IDF.IDF(
        pathIdfInput=thisFilePath, 
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
    #print IDF.keptClassesDict2
    for k in IDF.keptClassesDict.keys():
        print k
    thisIDF.cleanOutObject(IDF.keptClassesDict['OSNoZonesOrShades'])

    #thisIDF.cleanOutOpenStudio()
    #thisIDF.cleanOutObject()
    thisIDF.convertXMLtoIDF()
    

    thisIDF.convertXMLtoIDF()
    thisIDF.writeIdf(r"D:\Freelancing\Simulation\testNoShade" + str(tempCount) + ".osm")
    tempCount += 1
        
print "Final Clean"

#newIDF.cleanOutObject()
#newIDF.cleanOutOpenStudio()
#newIDF.convertXMLtoIDF()
#newIDF.writeIdf(r"D:\Freelancing\Simulation\test.osm")
#newIDF.writeXml(r"c:\Freelance\Simulation\test.xml")
logging.info("Finshed Al Ain Geometry Processing  script")
