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
from __future__ import division    
import logging.config
from UtilityInspect import whoami, whosdaddy
from config import *
import idf_xml.IDF as IDF
import html_summary.ParseHTMLTables as htPr
#===============================================================================
# Code
#===============================================================================
raise Exception("Needs update")

def parseSummary():
    projectDir = FREELANCE_DIR + r"\Simulation"
    templatePath = FREELANCE_DIR + r"\01_AutomatedReporting\postProcessTemplateLEED r02.xlsx"
    xlTargetPath = FREELANCE_DIR + r"\Simulation\\" + r"00 results.xlsx"
    
    # Locate the HTML table files
    theFiles = htPr.locateHTMLfiles(projectDir)
    logging.info("Processing {0} HTML files".format(len(theFiles)))
    
    #print mySubsetHTMLFiles
    myVariants = htPr.parseFilesIntoVariants(projectDir, theFiles)
    
    #self.SetStatusText("Permuting {0} HTML files".format(mySubsetHTMLFiles))
    
    #self.myVariants = ParseHTMLTable.permuteEstidama(self.myVariants)
    
    htPr.writeExcel(templatePath, xlTargetPath, myVariants )


#===============================================================================
# Main
#===============================================================================
if __name__ == "__main__":
    print ABSOLUTE_LOGGING_PATH
    logging.config.fileConfig(ABSOLUTE_LOGGING_PATH)
    
    myLogger = logging.getLogger()
    myLogger.setLevel("DEBUG")

    logging.debug("Started _main".format())
    
    parseSummary()
    
    
        
    logging.debug("Finished _main".format())
    