'''
Created on Apr 1, 2011

@author: UserXP
'''
import re

print "Starting"

# Define input and output full file paths
fIn = open('..\\Test OSM files\\OSM in.osm', 'r')
fOut = open('..\\OSM Output\\OSMout.txt', 'w')

# Calls the readlines method of object which returns a list object of lines
lines = fIn.readlines()

lineIndex = 0
zoneNameIndex = 0

# Loop over each line
while (lineIndex < len(lines)) :
    
    # Found a Zone object
    # A sample Zone object looks like:
    #    Zone,
    #      Zone {2dd358c6-cfbf-4c9e-9288-0fb821562ad2},  ! Name
    #      -0,
    #      -8.7886328617592611,
    #      -2.7799448931827579,
    #      0;
    #
    
    # Search the entire file for the "Zone," string     
    if re.search('Zone,', lines[lineIndex]):
        zoneNameIndex += 1
        
        # Break off the name inside the curly braces
        zoneName = re.split("[\{\}]", lines[lineIndex+1])[1]
        print "Zone name: ", zoneName, "is replaced with ", zoneNameIndex
        newLineArray = []
        
        # Now replace all instances with new name, using a temporary array
        for line in lines: 
            newLineArray += [re.sub(zoneName,str(zoneNameIndex), line)]
        # Reassign the array
        lines = newLineArray
        
    # Write this new 
    fOut.write(lines[lineIndex])

    lineIndex += 1

fIn.close()

print "Finished"