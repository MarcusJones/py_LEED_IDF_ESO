'''
Created on Apr 1, 2011

@author: UserXP
'''
import re
from lxml import etree

print "Starting"

# Define input and output full file paths
fIn = open('..\\Test OSM files\\OSM in.osm', 'r')
fOut = open('..\\XML Output\\Test IDF.xml', 'w')


# Calls the readlines method of object which returns a list object of lines
lines = fIn.readlines()

patObject = """
    ^      # beginning of string
    \w+    # 1 or more alphanumeric chars
    [\w:]*  # Any number of colons and alphanumerics
    ,        # Comma
    $        # End of the line 
    """

patValue = """
    ^      # beginning of string
    \s+    # some spaces
    .+    # 1 or more of anything
    ,        # Comma
    """

patClosing = """
    ^      # beginning of string
    \s+    # some spaces
    .+    # 1 or more of anything
    ;        # Semi-colon
    """
    
xmlVer = "0.1"

currentXML = etree.Element("EnergyPlus_XML", XML_version=xmlVer)
commentXML = etree.Comment("XML Schema for EnergyPlus version 6 'IDF' files and OpenStudio version 0.3.0 'OSM' files")
currentXML.append(commentXML)
commentXML = etree.Comment("Schema created April. 2011 by Marcus Jones")
currentXML.append(commentXML)

lineIndex = 0
zoneNameIndex = 0

# Loop over each line
while (lineIndex < len(lines)) :
    
    # Clean up the line
    thisLine = lines[lineIndex].rstrip()
    
    # Found object start
    if re.search(patObject, thisLine,re.VERBOSE):
        # Start an Object
        thisObjectXML = etree.SubElement(currentXML, "OBJECT")
        # An object always has a name
        thisNameXML = etree.SubElement(thisObjectXML, "NAME")
        
        objectName = re.split(',', thisLine,re.VERBOSE)[0]
        #print objectName
        thisNameXML.text = objectName
    
    # Found object attribute
    elif re.search(patValue, thisLine,re.VERBOSE):
        # Start an attribute
        thisAttrXML = etree.SubElement(thisObjectXML, "ATTR")
        
        # Read the attribute
        value,comment = re.split(r",", thisLine,re.VERBOSE)
        value = value.strip()
        comment = comment.strip()
        
        # Found a comment
        if re.search(r"!", comment):
            comment = re.split(r"!", comment,re.VERBOSE)[1]
            comment = comment.strip()
            
        # Add this to the element
        thisAttrXML.text = value

        thisAttrXML.set("Comment", comment)
        
        # Additional tags
        #thisAttrXML.set("Units", "NA")
        
        #print value, comment
        
    # Found a closing semicolon
    elif re.search(patClosing, thisLine,re.VERBOSE):
        # Start an attribute
        thisAttrXML = etree.SubElement(thisObjectXML, "ATTR")
        
        value,comment = re.split(r";", thisLine,re.VERBOSE)
        value = value.strip()
        comment = comment.strip()
        
        if re.search(r"!", comment):
            comment = re.split(r"!", comment,re.VERBOSE)[1]
            comment = comment.strip()
            
        # Add this to the element
        thisAttrXML.text = value

        thisAttrXML.set("Comment", comment)
        #thisAttrXML.set("Units", "NA")
        
        #print value, comment
 
    # Found an empty line or a comment
    else:
        pass

    lineIndex += 1

fIn.close()

print "Finished"

resultXML = (etree.tostring(currentXML, pretty_print=True))

#print resultXML
fOut.write(resultXML )
fOut.close