# -*- coding: utf-8 -*-
"""
Created on Thu Jun 18 13:34:37 2020

@author: books
"""

from os import makedirs, path
from re import compile
from shutil import copyfileobj, make_archive
from zipfile import ZipFile
from pathlib import Path
from tempfile import TemporaryDirectory
import click
import cli

NotionZip = Path(fileopenbox(filetypes = ['*.zip']))


# Load zip file
notionsData = ZipFile(NotionZip, 'r')

NotionPathRaw = []
ObsidianPathRaw = []
NotionPaths = []
ObsidianPaths = []



# Generate a list of file paths for all zip content
[NotionPathRaw.append(line.rstrip()) for line in notionsData.namelist()]



# Clean paths for Obsidian destination
regexUID = compile("\s+\w{32}")

for line in NotionPathRaw:
    ObsidianPathRaw.append(regexUID.sub("", line))


### PATHS IN PROPER OS FORM BY PATHLIB ###
[NotionPaths.append(Path(line)) for line in NotionPathRaw]
[ObsidianPaths.append(Path(line)) for line in ObsidianPathRaw]



# Get all the relevant indices (folders, .md, .csv, others)
mdIndex, csvIndex, othersIndex, folderIndex, folderTree = N2Omodule.ObsIndex(ObsidianPaths)
 

# Rename the .csv files to .md files for the conversion
for i in csvIndex:
    ObsidianPaths[i] = Path(str(ObsidianPaths[i])[0:-3]+"md")


## Create a temporary directory to work with
unzipt = TemporaryDirectory()
tempPath = Path(unzipt.name)


## Create temp directory paths that match zip directory tree
tempDirectories = []

# Construct complete directory paths (<tempDirecory>/<zipDirectories>)
for d in folderTree:
    tempDirectories.append(tempPath / d)

## Create the temporary directory structure for future archive
for d in tempDirectories:
    makedirs(d, exist_ok=True)






# Process all CSV files
for n in csvIndex:
    
    # Access the original CSV file
    with notionsData.open(NotionPathRaw[n], "r") as csvFile:
         
        # Convert CSV content into Obsidian Internal Links
        mdTitle = N2Omodule.N2Ocsv(csvFile)
    
        ## Make temp destination file path
        newfilepath = tempPath / ObsidianPaths[n]
        
        # Check if file exists, append if true
        if path.exists(newfilepath):
            append_write = 'a' # append if already exists
        else:
            append_write = 'w' # make a new file if not
        
        # Save CSV internal links as new .md file
        with open(newfilepath, append_write) as tempFile:
            [print(line.rstrip().encode("utf-8"), file=tempFile) for line in mdTitle]






# Process all MD files
for n in mdIndex:
    
    # Access the original MD file
    with notionsData.open(NotionPathRaw[n], "r") as mdFile:
        
        # Find and convert Internal Links to Obsidian style
        mdContent = N2Omodule.N2Omd(mdFile)
        
        ## Make temp destination file path
        newfilepath = tempPath / ObsidianPaths[n]
        
        # Check if file exists, append if true
        if path.exists(newfilepath):
            append_write = 'a' # append if already exists
        else:
            append_write = 'w' # make a new file if not
        
        # Save modified content as new .md file
        with open(newfilepath, append_write, encoding='utf-8') as tempFile:
            [print(line.rstrip(), file=tempFile) for line in mdContent]
        



#### Process all attachment files using othersIndex ####
for n in othersIndex:
    
    # Move the file from NotionPathRaw[n] in zip to newfilepath = tempPath / ObsidianPaths[n]
    newfilepath = tempPath / ObsidianPaths[n]
    
    # Manage chance of attachments being corrupt. Save a file listing bad files
    try:
        ## if no issue, copy the file
        with notionsData.open(NotionPathRaw[n]) as zf:
            with open(newfilepath, 'wb') as f:
                copyfileobj(zf, f)
    except:
        ## If there's issue, List bad files in a log file
        with open(tempPath / 'ProblemFiles.md', 'a+', encoding='utf-8') as e:
            if path.getsize(tempPath / 'ProblemFiles.md') == 0:
                print('# List of corrupt files from', NotionZip, file=e)
                print('', file=e)
            print('  !!File Exception!!',ObsidianPaths[n])
            print(NotionPathRaw[n], file=e)
            print('', file=e)





# Save temporary file collection to new zip
make_archive( NotionZip.parent / (NotionZip.name[:-4]+'-ObsidianReady'), 'zip', tempPath)




# Close out!
notionsData.close()
