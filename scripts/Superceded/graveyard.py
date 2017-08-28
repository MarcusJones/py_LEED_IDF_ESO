
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
 
 
 
 
def parse_timestepOLD(lines):

    #===========================================================================
    # The first line holds the timestamp
    #===========================================================================
    # Looks like this;
    #2,    6,      Day of Simulation[],    Month[], Day of Month[],DST Indicator[1=yes 0=no],Hour[],StartMinute[],EndMinute[],DayType
    #2,            1,                      12,      21,            0,                        1,     0.00,         60.00,      WinterDesignDay

    # Get it
    first_line = lines.pop(0)
    first_line = re.split(",",first_line)

    # Break it down
    id = first_line.pop(0)
    year = 2014
    day_of_simulation = int(first_line.pop(0))
    month = int(first_line.pop(0))
    day = int(first_line.pop(0))
    dst = int(first_line.pop(0))
    hour = int(first_line.pop(0))
    start_minute = int(float(first_line.pop(0)))
    end_minute = int(float(first_line.pop(0)))
    time_step = end_minute - start_minute
    day_type=first_line.pop(0)

    timestamp = datetime.datetime(year, month, day, hour-1,start_minute)

    #===========================================================================
    # Process the values
    #===========================================================================
    # Break the lines down
    values = list()
    for line in lines:
        split_line = re.split(",",line)
        var_id = int(split_line.pop(0))

        value = split_line
        if len(split_line) == 1:
            try:
                value = float(value[0])
            except:
                print(value)
                raise
        elif len(split_line) > 1:
            pass
        # A dictionary containing the id and the value as pairs
        values.append((var_id, value))


    table_row = dict((('Timestamp',timestamp), ('step', time_step), ('Day type',day_type)))
    table_row = {'Timestamp':timestamp}
    table_row.update(dict(values))
    #logging.debug("TIMESTEP {}".format(table_row))
    return table_row

def parse_environmentOLD(lines,line_index,hourly_indices):
    this_line = lines[line_index]
    split_line = re.split(",",this_line)
    id = split_line.pop(0)
    location = split_line.pop(0)
    logging.debug("Found environment {}".format(location))

    #environ_table = defaultdict(list)
    time_rows = list()
    line_index += 1

    flg_end_environment = False
    while not flg_end_environment:
        this_line = lines[line_index]
        split_line = re.split(",",this_line)
        #logging.debug("{}".format(split_line))
        if split_line[0] == "1":
            id = split_line.pop(0)
            location = split_line.pop(0)
            logging.debug("Found next environment, break".format())
            flg_end_environment = True
            line_index -= 1

        elif re.compile(r"^ Number of Records Written=").match(this_line):
            logging.debug("Found EOF, break".format())
            flg_end_environment = True
            line_index -= 1

        elif re.compile(r"^End of Data").match(this_line):
            flg_end_environment = True
            logging.debug("Found EOF, break".format())
            line_index -= 1

        elif split_line[0] == "2":
            # Timestep
            line_index, table_row = parse_timestepOLD(lines, line_index,hourly_indices)
            time_rows.append(table_row)
            continue
        else:
            print(this_line)
            raise
        line_index += 1

    df = pd.DataFrame.from_records(time_rows, index='Timestamp')
    #print(df.head())

    return line_index - 1,  (location, df)



def old():

    #=======================================================================
    # Get the hourly values only
    #=======================================================================
    mask_hourly = (definition_frame.loc["Timestep",:]  == "Hourly")
    df_hourly = definition_frame

    annual_hourly = xrg.ExergyFrame(annual_frame.data_frame.loc[:,mask_hourly],
                                    annual_frame.header_frame.loc[:,mask_hourly],
                                    'Main',)

    annual_hourly = annual_hourly.return_multi_index()
    print(annual_hourly)

    path = r'D:\Projects\Temp\testing.xlsx'



def parse(path_eso):
    # OLD
    """Return the something to the something."""
    logging.debug("Parsing {}".format(path_eso))

    with open(path_eso, 'r') as eso_file:
        logging.debug("Opened {}".format(eso_file))
        lines = eso_file.readlines()


    #=======================================================================
    # Break off  variable definitions
    #=======================================================================
    mainLoop = parserCursor(lines,PRIMARY_TOKENS, COMMENT_TOKENS)
    blocks = list()
    for block in mainLoop:
        blocks.append(block['lines'])
        logging.debug("Processed {} blocks".format(len(blocks)))


    definition_lines = blocks.pop(0)
    logging.debug("{} definition lines".format(len(definition_lines)))


    # Definitions are in a dataframe
    definition_frame = get_headers(definition_lines)
    #print(definition_frame)

    #=======================================================================
    # The data left over
    #=======================================================================
    data = blocks.pop(0)
    data = data[1:-1] # Skip the first line
    logging.debug("{} data lines".format(len(data)))



    #=======================================================================
    # Get the environments
    #=======================================================================
    logging.debug("Parsing environments".format(len(definition_lines)))
    data_loop = parserCursor(data,ENVIRONMENT_TOKENS, COMMENT_TOKENS)
    environments =list()
    for block in data_loop:
        environments.append(block['lines'])
    logging.debug("{} environments".format(len(environments)))

    #=======================================================================
    # Get time step blocks in each environment
    #=======================================================================
    logging.debug("Parsing environments".format(len(definition_lines)))
    expanded_environments = list()
    for env in environments:
        logging.debug("Processing environment {} , {} lines".format(env[0].strip(),len(env)))
        this_environment = env[0].strip()
        time_loop = parserCursor(env,TIMESTEP_TOKENS, COMMENT_TOKENS)
        timesteps = list()
        for block in time_loop:
            #print(block['function'])
            #print(len(block['lines']))
            #environments.append(block['lines'])
            timesteps.append(block['lines'])

        logging.debug("Found {} time steps in {} ".format(len(timesteps),env[0].strip()))

        env_dict = {'name':this_environment, 'tsteps':timesteps}

        expanded_environments.append(env_dict)

    #=======================================================================
    # Process timesteps, create xframes
    #=======================================================================
    frames = list()
    for env in expanded_environments:
        logging.debug("Getting all data from {}".format(env['name']))
        rows = list()
        # Step over all timesteps

        for tstep in env['tsteps']:
            this_row = parse_timestepOLD(tstep)
            rows.append(this_row)

        df = pd.DataFrame.from_records(rows,index = "Timestamp")
        logging.debug("Returned {} rows in data frame".format(len(df)))

        df,definition_frame = xrg.drop_missing_cols(df,definition_frame)
        this_xframe = xrg.ExergyFrame(df,definition_frame,env['name'],)
        frames.append(this_xframe)

    logging.debug("{} xframes created".format(len(frames)))
    return frames


