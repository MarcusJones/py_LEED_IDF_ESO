import logging.config
from config import *
from UtilityPathsAndDirs import filterFilesDir,getLatestRev
from xls_preprocess.preprocess import process_project
    
if __name__ == "__main__":
    # Load the logging configuration
    logging.config.fileConfig(ABSOLUTE_LOGGING_PATH)
    
    logging.info("Started IDF test script")
    
    excelProjectDir = getLatestRev(r"C:\Projects\Twin_Riga_ENE5\Project\\", r"^Input Data ENE 5", ext_pat = "xlsx")

    #excelProjectDir = getLatestRev(r"C:\Projects2\Twin_Riga_ENE5\Project\\", r"^Input Data ENE 5", ext_pat = "xlsx")
    
    process_project(excelProjectDir)
    
    logging.info("Finished IDF test script")                
    