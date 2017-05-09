'''
Created on Jun 19, 2011

@author: UserXP
'''
from IDF import Variant, IDF

import logging.config

# Load the logging configuration
logging.config.fileConfig('..\\LoggingConfig\\logging.conf')

logging.info("Started Parametric loads script")

pathXmlOutput = '..\\XML Output\\Test IDF.xml' 

#pathOSMInput = '..\\Input IDF\\Input.idf'
#pathOSMInput = '..\\Input IDF\\SimpleInput.idf'   

#runControlType = "RunControl_10days"
runControlType = "RunControl_Full"
#runControlType = "RunControl_Sizing"

#outputType = "Output"
outputType = "TableOutput"

# Input files
#InputPath_ = r"C:\Freelance\Decathlon\Parametric\IDF\Main.idf"

mainFolder = r"C:\Freelance\Decathlon"

InputPath_Andras = mainFolder + r"\01 Andras Vernes\IDF\main.idf"
InputPath_Boeckle = mainFolder + r"\02 Boeckle & Benz\IDF\main.idf"
InputPath_Kraler = mainFolder + r"\03 David Kraler\IDF\main.idf"
InputPath_Buehrle = mainFolder + r"\04 Buehrle Hua\IDF\main.idf"
InputPath_Marlies = mainFolder + r"\05 Marlies Arnhof\IDF\main.idf"


variantList = [
            Variant('01Andras PassivHaus',InputPath_Andras,['IdealLoadsAir','DecathlonLoads','ConstructionSetPassivHaus','MonthlyOutputs']),
            Variant('02Boeckle PassivHaus',InputPath_Boeckle,['IdealLoadsAir','DecathlonLoads','ConstructionSetPassivHaus','MonthlyOutputs']),
            Variant('03Kraler PassivHaus',InputPath_Kraler,['IdealLoadsAir','DecathlonLoads','ConstructionSetPassivHaus','MonthlyOutputs']),
            Variant('04Buerhle PassivHaus',InputPath_Buehrle,['IdealLoadsAir','DecathlonLoads','ConstructionSetPassivHaus','MonthlyOutputs']),
            Variant('05Marlies PassivHaus',InputPath_Marlies,['IdealLoadsAir','DecathlonLoads','ConstructionSetPassivHaus','MonthlyOutputs']),
           ]

            #Variant('01Andras Baseline 4A',InputPath_Andras,['IdealLoadsAir','DecathlonLoads','ConstructionSetBaseline4A','MonthlyOutputs']),
            #Variant('01Andras AndrasSet',InputPath_Andras,['IdealLoadsAir','DecathlonLoads','ConstructionSet01Andras','MonthlyOutputs']),

            #Variant('02Boeckle Baseline 4A',InputPath_Boeckle,['IdealLoadsAir','DecathlonLoads','ConstructionSetBaseline4A','MonthlyOutputs']),
            #Variant('02Boeckle AndrasSet',InputPath_Boeckle,['IdealLoadsAir','DecathlonLoads','ConstructionSet01Andras','MonthlyOutputs']),            

            #Variant('03Kraler Baseline 4A',InputPath_Kraler,['IdealLoadsAir','DecathlonLoads','ConstructionSetBaseline4A','MonthlyOutputs']),
            #Variant('03Kraler AndrasSet',InputPath_Kraler,['IdealLoadsAir','DecathlonLoads','ConstructionSet01Andras','MonthlyOutputs']),

            #Variant('04Buerhle Baseline 4A',InputPath_Kraler,['IdealLoadsAir','DecathlonLoads','ConstructionSetBaseline4A','MonthlyOutputs']),
            #Variant('04Buerhle AndrasSet',InputPath_Kraler,['IdealLoadsAir','DecathlonLoads','ConstructionSet01Andras','MonthlyOutputs']),


variantCount = 1
for variant in variantList:
    
    #thisOSM = IDF.fromIdfFile(variant.path)
            
    variant.ID = variantCount
    variant.path =  "C:\\Freelance\\Simulation\\Variant" + str(variantCount) + ".idf"  
    
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
        
        
logging.info("Finished Parametric loads script")                
