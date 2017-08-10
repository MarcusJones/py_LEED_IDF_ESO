#===============================================================================
# Title of this Module
# Authors; MJones, Other
# 00 - 2012FEB05 - First commit
# 01 - 2012MAR17 - Update to ...
#===============================================================================

"""
Created on Aug 3, 2011

@author: Marcus Jones

Post process HTML files from energyplus run
"""
#--- SETUP Config
from __future__ import division
import logging.config
#from utility_inspect import whoami, whosdaddy
from config import *

#--- SETUP Standard modules
import re
import os

#--- SETUP 3rd party modules
import pandas as pd
pd.set_option('display.width', 500)


#--- SETUP Custom modules
#from idf_parser import IDF as IDF 
import utility_path as util_paths
#from html_summary.parse_html import run_project,get_zone_summary_tables
import parse_html as p_html
#import parse_eso2 as p_eso


#import html_summary.ParseHTMLTables as htPr
#===============================================================================
# Code
#===============================================================================

def parseSummary():
    project_dir = OUTPUT_DIR

    #project_dir = r"C:\Projects2\081_Central_Admin2\140328 March review submission\\"
    #project_dir = r"D:\Projects\IDFout2\\"

    if 1:
        #===========================================================================
        # Parse HTML LEED files into one excel file
        #===========================================================================
        #loc_post_excel = r"C:\EclipseWorkspace\PyIDF\ExcelTemplates\LEED PostProcess r21.xlsx"
        
        loc_post_excel = os.path.dirname(os.path.realpath(__file__)) + r"\..\ExcelTemplates\LEED PostProcess r22.xlsx"
        loc_post_excel = os.path.abspath( loc_post_excel )
        
        p_html.run_project(project_dir,loc_post_excel)
        
        logging.debug("Finished with HTML tables in {}".format(project_dir))
        
    if 1:
        #===========================================================================
        # Parse the html files to get zone summary pck
        #===========================================================================
        p_html.get_zone_summary_tables(project_dir)

        logging.debug("Finished with zone summary tables in {}".format(project_dir))

    if 1:
        #===========================================================================
        # Parse the proposed and 1 baseline eso file
        #===========================================================================
        files = [
             {'in': project_dir+r'\Proposed.eso',       'out': project_dir+r'\\Proposed '},
                 
             {'in': project_dir+r'\Baseline-G000.eso',  'out': project_dir+r'\\Baseline '},
             ]

        for file_def in files:
            p_eso.parse2(file_def['in'],file_def['out'])

        logging.debug("Parsed eso's in {}".format(project_dir))

    #===========================================================================
    # Reload the pck files into an analysis set
    #===========================================================================
    if 1:
        pck_files=util_paths.get_files_by_name_ext(project_dir, '.', 'pck')

        analysis_set = dict()
        analysis_set['baseline'] = dict()
        analysis_set['proposed'] = dict()
        for pck in pck_files:

            #print(pck)
            #print(util_paths.split_up_path(pck))
            this_name = util_paths.split_up_path(pck, False)[-2]
            if re.search(r'^Baseline.+Zone Summary dataframe$', this_name):
                this_frame = pd.read_pickle(pck)
                logging.debug("Loaded {}".format(pck))
                analysis_set['baseline']['summary'] = this_frame
            elif re.search(r'^Proposed.+Zone Summary dataframe$', this_name):
                this_frame = pd.read_pickle(pck)
                logging.debug("Loaded {}".format(pck))
                analysis_set['proposed']['summary'] = this_frame

            elif re.search(r'^Baseline', this_name):
                #print(this_name)
                this_frame = pd.read_pickle(pck)
                logging.debug("Loaded {}".format(pck))

                analysis_set['baseline']['data'] = this_frame
            elif re.search(r'^Proposed', this_name):
                this_frame = pd.read_pickle(pck)
                logging.debug("Loaded {}".format(pck))
                analysis_set['proposed']['data'] = this_frame
            else:
                raise Exception("Unknown pck file: {}".format(this_name))
#         #print(analysis_set['proposed'])
#         for k,v in analysis_set.iteritems():
#             print(k)
#             print(v)
#         raise
#     
#         for k,v in analysis_set['proposed'].iteritems():
#             print(k)
#             print(v)
#         raise
        p_eso.analyze_results(analysis_set['proposed']['data'],project_dir + "\\Proposed.xlsx")
        p_eso.analyze_results(analysis_set['baseline']['data'],project_dir + "\\Baseline.xlsx")
        #for k,v in analysis_set.iteritems():
        #    print(k)

            #print(v.shape())
    #        for k,v in k.iteritems():
    #            print("\t{}".format(k))

        logging.debug("Analyzed data in {}".format(project_dir))
    logging.debug("Done post-processing {}".format(project_dir))


#===============================================================================
# Main
#===============================================================================
if __name__ == "__main__":
    print(ABSOLUTE_LOGGING_PATH)
    logging.config.fileConfig(ABSOLUTE_LOGGING_PATH)

    myLogger = logging.getLogger()
    myLogger.setLevel("DEBUG")

    logging.debug("Started _main".format())
    #raise
    parseSummary()



    logging.debug("Finished _main".format())
