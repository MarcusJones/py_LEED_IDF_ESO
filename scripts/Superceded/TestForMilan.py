'''
Created on Aug 3, 2011

@author: Marcus Jones
'''

import logging.config
from config import *
#import idf_xml.IDF.IDF as IDF
from idf_xml.IDF import IDF,loadVariants,assembleVariants,printXML
from idf_xml.IDF import treeGetClass,getPositionOfATTR,cleanOutObject,xpathRE
from idf_xml.IDF import keptClassesDict
from idf_xml.IDF import idfGetZoneNameList,loadTemplates,IDDboolMatchField, xmlTextReplace 
from idf_xml.IDF import IDDgetMatchedPosition
from idf_xml.IDF import printStdTable,getAllObjectsTable, applyTemplate

from UtilityPathsAndDirs import splitUpPath,getNewerFileRevName
from idf_xml.Utilities import idStr
from copy import deepcopy
import re
    # Path to IDD XML




def testProject():
    thisProjRootPath = r"C:\Users\Anonymous\Desktop\5ZoneAirCooled.idf"
    IDFobj = IDF.fromIdfFile(thisProjRootPath)
    
    thisProjXMLpath = r"C:\Users\Anonymous\Desktop\5ZoneAirCooled.xml"
    thisProjOutPath = r"C:\Users\Anonymous\Desktop\5ZoneAirCooledMARCUS.idf"
    #IDFobj.writeXml(thisProjXMLpath)
    
    #print IDFobj.XML.xpath("//CLASS")
    
    #for item in IDFobj.XML.xpath("//CLASS"):
        #pass
        #print item.text
    
    #print idfGetZoneNameList(IDFobj, zoneName='SPACE')
    #printStdTable(getAllObjectsTable(IDFobj))
    
    IDFobj = cleanOutObject(IDFobj,keptClassesDict['onlyGeometry'])
    
    
    IDFobj.writeIdf(thisProjOutPath)
    
    
    template = loadTemplates(r"C:\Projects\IDF_Library\HVAC templates", filterRegExString = "HVAC FanCoil plus DOAS", flgExact = True)[0]
    
    #print template
    thisProjRoot = splitUpPath(os.getcwd())[:4] 
    path_IDD_XML = thisProjRoot + ["SampleIDFs"] + ["Energy+idd.xml"]
    path_IDD_XML = os.path.join(*path_IDD_XML)
    IDDobj = IDF.fromXmlFile(path_IDD_XML)

    IDFobj = applyTemplate(IDFobj,IDDobj,template)
    IDFobj.writeIdf(thisProjOutPath)
    raise 
    
    # Path to XLS definition 
    thisTestExcelProj = "\\".join(thisProjRoot) + r"\ExcelTemplates\Input Data Tower SO03 r06.xlsx"
    thisTestExcelProj = thisTestExcelProj
    
    # Path to full IDD
    pathIDDsample2 = thisProjRoot + ["SampleIDFs"] + ["Energy+.idd"]  
    pathIDDfull = os.path.join(*pathIDDsample2)
    
    # Path to an actual model file
    path_CentralTower = thisProjRoot + ["SampleIDFs"] + ["r00 MainIDF.idf"]
    path_CentralTower = os.path.join(*path_CentralTower)
    
    # Path to IDD XML
    path_IDD_XML = thisProjRoot + ["SampleIDFs"] + ["Energy+idd.xml"]
    path_IDD_XML = os.path.join(*path_IDD_XML)
    
    # Path to output final IDF
    pathIdfOutput = r"c:\temp\final.idf"


    thisProjRoot = splitUpPath(os.getcwd())[:4] 

    variants = loadVariants(thisTestExcelProj)
#    print variants
#    myVariants = list()
#    for variant in variants:
#        #print variant
#        print variant["source"] 
#        variant["source"] = path_CentralTower # Update source
#        myVariants.append(variant)
    # Customize for test
    myVariant = variants.itervalues().next() # Get one variant
    myVariant["source"] = path_CentralTower # Update source
    myVariants = [myVariant]
    variants = myVariants
    
    for variant in variants:
        #=======================================================================
        # GET IDF
        #=======================================================================
        IDFobj = IDF.fromIdfFile(variant['source'])
        
        #print "OUTPUT: Zone Names"
        for zoneName in idfGetZoneNameList(IDFobj):
            #print zoneName
            pass
        
        #=======================================================================
        # CLEAN OUT
        #=======================================================================
        IDFobj = cleanOutObject(IDFobj,keptClassesDict['onlyGeometry'])
        
        #=======================================================================
        # APPLY TEMPLATES
        #=======================================================================
        #""" # SKIP TEMP 
        for templateDef in variant["templates"]:
            # Get the template IDF
            thisTemplate = loadTemplates(IDF_TEMPLATE_PATH, templateDef['templateName'])
            assert(len(thisTemplate) == 1), "Template; {} found {} matches {}".format(templateDef['templateName'],
                            len(thisTemplate),thisTemplate)
            thisTemplate = thisTemplate[0]
            logging.debug(idStr("Processing template; {}".format(templateDef['templateName']),IDFobj.ID)) 
            
            # Apply it
            IDFobj = applyTemplate(IDFobj,IDDobj,thisTemplate)
        #"""
        #=======================================================================
        # APPLY CHANGES
        #=======================================================================
        """ # SKIP TEMP
        for change in variant["changes"]:
            IDFobj = applyChange(IDFobj, IDDobj, change)
            """ # SKIP TEMP

        IDFobj = addZoneHVAC(IDFobj)
        
        #printXML(IDFobj.XML)
        
        newPathIdfOutput = getNewerFileRevName(pathIdfOutput)
        
        IDFobj.writeIdf(newPathIdfOutput)

    
    
if __name__ == "__main__":
    # Load the logging configuration
    logging.config.fileConfig(ABSOLUTE_LOGGING_PATH)
    
    logging.info("Started IDF test script")
    
    testProject()

    logging.info("Finished IDF test script")                
    