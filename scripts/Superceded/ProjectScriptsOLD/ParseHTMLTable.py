'''
Created on Aug 7, 2011

@author: UserXP
'''

"""
Note - 
"""


from BeautifulSoup import BeautifulSoup
import re
import os
import re
import cProfile
from win32com.client import Dispatch
import logging.config
import sys
import psutil

class VariantTables(object):
    def __init__(self,htmlFilePath):
        # Parse the HTML        

        logging.info("New HTML variant table object started")
        infile = open(htmlFilePath, 'r')
        # Load it all into soup
        self.soup = BeautifulSoup(infile)
        
        infile.close()
        
        logging.info("Soup loaded, length is {0} ".format(len(self.soup)))
        
        self.title = self.getTitle()
        self.area = self.getArea()
        self.totalSiteEnergy = self.getTotalSiteEnergy()
        self.endUseBreakdown = self.getBreakDown()
        self.unmetCooling = self.getUnmetCooling()
        self.avgWallU = self.getAvgWallU()
        self.avgWindowU = self.getAvgWindowU()
        
        
        # NEW
        self.heatGainComponents = self.getHeatGainComponents()

        self.outdoorAirSummary = self.getOutdoorAirSummary()
        
        # Try to free up some memory
        self.soup = 0 
        
        logging.info("This HTML variant table has been initialized")
        
        
#        print [
#        self.title,
#        self.area,
#        self.totalSiteEnergy,
#        self.endUseBreakdown,
#        self.unmetCooling,
#        self.avgWallU,
#        self.avgWindowU,            
#               ]
 
 
    def getTitle(self):
        #===============================================================================
        # Variant title
        #===============================================================================
        title = self.soup.find(text='Building: ').findNext('b')
        #title2 = self.soup.extract(text='Building: ').findNext('b')
        #print type(title)
        #print type(title.extract())
        #print BeautifulSoup.extract(self.soup)
        #print title
        #print title.__repr__()
        #print repr(title)
        #print str(title)
        #title = BeautifulSoup.extract(title)

        #finalValue = title.find(text=True).extract()
        #finalValue = repr(finalValue)
        #print finalValue
        #print type(repr(finalValue))
        #raise
        
        thisItem = title.find(text=True)
        thisItem = repr(thisItem)
        return thisItem
    
    def getArea(self):
        #===============================================================================
        # Building area
        #===============================================================================
        # Select the table
        thisTable = self.soup.find(text='Building Area').findNext('table')
        # Select the td, and choose the next one
        thisTd = thisTable.find(text='Total Building Area').findNext('td')
        #print float(thisTd.find(text=True))
        
        thisItem = float(thisTd.find(text=True))
        thisItem = repr(thisItem)
        return thisItem

    def getTotalSiteEnergy(self):
        #===============================================================================
        # Total site energy
        #===============================================================================
        thisTable = self.soup.find(text='Site and Source Energy').findNext('table')
        # Select the td, and choose the next one
        thisTd = thisTable.find(text='Total Site Energy').findNext('td')
        #print float(thisTd.find(text=True))
        thisItem = float(thisTd.find(text=True))
        thisItem = repr(thisItem)
        return thisItem


    def getUnmetCooling(self):
        #===============================================================================
        # Total site energy
        #===============================================================================
        thisTd = self.soup.find(text='Time Set Point Not Met During Occupied Cooling').findNext('td')
        # Select the td, and choose the next one
        #thisTd = thisTable.find(text='Total Site Energy').findNext('td')
        #print float(thisTd.find(text=True))
        thisItem = float(thisTd.find(text=True))
        thisItem = repr(thisItem)
        return thisItem
      
    def getHeatGainComponents(self):
        thisTable = self.soup.find(text='Annual Building Sensible Heat Gain Components').findNext('table')
        
        # Select all tr
        allRows = thisTable.findAll('tr')
        components = list()
        
        # Only want last row
        lastRow =  allRows[-1]
        colNodes = lastRow.findAll('td')
        
        # Skip first
        for thisTd in colNodes[1:]:
            thisItem = float(thisTd.find(text=True))
            thisItem = repr(thisItem)
            #print node
            components.append(float(thisItem))
            
        return components
                
    def getBreakDown(self):
        #===============================================================================
        # Energy use breakdown
        #===============================================================================
        thisTable = self.soup.find(text='End Uses').findNext('table')
        # Select all tr
        allRows = thisTable.findAll('tr')
        endUseBreakDown = list()
        # The last row is the sum anyways, don't need it
        for row in allRows[1:-2]:
            colNodes = row.findAll('td')
            # Match all number of form 00.000, at end of string
            colNumberNodes = row.findAll('td',text=re.compile(r"\d+\.?\d*$"))
            #print colNumberNodes
            #print row.findNext('td')
            #print colNumberNodes
            newColumnValue = 0
            # The columns, in order are; Elec, Gas, Other, Cool, Heat, Water
            # We don't need last one, water:
            #print "Len", len(colNumberNodes)
            for node in colNumberNodes[0:-1]:      
                #print "value", float(node)
                newColumnValue += float(node)
                #print node.find(text=True)
                pass
            #print "Sum:", newColumnValue
            endUseBreakDown.append(newColumnValue)
            
        return endUseBreakDown
        #print thisTd.find(text=True)

        #r"[+-]?((\d+(\.\d*)?)|\.\d+)([eE][+-]?[0-9]+)?"

        #def coreFunction():

    def getOutdoorAirSummary(self):
        #===============================================================================
        # Energy use breakdown
        #===============================================================================
        thisTable = self.soup.find(text='Average Outdoor Air During Occupied Hours').findNext('table')
        # Select all tr
        allRows = thisTable.findAll('tr')
        oaData = list()
        # Skip header
        nominalOccSum = 0
        zoneVolumeSum = 0
        totalVentRate = 0
        totalInfRate = 0
        totalSimpleInfRate = 0
        
        for row in allRows[1:]:
            colNodes = row.findAll('td')
            colNodesData = colNodes[1:] # Skip the zone name

            thisOccupancy = float(colNodesData[1].find(text=True))
            thisZoneVol = float(colNodesData[2].find(text=True))
            thisZoneVentAch = float(colNodesData[3].find(text=True))
            thisZoneInfAch = float(colNodesData[4].find(text=True))
            thisZoneSimpleVenAch = float(colNodesData[5].find(text=True))
            
            thisZoneVentRate_m3_hr = thisZoneVol * thisZoneVentAch
            thisZoneInfRate_m3_hr = thisZoneVol * thisZoneInfAch
            thisZoneSimpleVenRate_m3_hr = thisZoneVol * thisZoneSimpleVenAch

            

            nominalOccSum += thisOccupancy
            zoneVolumeSum += thisZoneVol
            totalVentRate += thisZoneVentRate_m3_hr
            totalInfRate += thisZoneInfRate_m3_hr
            totalSimpleInfRate += thisZoneSimpleVenRate_m3_hr   

        oaSummary = [
                     nominalOccSum,
                     zoneVolumeSum,
                     totalVentRate,
                     totalInfRate,
                     totalSimpleInfRate,] 
            
        return oaSummary

    def getAvgWallU(self):
        #===============================================================================
        # Energy use breakdown
        #===============================================================================
        thisTable = self.soup.find(text='Opaque Exterior').findNext('table')
        # Select all tr
        allRows = thisTable.findAll('tr')
        #print allRows
        #endUseBreakDown = list()
        areaSum = 0
        UAprodSum = 0
        for row in allRows[1:-1]:
            colNodes = row.findAll('td')
            #print "All the columns:",colNodes
            # Match all number of form 00.000, at beginning and end of string
            colNumberNodes = row.findAll('td',text=re.compile(r"^\s*\d+\.\d*$"))
            #print "Here are the numbers:", colNumberNodes 
            #colsWithNumbers = row.findAll('td',text=re.compile(r"\d+\.?\d*$"))
            #print "Here are the numbers:", colsWithNumbers
            #print row.findNext('td')
            #print colNumberNodes
            #newColumnValue = 0
            # The columns, in order are; Reflectance     U-Factor with Film [W/m2-K]     U-Factor no Film [W/m2-K]     Gross Area [m2]     Azimuth [deg]     Tilt [deg]
            UfacWithFilm = float(colNumberNodes[1])
            grossArea = float(colNumberNodes[2])
            UAproduct = UfacWithFilm*grossArea
            UAprodSum += UAproduct
            areaSum += grossArea
            #print breakHereError
            
            # We don't need last one, water:
            #print "Len", len(colNumberNodes)
            #for node in colNumberNodes[0:-1]:      
#                #print "value", float(node)
#                print node
#                newColumnValue += float(node)
#                #print node.find(text=True)
#                pass
#            #print "Sum:", newColumnValue
#            endUseBreakDown.append(newColumnValue)
#        print 
        averageU = UAprodSum/areaSum
        
        logging.info("Calculated average wall U-value {0} ".format(averageU))

        return averageU
        #print thisTd.find(text=True)

    def getAvgWindowU(self):
        #===============================================================================
        # Energy use breakdown
        #===============================================================================
        thisTable = self.soup.find(text='Exterior Fenestration').findNext('table')
        # Select all tr
        allRows = thisTable.findAll('tr')

        areaSum = 0
        UAprodSum = 0
        for row in allRows[1:-4]:
            colNodes = row.findAll('td')

            colNumberNodes = row.findAll('td',text=re.compile(r"^\s*\d+\.\d*$"))

            UfacWithFilm = float(colNumberNodes[5])
            grossArea = float(colNumberNodes[0])
            UAproduct = UfacWithFilm*grossArea
            UAprodSum += UAproduct
            areaSum += grossArea

        averageU = UAprodSum/areaSum
        logging.info("Calculated average window U-value {0} ".format(averageU))
        return averageU


def locateHTMLfiles(projectDir):
    #===========================================================================
    # Locate the HTML table files
    #===========================================================================
    
    logging.info("Looking in {0}".format(projectDir))
    
    tableFileNames = list()
    for name in os.listdir(projectDir):
        if re.search(".html$",name):
            #print name
            logging.info("Found {0}".format(name))
            tableFileNames.append(name)
            
    logging.info("Found {0} HTML".format(len(tableFileNames)))
    return tableFileNames 
   
def parseFilesIntoVariants(projectDir, tableFileNames):
    #===========================================================================
    # Parse the files, store into objects
    #===========================================================================
    variantsDataList = list()
    

    for thisTableFileName in tableFileNames:
        htmlTableFilePath = os.path.join(projectDir, thisTableFileName)
        logging.info("*** Loading HTML file: {0}".format(htmlTableFilePath))
        thisVariant = VariantTables(htmlTableFilePath)
        
        #logging.info("This variant: {}".format(vars(thisVariant)))
        # Output the object
#        for attr, value in thisVariant.__dict__.iteritems():
#            print attr, value
#            #print thisVariant.attr
#            getTypeString = "type(thisVariant." + attr + ")"
#            print eval(getTypeString)
        
        

        variantsDataList.append(thisVariant)

        #thisVariant = None
        
        logging.info("*** Finished with HTML file: {0}".format(thisVariant.title))


        #print "Python: {}".format(os.getpid("python"))
        #p = psutil.Process(os.getpid())
        #p = psutil.Process(os.getpid())
        #print p.get_memory_info()
        
        for proc in psutil.process_iter():
            if proc.name == "python.exe":
                #print proc
                #print type(proc)
                #print dir(proc)
                #print type(proc.get_memory_info())
                #print dir(proc.get_memory_info())
                #print "MB of memory for python-{}: {}".format(proc.pid, proc.get_memory_info().rss / 1000 / 1000)
                #print "The python process:".format(type(proc))
                logging.info("MB allocation for python-{}: {}".format(proc.pid, proc.get_memory_info().rss / 1000 / 1000))

        
        #print psutil.Process(the_pid_you_want)

    
    logging.info("*** Parsed {0} HTML files".format(len(variantsDataList)))


     
    return variantsDataList

def permuteEstidama(variantsDataList):
    #===========================================================================
    # Permute the results for Estidama
    #===========================================================================
    for variant in variantsDataList:
        thisData = list()
        thisData.append(variant.endUseBreakdown[1])
        thisData.append(variant.endUseBreakdown[8])
        thisData.append(variant.endUseBreakdown[0])
        thisData.append(variant.endUseBreakdown[7])
        thisData.append(variant.endUseBreakdown[6])
        thisData.append(0) # Car park fans
        thisData.append(variant.endUseBreakdown[2])
        thisData.append(variant.endUseBreakdown[5])               
        thisData.append(variant.endUseBreakdown[11])     
        thisData.append(variant.endUseBreakdown[4])
        thisData.append(0)
        thisData.append(0)
        variant.endUseBreakdown = thisData
        
        """
        LEED
        0Heating
        1Cooling
        2Interior Lighting
        3Exterior Lighting
        4Interior Equipment
        5Exterior Equipment
        6Fans
        7Pumps
        8Heat Rejection
        9Humidification
        10Heat Recovery
        11Water Systems
        12Refrigeration
        13Generators
        
        ESTI
        0Space Cooling
        1Heat Rejection
        2Space Heating
        3Pumps
        4Fans - Interior
        5Fans - Car park
        6Interior Lighting
        7Exterior Lighting
        8Service Water Heating
        9Receptacle/Process Equipment
        10Data Centre Equipment
        11Elevators and Escalators
        """
        
    logging.info("Permuted lists in {0} HTML".format(variantsDataList))

    return variantsDataList
        

def writeExcel(excelTemplate,savePath, variantsDataList):
    #===========================================================================
    # Open the Excel file   
    #===========================================================================
    
    excel           = Dispatch('Excel.Application')
    excel.Visible   = False  
    book = excel.Workbooks.Open(excelTemplate)
    logging.info("Opened {0}".format(excelTemplate))
    # Select first sheet
    sheet = book.Worksheets(1)
    
    logging.info("Opened template: {0} ".format(excelTemplate))

    
    #===========================================================================
    # Write the data
    #===========================================================================
    col = startColumn = 3
    row = startRow = 1
    for variant in variantsDataList:
        row = startRow
        logging.info("Writing {0} to column {1}".format(variant.title,col))
        sheet.Cells(row,col).Value = variant.title
        row += 1
        sheet.Cells(row,col).Value = variant.area
        row += 1
        sheet.Cells(row,col).Value = variant.totalSiteEnergy
        row += 4
        for energyUse in variant.endUseBreakdown:
            sheet.Cells(row,col).Value = energyUse
            row += 1
        row += 4
        sheet.Cells(row,col).Value = variant.unmetCooling
        row += 4
        sheet.Cells(row,col).Value = variant.avgWallU  
        row += 1
        sheet.Cells(row,col).Value = variant.avgWindowU
        
        row += 6
        for component in variant.heatGainComponents:
            sheet.Cells(row,col).Value = component
            row += 1
            
        row += 6
        for value in variant.outdoorAirSummary:
            sheet.Cells(row,col).Value = value
            row += 1


        
        
        # The last item - Carriage return to next column!
        col += 1
        
    logging.info("Wrote data: {0} ".format(excelTemplate))

    #===========================================================================
    # Save and close
    #===========================================================================
    #The remove doesn't work for me, but I simply save as different file...
    #I just put the lines for you to see what I had found...
    #if os.path.exists(file_name):
    #os.remove(file_name)
    
    logging.info("Writing data to: {0} ".format(savePath))

    book.SaveAs(savePath)#change name
    
    logging.info("Success, wrote data to: {0} ".format(savePath))

    #The end...
    book.Saved = 0 #p.248 Using VBA 5
    book.Close(SaveChanges=0) #to avoid prompt
    excel.Quit()
    #excel.Visible = 0
    #must make Visible=0 before del self.excelapp or EXCEL.EXE remains in memory.
     
    del excel
    
 
def simpleOpenExcel(excelPath):
    #===========================================================================
    # Open the Excel file   
    #===========================================================================
    
    excel           = Dispatch('Excel.Application')
    excel.Visible   = True  
    book = excel.Workbooks.Open(excelPath)
    logging.info("Opened {0}".format(excelPath))
    # Select first sheet
    sheet = book.Worksheets(1)
    
    logging.info("Opened template: {0} ".format(excelPath))
    
    #excel.Application.Quit()

#    #The end...
#    book.Saved = 0 #p.248 Using VBA 5
#    book.Close(SaveChanges=0) #to avoid prompt
#    excel.Quit()
#    #excel.Visible = 0
#    #must make Visible=0 before del self.excelapp or EXCEL.EXE remains in memory.
#     
#    del excel
#    
 

def _parseTheMediaCentre():
    projectDir = r"D:\Freelancing\MediaSim\Sizing runs"
    
    theFiles = locateHTMLfiles(projectDir)
    
    # Locate the HTML table files
    #self.myScrollCtrl.SetValue("Processing {0} HTML files".format(len(self.myHTMLfiles)))
    
    #selectedItems = self.myListBox.GetSelections()
    
    #mySubsetHTMLFiles = [self.myHTMLfiles[i] for i in selectedItems]
    
    logging.info("Processing {0} HTML files".format(len(theFiles)))
    
    #print mySubsetHTMLFiles
    myVariants = parseFilesIntoVariants(projectDir, theFiles)
    
    #self.SetStatusText("Permuting {0} HTML files".format(mySubsetHTMLFiles))
    
    #self.myVariants = ParseHTMLTable.permuteEstidama(self.myVariants)
    
    writeExcel(self.templatePath, self.xlTargetPath, self.myVariants )
    


def _test1():
    projectDir = r"D:\Freelancing\Simulation"
    
    theFiles = locateHTMLfiles(projectDir)
    
    #print theFiles
    
    # Locate the HTML table files
    #self.myScrollCtrl.SetValue("Processing {0} HTML files".format(len(self.myHTMLfiles)))
    
    #selectedItems = self.myListBox.GetSelections()
    
    #mySubsetHTMLFiles = [self.myHTMLfiles[i] for i in selectedItems]
    
    logging.info("Processing {0} HTML files".format(len(theFiles)))
    
    #print mySubsetHTMLFiles
    myVariants = parseFilesIntoVariants(projectDir, theFiles)
    
    #self.SetStatusText("Permuting {0} HTML files".format(mySubsetHTMLFiles))
    
    #self.myVariants = ParseHTMLTable.permuteEstidama(self.myVariants)
    
    #writeExcel(self.templatePath, self.xlTargetPath, self.myVariants )

def _parse1file():
    
    TEMPLATEPATH = os.path.normpath(r"D:\Freelancing\01_AutomatedReporting\postProcessTemplateEstidama r02.xlsx")
    
    #XLTARGETPATH= os.path.normpath(r"D:\Freelancing\Simulation\\00VariantsPostProcess.xlsx")
    thisProjDir = r"D:\Freelancing\Simulation\\"
    #thisProjDir = r"D:\Freelancing\Simulation\FirstHalf\\"
    PROJECTDIR = os.path.normpath(thisProjDir)
    XLTARGETPATH =  os.path.normpath(thisProjDir + r"\\00VariantsPostProcess.xlsx")

    
    tableFileNames = r"Proposed 1.00 1.00 COP 5.idfTable.html"
    tableFileNames = [tableFileNames]
    
    dataList = parseFilesIntoVariants(thisProjDir, tableFileNames)
    
    dataListP = permuteEstidama(dataList)

    writeExcel(TEMPLATEPATH, XLTARGETPATH, dataListP )

    
    writeExcel 

if __name__ == "__main__":
    
    logging.config.fileConfig('..\\LoggingConfig\\loggingNofile.conf')
    
    logging.info("Start")
    
    _parse1file()

    
    
    logging.info("Finished")
