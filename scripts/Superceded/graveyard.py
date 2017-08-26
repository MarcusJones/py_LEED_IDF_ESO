
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
 