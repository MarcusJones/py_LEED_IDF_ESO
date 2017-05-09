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


def testProject():
    thisProjDefRoot = FREELANCE_DIR
    
    # Path to project IDF
    
    path_IDF = [thisProjDefRoot] + [r"123_Twin_Riga_ENE5\01 ENE 1 reports\Riga II"] + [r"Riga_II_ene.idf"]
    path_IDF = os.path.join(*path_IDF)
    
    # Path to IDD XML (In the SVN repo)
    thisProjRoot = splitUpPath(os.getcwd())[:4] 
    path_IDD_XML = thisProjRoot + ["SampleIDFs"] + ["Energy+idd.xml"]
    path_IDD_XML = os.path.join(*path_IDD_XML)
    IDDobj = idf.IDF.fromXmlFile(path_IDD_XML)
    
    # Path to output dir
    pathIdfOutput = FREELANCE_DIR + r"\\IDFout"
    
    # Weather file
    pathWeather = r"C:\Projects\081_CentralTowerFinal\WEA\SVK_Bratislava.118160_IWEC.epw"
    
    IDFobj = idf.IDF.fromIdfFile(path_IDF)
    
    zoneNames = idf.idfGetZoneNameList(IDFobj, zoneName='1NP%B:1NP%B%retail%core%1')
    xpathSearch = r"OBJECT/CLASS[text() = '{}']/../ATTR[{}][text()='{}']/..".format(className,position,listName)

    equipList = xpathRE(IDFobj.XML, xpathSearch)
    print zoneNames
    

    raise

    variants = idf.loadVariants(thisTestExcelProj)
    for varName,variant in variants.iteritems():
        logging.info("Working on variant {}: {}".format(varName,variant))
 
        #=======================================================================
        # GET IDF
        #=======================================================================
        #print variant
        IDFobj = idf.IDF.fromIdfFile(variant['source'])
        
        #print "OUTPUT: Zone Names"
        for zoneName in idf.idfGetZoneNameList(IDFobj):
            #print zoneName
            pass
        
        #=======================================================================
        # CLEAN OUT
        #=======================================================================
        IDFobj = idf.cleanOutObject(IDFobj,idf.keptClassesDict['onlyGeometry'])
        
        #=======================================================================
        # APPLY TEMPLATES
        #=======================================================================
        for templateDef in variant["templates"]:
            with loggerCritical():
                templatePath = idf.getTemplatePath(IDF_TEMPLATE_PATH,templateDef['templateName'])
                templateIDF = idf.IDF.fromIdfFile(templatePath)
            #thisTemplate = loadTemplates(IDF_TEMPLATE_PATH, templateDef['templateName']) # Get the template IDF
            idf.applyTemplate(IDFobj,IDDobj,templateIDF) # Apply it
            
        #=======================================================================
        # APPLY CHANGES
        #=======================================================================
        for change in variant["changes"]:
            #pass
            idf.applyChange(IDFobj, IDDobj, change)

        #IDFobj = vrv.addZoneHVAC(IDFobj)
        #idf.printXML(IDFobj.XML)
        #vrv.addTerminals(IDFobj)
        #vrv.getZoneHVAC(IDFobj)
        #printXML(IDFobj.XML)
        
        #newPathIdfOutput = getNewerFileRevName(pathIdfOutput)
        fullOutPath= pathIdfOutput + "\\" + varName + ".idf"
        IDFobj.writeIdf(fullOutPath)
        groupName = "00myGroup"
        groupFilePath = pathIdfOutput + r"\\" + groupName + ".epg"
        csvout = csv.writer(open(groupFilePath, 'ab'))
        
        thisRow = [fullOutPath,pathWeather,pathIdfOutput,"1"]
        csvout.writerow(thisRow)
            
    #logging.info("Wrote the {0} variants to the group simulation file at: {1}".format(len(variantsList),groupFilePath))     
         
    
if __name__ == "__main__":
    # Load the logging configuration
    logging.config.fileConfig(ABSOLUTE_LOGGING_PATH)
    
    logging.info("Started IDF test script")
    
    testProject()

    logging.info("Finished IDF test script")                
    