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
#  -i <inputfile> = <Log file to process>

# Output Variables
# It prints the output data to a text file 

# Assumptions :
# 1. All the Required Utilities where installed and working
# 2. Default script related directories are created and scripts are placed
# 3. Syntax check is done for the script.

# DOCEND

# ########IMPORTS SECTION########
import sys
import re
import time
import getopt
from time import strftime

# Main function consists of primary executable code, main() function is not
# mandatory in Python but it brings order to the program.

def main(argv):
#Initializing the variable to store the file name

    log_file_path = '/home/deeps/git_deeps'
    
# Verifying whether any argument passed to the script.    
    if len(sys.argv) <= 1:
        print('Usage: MTA_Log_Analyzer.py -i <inputfile>')
        exit(1)

# Verifying the arguments and printing help text    
    try:
        opts, args = getopt.getopt(argv,"hi:",["ifile="])
    except getopt.GetoptError:
        print('Usage: MTA_Log_Analyzer.py -i <inputfile>')
        sys.exit(2)
    for opt, arg in opts:
       if opt == '-h':
           print('Usage: MTA_Log_Analyzer.py -i <inputfile>')
           sys.exit()
       elif opt in ("-i", "--ifile"):
           log_file_path = arg
    
    export_file_path = "/home/deeps/git_deeps/Zimbra-Support-Scripts/"
    time_now = str(strftime("%Y-%m-%d %H-%M-%S", time.localtime()))
    file = "ParserOutput" + time_now + ".txt"
    export_file = export_file_path + file
    export_file = export_file.replace(' ', '_')
 
    #regex = '(?:status=[b|d|s]+.*$)'
    regex = '(?:status=[b|d]+.*$)'
    #regex = '(status=[b|d]+.*$)'
 
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
        file.write("=============================================================================\n")
        file.write("                    MTA ERRORS FOUND\n")
        file.write("=============================================================================\n")
        match_list_clean = list(set(match_list))
        for item in range(0, len(match_list_clean)):
            #print(match_list_clean[item])
            file.write(match_list_clean[item] + "\n")
        #file.write("\n" + "Possible Solutions for the above errors could be but not limited to: " + "\n")
        file.write("=============================================================================\n")
        file.write("                    SOLUTIONS\n")
        file.write("=============================================================================\n")

        file.write("\nWe can see Bounced and Deferred errors in the log, below are some suggestions\n\
on how to troubleshoot:" + "\n" + "\n")
        file.write("Bounced: These errors occur usually if the recipient or domain doesn't exist.\n\
Please take a look at these elements." + "\n\n" )
        file.write("Deferred: This would mean the remote server is either not available,\n\
or is not accepting mails currently. In such cases, errors\n\
like \"Service temporarily unavailable\" will be shown. It could also\n\
be a sign of this server being blacklisted due to spamming, and which case\n\
the number of errors would be large. To confirm this, run\n\
'/opt/zimbra/libexec/zmqstat' to take a look at the queue.  " + "\n\n")
        #file.write("Solution 1: " + "\n")
        #file.write("Solution 2: " + "\n")
    file.close()
 
if __name__ == '__main__':
    main(sys.argv[1:])
            
