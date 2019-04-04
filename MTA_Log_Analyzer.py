#!/usr/bin/python3

# DOCSTART
# This is Log Analyzing script for the MTA.
# The script will look for the "familiar" error codes in the given log file and
# process and output a error log lines and
# possible solution for the errors.

# Script name   : MTA_LOG_ANALYZER.py
# Written by    :
# Reviewed by   :
# Written Date  :
# Version       : 1.0

# Input Variables
#  LOGFILE_NAME = <hard coded for now, it can be added as argument>

# Output Variables
# It prints the output data to a text file 

# Assumptions :
# 1. All the Required Utilities where installed and working
# 2. Default script related directories are created and scripts are placed
# 3. Syntax check is done for the script.

# DOCEND

# ########IMPORTS SECTION########

import re
import time
from time import strftime

# Main function consists of primary executable code, main() function is not
# mandatory in Python but it brings order to the program.

def main():
    log_file_path = "/home/deeps/git_deeps/Zimbra-Support-Scripts/error_collection.txt"
    export_file_path = "/home/deeps/git_deeps/Zimbra-Support-Scripts/"
 
    time_now = str(strftime("%Y-%m-%d %H-%M-%S", time.localtime()))
 
    file = "ParserOutput" + time_now + ".txt"
    export_file = export_file_path + file
    export_file = export_file.replace(' ', '_')
 
    #regex = '(?:status=[b|d|s]+.*$)'
    regex = '(?:status=[b|d]+.*$)'
 
    parseData(log_file_path, export_file, regex, read_line=True)
 
# parseData() - function reads the input file line by line and looks for 
# the pattern(aka, regular expression) which is defined in "regex" variable and
# matches the rest of the line and assign the value to the match_text variable.

# Then, we are appending the match_text values to the list which is match_list

# Once the whole file is processed, the match_list output is written to the
# output file.

# As of now the script is limited to find only PostFix errors such as bounced, deferred.
# We are looking forward to add more functions to this script and make as whole module.

def parseData(log_file_path, export_file, regex, read_line=True):
    with open(log_file_path, "r") as file:
        match_list = []
        if read_line == True:
            for line in file:
                for match in re.finditer(regex, line, re.S):
                    match_text = match.group()
                    match_list.append(match_text)
                    #print(match_text)
        else:
            data = file.read()
            for match in re.finditer(regex, data, re.S):
                match_text = match.group();
                match_list.append(match_text)
    file.close()
 
    with open(export_file, "w+") as file:
        file.write("MTA Errors:\n")
        match_list_clean = list(set(match_list))
        for item in xrange(0, len(match_list_clean)):
            #print(match_list_clean[item])
            file.write(match_list_clean[item] + "\n")
        file.write("\n" + "Possible Solutions for the above errors could be but not limited to: " + "\n")
        file.write("Solution 1: " + "\n")
        file.write("Solution 2: " + "\n")
    file.close()
 
if __name__ == '__main__':
    main()
            
