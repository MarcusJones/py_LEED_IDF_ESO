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

from config import *

import logging.config
import unittest
import csv
from utility_inspect import get_self, get_parent, list_object
from UtilityXML import createTextEl, printXML
import re
from lxml import etree

#===============================================================================
# Code
#===============================================================================

def addRow(table, row, lastIndex):
    thisRow = etree.SubElement(table, "tr")
    for text in row[1:lastIndex + 1]:
        thisCell = etree.SubElement(thisRow, "td", align = "right")
        
        #if not text:
        #    text = " "
        text = unicode(text)
        thisCell.text = text
        
        
        #createTextEl(thisRow,"td", text)
        #newTable.append()

def parse(csvPath):
    """Return the something to the something."""
    #soup = bs.BeautifulSoup()
    root = etree.Element("html")

    with open(csvPath, 'rb') as csvfile:
        reader = csv.reader(csvfile, delimiter=',')
        flgTable = False
        for row in reader:
            if re.search("^[-]+$",row[0]):
                #print "HR",
                #continue
                #root.append(soup.new_tag("b", href="http://www.example.com"))
                thisObjectXML = etree.SubElement(root, "hr")
                #createTextEl(root,"b", )
            elif row[0]:
                if row[1]:
                    #print "Name - val",
                    newPara = etree.SubElement(root, "p")
                    newPara.text = row[0] + " "
                    createTextEl(newPara,"b", row[1])                    
                else:
                    #print "Name",
                    newPara = etree.SubElement(root, "p")
                    createTextEl(newPara,"b", row[0])
            elif not row[0]:
                
                items = [row.index(item) for item in row if item]
                
                if items and not flgTable:
                    lastItem = items[-1]
                    flgTable = True
                    #print "Start",
                    
                    newTable = etree.SubElement(root, "table", 
                                                border="1", 
                                                cellpadding="4", 
                                                cellspacing="0")
                    
                    thisTable = list()
                    thisTable.append(row)
                    
                    

                    addRow(newTable, row, lastItem)
#
#                    thisRow = etree.SubElement(newTable, "tr")
#                    for item in row[1:lastItem]:
#                        createTextEl(thisRow,"td", item)
#                        #newTable.append()
                    
                elif items and flgTable:
                    flgTable = True
                    #print "Cont",
                    thisTable.append(row)
                    
                    addRow(newTable, row, lastItem)
                    

                elif not items and flgTable:
                    flgTable = False
                    #print "Table found:", len(thisTable)
                    #for tabRow in thisTable:
                    #    print tabRow
                        
                    #print "Blank", 
                    
                elif not items and not flgTable:
                    pass
                    #print "Blank", 
            else:
                pass
                #print "Blank",
            print ', '.join(row)
        return root
#===============================================================================
# Unit testing
#===============================================================================

class allTests(unittest.TestCase):
    
    def setUp(self):
        print "**** TEST {} ****".format(get_self())
        
        
    def test010_SimpleCreation(self):
        print "**** TEST {} ****".format(get_self())
        
        csvPath = r"C:\Projects\081_CentralTowerFinal2\Reporting\5Zone_TransformerMeter.csv"
        
        csvPath =  PYTHON_ECLIPSE + r"\PyIDF\data\SimplerTable.csv"
        csvPath = r"C:\Projects\081_CentralTowerFinal2\Reporting\Baseline VAVTable.csv"
        
        root = parse(csvPath)
        
        #printXML(root)
        
        outPath = r"C:\Projects\test\test.html"

        fOut = open(outPath, 'w')

        resultString = etree.tostring(root, pretty_print=True)

        fOut.write(resultString)
        fOut.close

#===============================================================================
# Main
#===============================================================================
if __name__ == "__main__":
    print ABSOLUTE_LOGGING_PATH
    logging.config.fileConfig(ABSOLUTE_LOGGING_PATH)
    
    
    myLogger = logging.getLogger()
    myLogger.setLevel("DEBUG")

    logging.debug("Started _main".format())
    
    #print FREELANCE_DIR
    
    unittest.main()
        
    logging.debug("Finished _main".format())
    