import logging.config
from config import *
from utility_path import filter_files_dir,get_latest_rev
from xls_preprocess.preprocess import process_project

if __name__ == "__main__":
    # Load the logging configuration
    logging.config.fileConfig(ABSOLUTE_LOGGING_PATH)

    logging.info("Started IDF test script")

    proj = PROJ_SHOPPPING
    proj = PROJ_ECOPOINT
    #proj = PROJ_ECOPOINT2

    excel_project_dir = get_latest_rev(proj['path_proj_excel'], r"^Input Data", ext_pat = "xlsx")

    process_project(excel_project_dir, proj['idf_base'] )



    logging.info("Finished IDF test script")


