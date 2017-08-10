"""
Created on Aug 3, 2011

@author: Marcus Jones

Template demonstrates how to run the IDF script to create variants from excel file
"""
#--- SETUP Config
from config import *
#import unittest

#--- SETUP Logging
import logging.config
print(ABSOLUTE_LOGGING_PATH)
logging.config.fileConfig(ABSOLUTE_LOGGING_PATH)
myLogger = logging.getLogger()
myLogger.setLevel("DEBUG")

#--- SETUP Standard modules
import os
import re
import csv
from pprint import pprint
from collections import defaultdict
from shutil import copyfile

#--- SETUP 3rd party modules

#--- SETUP Custom modules
#from utility_inspect import get_self
#import utilities_idf as util_idf
from idf_parser import IDF as IDF 
#from utility_print_table import PrettyTable,printTable
from utility_logger import LoggerCritical, LoggerDebug
from utility_path import get_files_by_ext_recurse, get_latest_rev, copy_file
#from utility_excel_api import ExtendedExcelBookAPI
from utility_excel import ExcelBookRead2
from kept_classes import kept_classes_dict
from utility_inspect import list_attrs, list_object
import utilities_xml as util_xml
from util_pretty_print import print_table

PROJ_LIDL = {
                  'path_proj_excel' : r'C:\Dropbox\16336 LIDL\IDF Project\\',
                  'idf_base' : r'C:\Dropbox\16336 LIDL\IDF Project\IDF\\',
                  'weather_file' : r'C:\Dropbox\16336 LIDL\Weather\SVN_Ljubljana.130140_IWEC.epw',
                  'output_dir' : r"C:\IDF_OUT\\",
                  'path_weather_file' : r"C:\Dropbox\16336 LIDL\Weather\SVN_Ljubljana.130140_IWEC.epw",
                  'idf_output_dir' :r"C:\Dropbox\16336 LIDL\IDF Project\OUTPUT\\", 
                  }

proj = PROJ_LIDL

def load_variants(inputExcelPath,path_idf_base):
    
    logging.debug("Loading variants from {0}".format(inputExcelPath))
    
    # Attach the book
    #book = ExtendedExcelBookAPI(inputExcelPath)
    with ExcelBookRead2(inputExcelPath) as book: 
        #--- Select the sheet
        #variants_table = book.get_table_2("(Variants)", startRow = 0, endRow=None, startCol=0, endCol=None)
        variants_table = book.get_table_all("(Variants)")
        #print_table(variants_table) 
        
        #--- Get variant sub-table
        try:
            variant_block_limits = [variants_table.index(row) for row in variants_table if row[0]]
        except:
            print(variants_table)
            raise

        #--- Process this sub-table
        variants = dict()
        while len(variant_block_limits) > 1:
            startRow = variant_block_limits[0]
            endRow = variant_block_limits[1]
            
            #print "This variant table", 
            variant_block_limits.pop(0)
            #print variants_table
            variantName = variants_table[startRow][0]
            logging.debug("Working on {} table, rows {} to {}".format(variantName,startRow, endRow))
            
            if variantName in variants:
                raise Exception("Duplicate variant name {}".format(variants_table[startRow][0]))
            
            rawTable = variants_table[startRow:endRow]
            description = rawTable[0][2]
            logging.debug("Description: {}".format(description))
            
            #--- Process source path
            sourcePathDefinition = rawTable[0][3]
            logging.debug("Source path definition: {}".format(sourcePathDefinition))
            
            sourcePath = path_idf_base + sourcePathDefinition
            
            #--- Flags
            flagIndices = [rawTable.index(row) for row in rawTable if row[1].strip() == "flag"]
            flagDefs =  [{"flag":rawTable[ind][2],
                    "argument":rawTable[ind][3]}
                    for ind in flagIndices]
            
            #logging.debug("{} flags".format(len(flagDefs)))

            
            #--- Deletes
            deleteIndices = [rawTable.index(row) for row in rawTable if row[1].strip() == "del"]
            deleteDefs =  [{"class":rawTable[ind][2],
                    "objName":rawTable[ind][3]}
                    for ind in deleteIndices]

            #logging.debug("{} deletions".format(len(deleteDefs)))

            
            #--- Templates
            templateIndices = [rawTable.index(row) for row in rawTable if row[1] == "tp"] 
            templateDefs =  [{"templateName":rawTable[ind][2],
                    "zones":rawTable[ind][3],
                    "uniqueName":"{}".format(rawTable[ind][4])} 
                    for ind in templateIndices]

            #logging.debug("{} deletions".format(len(deleteDefs)))
            
            
            #--- Changes
            changeIndices = [rawTable.index(row) for row in rawTable if row[1] == "ch"] 
            changeDefs = [{"class":rawTable[ind][2],
                    "objName":rawTable[ind][3],
                    "attr":rawTable[ind][4],
                    "newVal":rawTable[ind][5],
                    } 
                    for ind in changeIndices]
            
            #logging.debug("{} changes".format(len(changeDefs)))
            
              
            variants[variantName] = {
                                     "flags" : flagDefs,
                                     "deletes" : deleteDefs,
                                     "templates" : templateDefs,
                                     "changes" : changeDefs,
                                     "source" : sourcePath,
                                     "description" : description,
                                     
                                     }
    print()
    for var in variants:
        thisVar = variants[var]
        logging.debug("      *** {:>5} - {:<50} *** ".format("Variant",var))
        logging.debug("{:>20} : {:<50}".format("templates",len(thisVar["templates"])))
        logging.debug("{:>20} : {:<50}".format("flags",len(thisVar["flags"])))
        logging.debug("{:>20} : {:<50}".format("deletes",len(thisVar["deletes"])))
        logging.debug("{:>20} : {:<50}".format("changes",len(thisVar["changes"])))
        logging.debug("{:>20} : {:<50}".format("description",thisVar["description"]))
        logging.debug("{:>20} : {:<50}".format("source",thisVar["source"]))
        print()
    logging.debug("Loaded {} variants from {}".format(len(variants),inputExcelPath))

    return variants




def check_out_dir():
    """Delete old files if desired
    """
    if count_files(PATH_IDF_OUT) or count_dirs(PATH_IDF_OUT):
        if simpleYesNo("Delete from {} \n {} files \n {} directories".format(PATH_IDF_OUT,count_files(PATH_IDF_OUT),
                                                                            count_dirs(PATH_IDF_OUT),
                                                                            )):
            erase_dir_contents(PATH_IDF_OUT)
        else:
            pass




def get_templates(templatePath, filter_regex_string = ".", flgExact = True):
    """Given a path, return a list of matching IDF files (by regex), and load into IDF objects
    """ 
        # Used to be a method on IDF class
    # This is just a filter for file names now...

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


def idf_assembly(variants,templates,IDD_xml,proj_def):
    
    """
    A wrapper utility script to automate everthing
    """
    
    

    
    #--- Iterate variant_def definitions
    for key in variants:
        
        variant_def = variants[key]
        #pprint(variant_def)
        print()
        logging.debug("Processing variant {} {}".format(variant_def['description'],variant_def['source']))
        #pprint(variant_def)

        
        #--- Create a new IDF from the variant_def
        this_IDF = IDF.from_IDF_file(variant_def['source'])
        
        
        #--- Process flags
        #pprint(variant_def['flags'])
        for flag_def in variant_def['flags']:
            flag_function = flag_def['flag']
            flag_argument = flag_def['argument']
            #print(flag_function,flag_argument)
            #--- Flag cleanOut found
            if flag_function == 'cleanOut':
                if 0:
                    class_count_table = util_xml.get_table_object_count(this_IDF)
                    print_table(class_count_table)
                
                this_IDF = util_xml.clean_out_object(this_IDF, kept_classes_dict[flag_argument])
                
                if 0:
                    class_count_table = util_xml.get_table_object_count(this_IDF)
                    print_table(class_count_table)
                
        #--- Process deletions
        #raise
        for deletion in variant_def['deletes']:
            util_xml.delete_classes_from_excel(this_IDF, IDD_xml, deletion)
        
        #--- Apply unique templates
        loaded_templates_names = [this_template.ID for this_template in templates]
        indexed_templates = list(zip(loaded_templates_names,templates))
        templates_dict = dict(indexed_templates)
        #print(templates_dict)
        
        #raise
        for template_def in variant_def['templates']:
            template_name = template_def['templateName']
            template_def['uniqueName']
            
            assert(template_def['templateName'] in templates_dict), "{} not in templates".format(template_def['templateName'])
            
            util_xml.apply_template(this_IDF, 
                                    IDD_xml, 
                                    templates_dict[template_name], 
                                    zoneNames = template_def['zones'], 
                                    templateName = template_name, 
                                    uniqueName = None)

        
        #--- Apply changes
        #pprint(variant_def)
        for change in variant_def['changes']:
            util_xml.apply_change(this_IDF,IDD_xml,change)
            
        #--- Convert
        this_IDF.convert_XML_to_IDF()
        
        #--- Save to variant
        variants[key]['IDF_obj'] = this_IDF
        
        
        #--- Write to file
        output_filename = variant_def['description'] + ".idf"
        out_path = os.path.abspath(proj_def['idf_output_dir']+output_filename)
        variants[key]['out_path']  = out_path
        
        #--- Cleanup
        variants[key].pop('changes')
        variants[key].pop('deletes')
        variants[key].pop('flags')
        variants[key].pop('templates')
        
        #print(out_path)
        #raise
        #this_IDF.write_IDF(out_path)
        #raise
    
    return variants

def write_group_files(variants,proj_def):
    #===============================================================================
    # Write the group file
    #===============================================================================
        
    groupName = "Group name"
    
    outputTargetAbsDir = os.path.normpath(proj_def['idf_output_dir'])
    
    groupFilePath = outputTargetAbsDir + r"\\" + groupName + ".epg"
    
            
    csvout = csv.writer(open(groupFilePath, 'w'))
    
    #for variant_def in variants:
        
    #pprint(variants)
    #pprint(proj_def)
    #raise
    for key in variants:
        variant_def = variants[key]
        pprint(variant_def)
        variant_def['IDF_obj'].write_IDF(variant_def['out_path'])
        thisRow = [variant_def['out_path'],proj_def['weather_file_path'],variant_def['out_path'],"1"]
        csvout.writerow(thisRow)
        
    logging.info("Wrote the {0} variants to the group simulation file at: {1}".format(len(variants),groupFilePath))     
 





def process_project_OLD(excel_project_dir, path_idf_base):
    raise

    #print
    check_out_dir()
    #excelProjectPath =
    
    thisProjDefRoot = FREELANCE_DIR
    
    # Path to IDD XML (In the SVN repo, relies on current working dir)
    thisProjRoot = split_up_path(os.getcwd())[:4]
    path_IDD_XML = thisProjRoot + ["SampleIDFs"] + ["Energy+idd.xml"]
    path_IDD_XML = os.path.join(*path_IDD_XML)


    # Weather file
    pathWeather = thisProjDefRoot + r"\\081_CentralTowerFinal\WEA\SVK_Bratislava.118160_IWEC.epw"

    logging.info("\t {:>20} : {:<50}".format("Project file",excel_project_dir))
    logging.info("\t {:>20} : {:<50}".format("IDD file",path_IDD_XML))
    logging.info("\t {:>20} : {:<50}".format("Weather file",pathWeather))
    logging.info("\t {:>20} : {:<50}".format("Output directory",PATH_IDF_OUT))

    IDDobj = idf.IDF.fromXmlFile(path_IDD_XML)
    variants = idf.loadVariants(excel_project_dir,path_idf_base)

    # All variants
    varList = [var for var in variants.iteritems() if 1]

    # Just one for testing?
    #varList = [var for var in variants.iteritems() if var[0] == "VAV only"]
    #varList = [var for var in variants.iteritems() if var[0] == "TESTING"]

    for varName,variant in varList:
        if re.search(r"^SKIP",varName,re.VERBOSE):
            continue

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
        # Flags
        #=======================================================================
        for line in variant["flags"]:

            if line["flag"] == "cleanOut":
                keptDictName = line["argument"]
                idf.cleanOutObject(IDFobj,idf.keptClassesDict[keptDictName])

        #=======================================================================
        # CLEAN OUT
        #=======================================================================
        #idf.cleanOutObject(IDFobj,idf.kept_classes_dict['onlyGeometry'])
        #idf.applyDefaultConstNames(IDFobj, IDDobj)


        for delete in variant["deletes"]:
            idf.deleteClassesFromExcel(IDFobj, IDDobj, delete)


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
            idf.applyChange(IDFobj, IDDobj, change)

        #IDFobj = vrv.addZoneHVAC(IDFobj)
        #idf.printXML(IDFobj.XML)
        #vrv.addTerminals(IDFobj)
        #vrv.getZoneHVAC(IDFobj)
        #printXML(IDFobj.XML)

        #newPathIdfOutput = getNewerFileRevName(pathIdfOutput)
        fullInputPath= PATH_IDF_OUT + "\\" + varName + ".idf"
        fullOutputPath = PATH_IDF_OUT + "\\" + varName
        IDFobj.writeIdf(fullInputPath)
        groupName = "00myGroup"
        groupFilePath = PATH_IDF_OUT + r"\\" + groupName + ".epg"
        csvout = csv.writer(open(groupFilePath, 'ab'))

        thisRow = [fullInputPath,pathWeather,fullOutputPath,"1"]
        csvout.writerow(thisRow)

    #logging.info("Wrote the {0} variants to the group simulation file at: {1}".format(len(variantsList),groupFilePath))

def idf_assembly_OLD(projectFile,weather_file_path,output_dir_path,groupName):
    raise
    """
    A wrapper utility script to automate everything
    """
    
    templatesList = IDF.loadTemplates(IDF_TEMPLATE_PATH)
    raise
    groupFilePath = output_dir_path + r"\\" + groupName + ".epg"
    
    #===============================================================================
    # Load variants
    #===============================================================================
    variantFileAbsPath = os.path.abspath(projectFile)
    outputTargetAbsDir = os.path.normpath(output_dir_path)
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
        thisIDF.cleanOutObject(kept_classes_dict['onlyGeometry'])
        
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
        thisRow = [variant.targetDirAbsPath,weather_file_path,variant.targetDirAbsPath,"1"]
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
    templates = get_templates(IDF_TEMPLATE_PATH)
    
    #--- Get excel project variant definitions
    excel_project_dir = get_latest_rev(proj['path_proj_excel'], r"^Input Data", ext_pat = "xlsx")
    variants = load_variants(excel_project_dir,proj['idf_base'])
    
    #--- Load IDD
    
    IDD_xml = IDF.from_XML_file(IDD_XML_FILE_PATH)
    #IDD_xml = IDF.from_IDD_file(IDD_FILE_PATH)
    
    #--- Assemble variants
    proj['weather_file']
    variants = idf_assembly(variants,templates,IDD_xml,proj)
    #pprint(variants)
    
    #--- Write group
    #PATH_WEATHER_FILE
    proj['weather_file_path'] = proj['idf_output_dir']+"Weather.epw"
    copy_file(proj['path_weather_file'], proj['weather_file_path'])
    write_group_files(variants,proj)
    
    

if __name__ == "__main__":
    print(ABSOLUTE_LOGGING_PATH)
    logging.config.fileConfig(ABSOLUTE_LOGGING_PATH)
    
    myLogger = logging.getLogger()
    myLogger.setLevel("DEBUG")
    
    logging.info("Started IDF test script")
    
    process_project()

    logging.info("Finished IDF test script")                
    