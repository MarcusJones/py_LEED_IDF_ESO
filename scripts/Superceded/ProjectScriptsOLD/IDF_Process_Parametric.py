'''
Created on Jun 19, 2011

@author: UserXP
'''
from IDF import Variant, IDF

import logging.config

# Load the logging configuration
logging.config.fileConfig('..\\LoggingConfig\\logging.conf')

logging.info("Started Decathlon loads script")

pathXmlOutput = '..\\XML Output\\Test IDF.xml' 

#pathOSMInput = '..\\Input IDF\\Input.idf'
#pathOSMInput = '..\\Input IDF\\SimpleInput.idf'   

#runControlType = "RunControl_10days"
#runControlType = "RunControl_Full"
runControlType = "ParametricRunControl"
#runControlType = "RunControl_Sizing"

#outputType = "Output"
outputType = "TableOutput"

outputFolder = r"C:\Freelance\Simulation"
outputFolder = r"D:\Freelance\Simulation"

# Input files
mainFolder = r"D:\Freelance\Decathlon\Parametric"
InputPath_001 = mainFolder + r"\SKP_OSM\001.osm"
InputPath_011 = mainFolder + r"\SKP_OSM\011.osm"
InputPath_012 = mainFolder + r"\SKP_OSM\012.osm"
InputPath_013 = mainFolder + r"\SKP_OSM\013.osm"
                            
InputPath_101 = mainFolder + r"\SKP_OSM\101.osm"
InputPath_111 = mainFolder + r"\SKP_OSM\111.osm"
InputPath_112 = mainFolder + r"\SKP_OSM\112.osm"
InputPath_113 = mainFolder + r"\SKP_OSM\113.osm"
InputPath_123 = mainFolder + r"\SKP_OSM\123.osm"
InputPath_124 = mainFolder + r"\SKP_OSM\124.osm"

#InputPath_021 = r"C:\Freelance\Decathlon\Parametric\SKP_OSM\021.osm"
#InputPath_022 = r"C:\Freelance\Decathlon\Parametric\SKP_OSM\022.osm"
#InputPath_023 = r"C:\Freelance\Decathlon\Parametric\SKP_OSM\023.osm"
#InputPath_031 = r"C:\Freelance\Decathlon\Parametric\SKP_OSM\031.osm"
#InputPath_032 = r"C:\Freelance\Decathlon\Parametric\SKP_OSM\032.osm"
#InputPath_041 = r"C:\Freelance\Decathlon\Parametric\SKP_OSM\041.osm"
#InputPath_042 = r"C:\Freelance\Decathlon\Parametric\SKP_OSM\042.osm"
#InputPath_051 = r"C:\Freelance\Decathlon\Parametric\SKP_OSM\051.osm"
#InputPath_052 = r"C:\Freelance\Decathlon\Parametric\SKP_OSM\052.osm"

variantList = [
               
            Variant('001 Shoebox Base',InputPath_001,['ConStandard','IdealLoadsAir','DecathlonLoads','MonthlyOutputs']),
            
            Variant('011 Shoebox 25 window',InputPath_011,['ConStandard','IdealLoadsAir','DecathlonLoads','MonthlyOutputs']),
            Variant('012 Shoebox 50 window',InputPath_012,['ConStandard','IdealLoadsAir','DecathlonLoads','MonthlyOutputs']),
            Variant('013 Shoebox 75 window',InputPath_013,['ConStandard','IdealLoadsAir','DecathlonLoads','MonthlyOutputs']),
            
            Variant('101 Cube Base',InputPath_101,['ConStandard','IdealLoadsAir','DecathlonLoads','MonthlyOutputs']),
            
            Variant('111 Cube 25 window',InputPath_111,['ConStandard','IdealLoadsAir','DecathlonLoads','MonthlyOutputs']),
            Variant('112 Cube 50 window',InputPath_112,['ConStandard','IdealLoadsAir','DecathlonLoads','MonthlyOutputs']),
            Variant('113 Cube 75 window',InputPath_113,['ConStandard','IdealLoadsAir','DecathlonLoads','MonthlyOutputs']),
            
            Variant('123 Cube 30 cm Shade',InputPath_123,['ConStandard','IdealLoadsAir','DecathlonLoads','MonthlyOutputs']),
            Variant('124 Cube 70 cm Shade',InputPath_124,['ConStandard','IdealLoadsAir','DecathlonLoads','MonthlyOutputs']),
            
            Variant('031 Shoebox window G value plus',InputPath_012,['CongPlus','IdealLoadsAir','DecathlonLoads','MonthlyOutputs']),
            Variant('032 Shoebox window G value minus',InputPath_012,['CongMinus','IdealLoadsAir','DecathlonLoads','MonthlyOutputs']),
            
            Variant('041 Shoebox U value plus',InputPath_012,['ConUPlus','IdealLoadsAir','DecathlonLoads','MonthlyOutputs']),
            Variant('042 Shoebox U value minus',InputPath_012,['ConUMinus','IdealLoadsAir','DecathlonLoads','MonthlyOutputs']),
            
            Variant('051 Shoebox window U value plus',InputPath_012,['ConWindowUPlus','IdealLoadsAir','DecathlonLoads','MonthlyOutputs']),
            Variant('052 Shoebox window U value minus',InputPath_012,['ConWindowUMinus','IdealLoadsAir','DecathlonLoads','MonthlyOutputs']),
            
            Variant('061 Shoebox Massive Plus',InputPath_012,['ConMassMinus','IdealLoadsAir','DecathlonLoads','MonthlyOutputs']),
            Variant('062 Shoebox Massive Minus',InputPath_012,['ConMassPlus','IdealLoadsAir','DecathlonLoads','MonthlyOutputs']),            
           ]




variantCount = 1
for variant in variantList:
    
    #thisOSM = IDF.fromIdfFile(variant.path)
            
    variant.ID = variantCount
    variant.path =  outputFolder + r"\Variant" + str(variantCount) + ".idf"  
    
    variantCount += 1
    
    # Create a new IDF
    thisIDF = IDF(variant.inputPath,None,None,None,variant.name,variant.path)
    
    # Call the load        
    thisIDF.loadIDF()
    # Call convert
    thisIDF.convertIDFtoXML()
    thisIDF.cleanOutObject()
    
    # Apply standard templates
    thisIDF.applyTemplate(runControlType)
    thisIDF.applyTemplate('SizingParams')
    thisIDF.applyTemplate(outputType)
    thisIDF.selectCommentedAttrAndChange(["^Building$","Name",variant.name])
    
    # Apply unique templates
    for template in variant.templates:
        thisIDF.applyTemplate(template)
            
        # Apply changes
        if variant.changes:
            for change in variant.changes:   
                #print change
                try:  
                    thisIDF.selectCommentedAttrAndChange(change)
                except:
                    raise NameError("{0},{1}".format(change,variant.name))
                    
        
        thisIDF.convertXMLtoIDF()
    
    thisIDF.writeIdf(thisIDF.pathIdfOutput)
        
        #print thisIDF.listZonesWithName('Gym')
        
        #thisIDF.makeUniqueNames()
        
        
logging.info("Finished Decathlon loads script")                
