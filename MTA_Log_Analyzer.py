# DOCSTART
# This is Log Analyzing script for the MTA.
# The script will look for the "familiar" error codes in the given log file and
# process and output a error log lines and
# possible solution for the errors.

# Script name   : MTA_LOG_ANALYZER.py
# Written by    :
# Reviewed by   :
# Written Date  :
#
# Input Variables
#  LOGFILE_NAME = < Name of the logfile to be processed with absolute path >

# Output Variables

# Assumptions :
# 1. All the Required Utilities where installed and working
# 2. Default script related directories are created and scripts are placed
# 3. Syntax check is done for the script.

# DOCEND

# ########IMPORTS SECTION########

import re
import hashlib
import optparse
import logging
import sys
import random
import string

class MultiRegex(object):
    flags = re.DOTALL
    regexes = ()

    def __init__(self):
        '''
        compile a disjunction of regexes, in order
        '''
        self._regex = re.compile("|".join(self.regexes), self.flags)

    def sub(self, s):
        return self._regex.sub(self._sub, s)

    def _sub(self, mo):
        '''
        determine which partial regex matched, and
        dispatch on self accordingly.
        '''
        for k,v in mo.groupdict().iteritems():
            if v:
                sub = getattr(self, k)
                if callable(sub):
                    return sub(mo)
                return sub
        raise AttributeError, \
             'nothing captured, matching sub-regex could not be identified'



class MTA_Errors():
    

    bounce_error = ()
    deferred_error = ()
    inputfile = '/home/dselvam/zimbra_support_git/Zimbra-Support-Scripts/error_collection.txt'
    pattern1 = 'status=bounced'
    pattern2 = 'status=deferred'
    
    error_to_catch = getattr(__builtins__,'FileNotFoundError', IOError)
    try:
        f = open(inputfile)
    except error_to_catch:
        raise
        print('!')

    def Postfix_Errors():
        patterns = ["status=bounced", "status=deferred"]
        regex = re.compile(pattern1)
        #for line in enumerate(open(inputfile)):
        for line in open('/home/dselvam/zimbra_support_git/Zimbra-Support-Scripts/error_collection.txt', 'r'):
            print(line)
            my_match = regex.findall(line, re.MULTILINE)
            print(my_match)
            for match in my_match:
                print(match)
            #for match in re.finditer(pattern1, line):
             #   print("Finding pattern  %s" % log_file)
            #    print("Test" % match)
                #return 'Postfix Deferred Error'



def main():

    desc = (r"Finding a possible MTA errors and"
            r"printing the log lines and "
            r"possible solutions for the errors... ")

    parser = optparse.OptionParser(
        usage='Usage: %prog -i <input file> -o <output file> <options>',
        description=desc,
        version='%prog version 1.0')

    parser.add_option(
        '-i',
        '--inputfile',
        help='File to find/analyze errors.',
        dest='input_file',
        action='store',
        metavar='/home/dselvam/zimbra_support_git/Zimbra-Support-Scripts/error_collection.txt')

    parser.add_option(
        '-o',
        '--outputfile',
        help='File to store the output.',
        dest='output_file',
        action='store',
        metavar='/home/dselvam/zimbra_support_git/Zimbra-Support-Scripts/zimbra_solutions.txt')

    parser.add_option(
        '-l',
        '--logfile',
        help='Log file storing script operations.',
        dest='log_file',
        action='store',
        metavar='/home/dselvam/zimbra_support_git/Zimbra-Support-Scripts/MTA_Log_Parser_Script.log',
        default='MTA_Log_Parser_Script.log')

    parser.add_option(
        '-v',
        '--verbose',
        help=(r"Log verbosity.."),
        dest='log_level',
        action='store_true',
        default=False)

    (opts, args) = parser.parse_args()

    if not opts.input_file:
        sys.exit("Error: Specify an input file")
    if not opts.output_file:
        sys.exit("Error: Specify an output file")

    if opts.log_level:
        log_level = 10
    else:
        log_level = 20

    log_file = opts.log_file
    logging.basicConfig(
        level=log_level,
        filename=log_file,
        format='%(asctime)s %(levelname)s %(message)s')
    print("Starting script. Logging at %s" % log_file)
    
    logging.info('Input file is %s' % opts.input_file)
    logging.debug('Output file is %s' % opts.output_file)

    with open(opts.output_file, 'w') as new_file:
        with open(opts.input_file) as old_file:
            for line in old_file:
                # logging.debug('Modifying %s' % line)
                new_line = "test \n"
                #new_line = MTA_Errors().match
                # logging.debug('Modified to %s' % new_line )
                new_file.write(new_line)


    logging.info('Completed Finding Errors %s' % opts.input_file)
    print("Script Completed ")


if __name__ == '__main__':
    main()
