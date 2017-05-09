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
# Standard:
from __future__ import division
from __future__ import print_function

from config import *

import logging.config
import unittest

from utility_inspect import whoami, whosdaddy, listObject
from utility_path import get_current_file_dir
import re
import exergyframes.exergy_frame2 as xrg2

from collections import defaultdict
from numpy import genfromtxt

import datetime
import pandas as pd
import time
pd.set_option('display.width', 500)

from UtilityParse import parserCursor

#from exergyframes import exergy_frame as xrg
import exergyframes.exergy_frame2 as xrg

import utility_path as util_paths

FLG_PRINTLINES = True
FLG_PRINTLINES = False


#===============================================================================
# Code
#===============================================================================
def place_holder(line):
   #print "Token function: {} lines ".format(len(blockLines))
   #print blockLines
   #lineIndex = lineIndex + 1
   print(line)




PRIMARY_TOKENS = {
        re.compile("^Program Version")                                      :   place_holder,
        re.compile("^End of Data Dictionary")                                      :   place_holder,
        re.compile("^End of Data")                                      :   place_holder,
        }

ENVIRONMENT_TOKENS = {
        re.compile("^1,")                                      :   place_holder,
                      }
TIMESTEP_TOKENS = {
        re.compile("^2,")                                      :   place_holder,
        }

COMMENT_TOKENS = {
        re.compile("^!!!")                                      :   place_holder,
            }

token_header = re.compile(r"^Program Version,.+,.+$")
token_endhead = re.compile("^End of Data Dictionary$")
token_enddata =  re.compile("^End of Data$")

def parse_vardef(line):
        #======================================================================
        # Split the comment off of the line
        #======================================================================
        data_comment = re.split("!",line)
        # The first element is always the data
        data = data_comment.pop(0).strip()
        # And get the second element if exists
        if data_comment:
            comment = data_comment.pop(0).strip()
        else:
            comment = None
        assert(not(data_comment), "There should be no more elements in the line other than data and comment after splitting")

        #=======================================================================
        # Skip the first line
        #=======================================================================
        if re.compile("^Program Version").match(data):
            return 0

        #=======================================================================
        # The variable signatures
        #=======================================================================
        # Build up a definition on the dictionary var
        var = dict()
        split_data = re.split(",",data)
        #logging.debug("Line: {} !! {}".format(split_data,comment))


        # First element is variable ID
        var['Variable ID'] = int(split_data.pop(0))
        # Second element is number columns
        var['Number columns'] = int(split_data.pop(0))
        # Third element is the
        var['Category'] = split_data.pop(0)

        #=======================================================================
        # Get units
        #=======================================================================
        if split_data:
            name_units = split_data.pop(0)
            unit_search = re.search('\[(.+?)\]',name_units)

            if unit_search:
                # SRE_Match.group(1) is the matched object without brackets?
                var['Units'] = unit_search.group(1)
                # Replace the unit with nothing and the remainder is the name
                var['Name'] = re.sub('\[(.+?)\]','',name_units)
            # There are no unit brackets found
            else:
                var['Name'] = name_units
                var['Units'] = "Unknown"
        else:
            var['Name'] = "Unknown"
            var['Units'] = "Unknown"
        #=======================================================================
        # Get the timestep
        #=======================================================================
        if comment:
            regex_timestep = re.compile("^(Detailed|TimeStep|Hourly|Daily|Monthly|Runperiod)")
            period = re.search(regex_timestep,comment)
            if period:
                var['Timestep'] = period.group(0)
            else:
                var['Timestep'] = "N/A"
        else:
            var['Timestep'] = "N/A"

        assert(len(var.items()) == 6), "{}".format(var)
        return(var)


def get_headers(header_lines):
    logging.debug("Processing variable definitions in {} lines".format(len(header_lines)))

    data = list()
    var_defs = list()
    for line in header_lines:
        #======================================================================
        # Split the comment off of the line
        #======================================================================
        data_comment = re.split("!",line)
        # The first element is always the data
        data = data_comment.pop(0).strip()
        # And get the second element if exists
        if data_comment:
            comment = data_comment.pop(0).strip()
        else:
            comment = None
        assert(not(data_comment), "There should be no more elements in the line other than data and comment after splitting")

        #=======================================================================
        # Skip the first line
        #=======================================================================
        if re.compile("^Program Version").match(data):
            continue

        #=======================================================================
        # The variable signatures
        #=======================================================================
        # Build up a definition on the dictionary var
        var = dict()
        split_data = re.split(",",data)
        #logging.debug("Line: {} !! {}".format(split_data,comment))


        # First element is variable ID
        var['Variable ID'] = int(split_data.pop(0))
        # Second element is number columns
        var['Number columns'] = int(split_data.pop(0))
        # Third element is the
        var['Category'] = split_data.pop(0)

        #=======================================================================
        # Get units
        #=======================================================================
        if split_data:
            name_units = split_data.pop(0)
            unit_search = re.search('\[(.+?)\]',name_units)

            if unit_search:
                # SRE_Match.group(1) is the matched object without brackets?
                var['Units'] = unit_search.group(1)
                # Replace the unit with nothing and the remainder is the name
                var['Name'] = re.sub('\[(.+?)\]','',name_units)
            # There are no unit brackets found
            else:
                var['Name'] = name_units
                var['Units'] = "Unknown"

        #=======================================================================
        # Get the timestep
        #=======================================================================
        if comment:
            regex_timestep = re.compile("^(Detailed|TimeStep|Hourly|Daily|Monthly|Runperiod)")
            period = re.search(regex_timestep,comment)
            if period:
                var['Timestep'] = period.group(0)
            else:
                var['Timestep'] = "N/A"
        else:
            var['Timestep'] = "N/A"


        var_defs.append(var)



    df = pd.DataFrame.from_records(var_defs)
    # The labels should be on the index
    df = df.T

    # The ID is used for column labels now
    df.columns = df.loc['Variable ID']
    df = df.drop(['Variable ID'])
    logging.debug("Returned {} variable definition rows in data frame".format(len(df)))
    return df

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


def get_hourly_data(lines,hourly_indices):
    line_count = 0
    #lines = eso_file.readlines()
    mark_environment = list()
    mark_timestep = list()
    line_index = 0

    tokenized_lines = list()
    flg_stop = False
    flg_header = True
    environments = list()
    while not flg_stop:
        if line_index >= 1000:
            flg_stop = True

        #for line in lines[:200]:

        line = lines[line_index]

        print("Line: {}",line,end='')
        #tokenized_line = list()

        #=======================================================================
        # Skip the header
        #=======================================================================
        if re.compile("^End of Data Dictionary").match(line):
            flg_header = False
            #print("End header")
            #line_index += 1
            #tokenized_line += ['HEAD']

        if flg_header:
            #tokenized_line += ['HEAD']
            #print("HEAD")
            line_index += 1
            continue

        line = line.strip()
        split_line = re.split(",",line)
        #print(line)
        #print(split_line)

        #=======================================================================
        # Environment
        #=======================================================================
        #1,5,Environment Title[],Latitude[deg],Longitude[deg],Time Zone[],Elevation[m]
        #1,DENVER CENTENNIAL  GOLDEN   N ANN HTG 99% CONDNS DB,  48.20,  17.20,   1.00, 130.00

        if split_line[0] == "1":

            line_index, this_environment = parse_environmentOLD(lines, line_index,hourly_indices)
            environments.append(this_environment)
        else:
            line_index += 1

    environments = dict(environments)
    #print("Done")
    return environments

def get_annual_frame(frames):
    #=======================================================================
    # Get the annual frame
    #=======================================================================
    annual_frame = None
    for frame in frames:
        if frame.n_data_rows == 8760:
            annual_frame = frame
            break
    if not annual_frame:
        raise
    logging.debug("Annual frame selected".format(len(frames)))

def get_biggest_frame(frames):
    biggest=frames[0]
    for frame in frames:
        if len(frame) > len(biggest):
            biggest = frame
    return frame


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



def save_frames(list_frames):
    for frame in list_frames:
        xrg.write_excel_one(annual_hourly, path)


def parse_tstep(tstep_def, eso_file):


    # Looks like this;
    #2,    6,      Day of Simulation[],    Month[], Day of Month[],DST Indicator[1=yes 0=no],Hour[],StartMinute[],EndMinute[],DayType
    #2,            1,                      12,      21,            0,                        1,     0.00,         60.00,      WinterDesignDay


    year = 2014
    id = int(tstep_def.pop(0))
    simday = int(tstep_def.pop(0))
    month = int(tstep_def.pop(0))
    day = int(tstep_def.pop(0))
    dst = int(tstep_def.pop(0))
    hour = int(tstep_def.pop(0))
    start_minute = int(float(tstep_def.pop(0)))
    end_minute = int(float(tstep_def.pop(0)))
    time_step = end_minute - start_minute
    day_type=tstep_def.pop(0)

    timestamp = datetime.datetime(year, month, day, hour-1,start_minute)
    timestamp = pd.Timestamp(timestamp)

    #if
    #if hour == 1:
    #    logging.debug("Parsing day: {}".format(timestamp))
    if day == 1 and hour == 1:
        logging.debug("Parsing month: {}".format(timestamp))

    #print(day,hour)

    line = eso_file.next()
    this_tstep_ids = list()
    this_tstep_vals = list()

    while 1:
        if FLG_PRINTLINES:
            print(line.strip())

        items = line.strip()
        items = line.split(',')
        if re.match(token_enddata, line):
            # Found the end of file
            logging.debug("End of Data found while in tstep".format())
            break
        
        if items[0] == "1":
            # Found the next environment
            logging.debug("Next env found while in tstep".format())
            break
        elif items[0] == "2":
            #logging.debug("Next timestep found".format())
            break
        
        # Cumulative variables, ignore
        elif items[0] == "3":
            break
        elif items[0] == "4":
            break
        elif items[0] == "5":
            break
        
        
        else:
            #print("This line: {}".format(line))
            pass
            
        assert(len(items)==2), "{} \n {}".format(items,line)
        
        
        this_tstep_ids.append(int(items.pop(0)))
        this_tstep_vals.append(float(items.pop(0)))
        #print(items, end='')
        assert(len(items)==0), "{}".format(items)

        line = eso_file.next()

    #logging.debug("Parsing timestep: {}".format(timestamp))
    assert(len(this_tstep_ids) == len(this_tstep_vals))

    #logging.debug("Parsed timestep: {}, {} items".format(timestamp, len(this_tstep_ids)))
    #print(this_tstep_vals)
    #raise
    return eso_file,line, {'timestamp' :timestamp, 'data':dict(zip(this_tstep_ids, this_tstep_vals)) }

def parse_env(env_defition, eso_file):
    """Returns a DataFrame with columns labelled by variable ID, and indexed by timestamp
    """

    env_defition = " - ".join(env_defition)
    env_defition = env_defition.strip()
    logging.debug("Parsing Env: {}".format(env_defition))

    t0 = time.time()


    line = eso_file.next()
    tstep_data_list = list()

    #max_lines = 1000
    cnt = 0
    while 1:
        if FLG_PRINTLINES:
            print(line.strip())

        cnt+=1
        items = line.strip()
        items = line.split(',')

        # Found the end of file
        if re.match(token_enddata, line):
            logging.debug("End of Data found while in environment".format())
            break
        # Found the next environment
        if items[0] == "1":
            logging.debug("Next environment found in environment".format())
            break

        # This is a timestep
        if items[0] == "2":
            #logging.debug("Found timestep: {}".format(items))

            eso_file, line, tstep_data = parse_tstep(items, eso_file)
            tstep_data_list.append(tstep_data)
            continue
        
        # Cumulative variables, ignore
        elif items[0] == "3":
            pass
        elif items[0] == "4":
            pass
        elif items[0] == "5":
            pass
        else:
            pass
        
        line = eso_file.next()

    #===========================================================================
    # Create the dataframe
    #===========================================================================
    data_list = [step['data'] for step in tstep_data_list]
    index = [step['timestamp'] for step in tstep_data_list]
    df = pd.DataFrame(data_list,index = index)

    t1 = time.time()
    total = t1-t0
    logging.debug("Finished processing environment {} seconds".format(total))


    return eso_file,line, df,env_defition

def process_vardefs(variable_defs):

    # Add the variable ID
    var_ids = [vdef['Variable ID'] for vdef in variable_defs]
    #/df = pd.DataFrame(columns = var_ids)

    #names = list()


    val_list = list()
    #raise
    for vdef in variable_defs:
        names = list()
        this_val_list = list()
        for k,v in vdef.iteritems():
            names.append(k)
            this_val_list.append(v)

        val_list.append(this_val_list)


    #===============================================================
    # Reorder the multiindex tuples
    #===============================================================
    id_index = names.index('Variable ID')
    indices = range(len(names))

    new_order = [id_index] +  list(set(indices).difference(set([id_index])))
    names_ordered = [names[idx] for idx in new_order]

    # Transpose
    val_list_T = zip(*val_list)
    # Reorder
    val_list_ordered_T = [val_list_T[idx] for idx in new_order]
    val_list_ordered = zip(*val_list_ordered_T)

    #index_frame = pd.DataFrame(data = val_list_ordered,columns = names_ordered)
    #index_frame = index_frame.set_index('Variable ID')
    #print(index_frame)
    #raise
    #m_index = pd.MultiIndex.from_tuples(tuples=val_list_ordered, names = names_ordered)
    #variable_definitions = index_frame
    column_labels = names_ordered
    #var_
    variable_definitions = [(val_item[0],  val_item) for val_item in val_list_ordered   ]
    variable_definitions = dict(variable_definitions)

    logging.debug("Processed {} variable definitions".format(len(variable_definitions)))

    return variable_definitions, column_labels


def parse2(path_eso, dir_out):

    """Return the something to the something."""
    logging.debug("Parsing {}".format(path_eso))
    #---http://code.ohloh.net/file?fid=DEXGA78swpM6h-Wfg-o0Gquk3fw&cid=Prb6amLFRs4&s=&fp=95353&mp&projSelected=true#L0

    df_dict = dict()

    with open(path_eso, 'r') as eso_file:

        #pth_output = r"d:\parsed.txt"
        #file_output = open(pth_output, 'w')

        logging.debug("Opened {}".format(eso_file))
        #lines = eso_file.readlines()

        cnt = 0
        flg_head = True
        # Get first line
        flg_end = False
        line = eso_file.next()
        variable_defs = list()
        column_labels = None
        df = None
        max_lines = 10000
        while not flg_end and cnt <= max_lines:
            #print(line)
            if cnt == 3000:
                #break
                pass
            label = 'NONE'


            #===================================================================
            # A data entry
            #===================================================================
            if not flg_head:
                original_line = line
                items = line.strip()
                items = line.split(',')
                num_items = len(items)
                line = " : ".join(items)

                #===============================================================
                # Environment found
                #===============================================================
                if items[0] == "1":
                    eso_file,line,df,env_name = parse_env(items, eso_file)
                    new_m_index = list()

                    # Collect the column definitions from our definition list
                    for col in df.iloc[:,:]:
                        new_row = variable_defs[col]
                        new_m_index.append(new_row)

                    # These are used to create the new column index of the final frame
                    new_m_index = pd.MultiIndex.from_tuples(new_m_index, names = column_labels)

                    df.columns = new_m_index


                    df_dict[env_name] = df
                    logging.debug("Added frame to list".format())

                    continue

                #===============================================================
                # End of data
                #===============================================================
                elif re.match(token_enddata, line):
                    logging.debug("End of Data found while in main loop".format())
                    break

                #===============================================================
                # A data entry with no environment is not possible
                #===============================================================
                else:
                    print("Line {} - {}".format(cnt,original_line))
                    raise Exception("A data entry with no environment is not possible".format())
            #===============================================================
            # The first list is skipped
            #===============================================================
            if flg_head and re.match(token_header, line):
                pass
                #label = "Header"

            #===================================================================
            # Done with variable definitions
            #===================================================================
            elif flg_head and re.match(token_endhead, line):
                label = "End header"
                logging.debug("{} different variable definitions loaded".format(len(variable_defs)))
                variable_defs,column_labels = process_vardefs(variable_defs)

                flg_head = False

            #===================================================================
            # A variable definition
            #===================================================================
            else:
                variable_defs.append(parse_vardef(line))

                #label = "Var def"
                #items = line.strip()
                #items = line.split(',')


            #print("{:<5} - {:<10} - {:20}".format(cnt,label,line), end = '', file = file_output)

            if re.match(token_enddata, line):
                logging.debug("End of Data found while in main loop".format())
                break

            line = eso_file.next()

            cnt += 1

        logging.debug("{} frames found".format(len(df_dict)))

        for name,df in df_dict.iteritems():
            original_name = util_paths.split_up_path(path_eso)[-2]
            original_name = original_name.replace('-','')

            path_out = dir_out + name + ".pck"
            df.to_pickle(path_out)
            logging.debug("Saved from file {} into frame {}".format(path_eso,path_out))

            path_out = dir_out + name + '.mat'
            xrg2.write_matlab_tseries(df,path_out,original_name)
            logging.debug("Saved from file {} into frame {}".format(path_eso,path_out))


def parse(path_eso):
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



def load_save(path_input, path_output):
    logging.debug("{} -> {}".format(path_input, path_output))


    t0 = time.time()


    #=======================================================================
    # Parse the eso into a big data frame
    #=======================================================================
    xframe = parse(path_input)
    frames = [frame.return_multi_index() for frame in xframe]
    frame = get_biggest_frame(frames)

    #=======================================================================
    # Extract the hourly data
    #=======================================================================
    mask = xrg.get_mask(frame, 'Timestep', 'Hourly')
    hourly_df = frame.iloc[:,mask]

    #=======================================================================
    # Save as excel and pickle
    #=======================================================================
    xrg.write_pickle_one(hourly_df,path_output)
    #xrg.write_excel_one(hourly_df,self.path_output + r'\eso.xlsx')


    t1 = time.time()
    total = t1-t0
    logging.debug("Finished with {}, {} seconds".format(path_input, total))

def analyze_results(frame,path_out):
    logging.debug("Analyzing a frame {}".format(frame.shape))

#     #=======================================================================
#     # # Reload the frame from pickle
#     #=======================================================================
#     #path_in = paths[0]
#     frame = this_frame

    #=======================================================================
    # The sub-frames will be saved to a dictionary
    #=======================================================================
    out_dfs = dict()

    #=======================================================================
    # *Get people count*
    #=======================================================================
    match = r'^People Occupant Count'
    mask = xrg.get_mask_regex(frame, 'Name', match)
    df_occupancy = xrg.apply_col_mask(frame,mask)
    #df_occupancy = df_occupancy.iloc[:,1:10]
    logging.debug("{} x {} occupancy frame".format(df_occupancy.shape[0],df_occupancy.shape[1]))

    df_occupancy = xrg.sum_rows(df_occupancy, 'Units')
    out_dfs['Occupancy'] = df_occupancy
    out_dfs['Occupancy stats'] = df_occupancy.describe()

    #=======================================================================
    # *Get the zone temperatures*
    #=======================================================================
    match = r'^Zone Mean Air Temperature'
    mask = xrg.get_mask_regex(frame, 'Name', match)
    df_temps = xrg.apply_col_mask(frame,mask)
    logging.debug("{} x {} temperature frame".format(df_temps.shape[0],df_temps.shape[1]))
    out_dfs['Zone temperature'] = df_temps
    out_dfs['Zone temperature stats'] = df_temps.describe()


    #=======================================================================
    # *Get outdoor air*
    #=======================================================================
    match = r'OUTDOOR AIR'
    mask1 = xrg.get_mask_regex(frame, 'Category', match)
    mask2 = xrg.get_mask_regex(frame, 'Units', 'kg/s')
    mask = mask1 & mask2
    df_oa = xrg.apply_col_mask(frame,mask)
    logging.debug("{} x {} outdoor air frame".format(df_oa.shape[0],df_oa.shape[1]))
    df_oa = xrg.sum_rows(df_oa, 'Units')
    out_dfs['Outdoor air'] = df_oa
    out_dfs['Outdoor air stats'] = df_oa.describe()
    #print(df_oa)

    #=======================================================================
    # *Get environment*
    #=======================================================================
    match = r'Environment'
    mask = xrg.get_mask_regex(frame, 'Category', match)
    df_env = xrg.apply_col_mask(frame,mask)
    logging.debug("{} x {} environment frame".format(df_env.shape[0],df_env.shape[1]))
    out_dfs['Environment'] = df_env
    out_dfs['Environment stats'] = df_env.describe()
    #print(df_env)

    xrg.write_dict_to_excel(out_dfs,path_out)

#===============================================================================
# Unit testing
#===============================================================================


def LEED_eso_parse_df(root_dir):
    files = [{'in': root_dir+r'\Proposed.eso',       'out': root_dir+r'\\Proposed.pck'},
             {'in': root_dir+r'\Baseline-G000.eso',  'out': root_dir+r'\\Baseline.pck'},
             ]

    for file_def in files:
        load_save(file_def['in'], file_def['out'])


class allTests(unittest.TestCase):

    def setUp(self):
        print("**** TEST {} ****".format(whoami()))
        #         path_eso = get_current_file_dir(__file__)
        #         path_eso = path_eso + r"\..\.."
        #         path_eso = os.path.abspath(path_eso)
        #         path_eso = path_eso + r"\SampleESO\1ZoneUncontrolled.eso"
        #         path_eso = r'D:\Projects\IDFout\Proposed.eso'
        #         self.path_eso = path_eso
        #
        #         self.path_output = r'D:\Projects\IDFout'
        root_dir = get_current_file_dir(__file__)
        root_dir = root_dir + r"\..\..\SampleESO\LEED hotel run 7 days"
        root_dir = os.path.abspath(root_dir)
        self.root_dir = root_dir
        print(self.root_dir)
        self.pth_big_eso = r"D:\Projects\Proposed.eso"

    @unittest.skipIf(0,'')
    def test010_parse1(self):

        print("**** TEST {} ****".format(whoami()))
        root_dir = self.root_dir
        pth_eso = os.path.join(root_dir,'Proposed.eso')
        pth_eso = self.pth_big_eso

        print(pth_eso)
        parse2(pth_eso)

        #LEED_eso_parse_df(root_dir)

    @unittest.skipIf(1,'')
    def test020_(self):
        pass
        #get_zone_summary_tables()

    @unittest.skipIf(1,'')
    def test030_read_analyze(self):

        print("**** TEST {} ****".format(whoami()))

        root_dir = self.root_dir
        paths = util_paths.get_files_by_name_ext(root_dir, '.', 'pck')
        #print(files)

        for path in paths:
            name = util_paths.split_up_path(path)[-2]
            path_in = path
            path_out = root_dir + name + '.xlsx'
            analyze_results(path_in,path_out)

#===============================================================================
# Main
#===============================================================================
if __name__ == "__main__":
    print(ABSOLUTE_LOGGING_PATH)
    #LOGGING_ROOT_PATH +
    logging.config.fileConfig(ABSOLUTE_LOGGING_PATH)

    #pth_log_file = r""
    #logging.basicConfig(filename=r'D:\parse_log.txt',level=logging.DEBUG)
    myLogger = logging.getLogger()
    myLogger.setLevel("DEBUG")

    logging.debug("Started _main".format())

    #print FREELANCE_DIR

    unittest.main()

    logging.debug("Finished _main".format())
