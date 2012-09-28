#!/usr/bin/python

import os,sys


# readconf to read the conf file

def readconf(conf_file):
        '''readconf() -> this function reads a configuration file with hardcoded path depending on user calling
           the function  and  returns a dictionary'''

        conf_file_name1 = conf_file

        confdict = {}
        #reading sitedef file
        if (os.access(conf_file_name1,os.F_OK) == True):
                file = open(conf_file_name1,"r")
                conflines = file.readlines()
                for line in conflines:
                        if (line.startswith('#') or line.startswith('\n')):continue
                        key = line.split('=')[0]
                        value = line.split('=')[1]
                        if len(line.split('=')) > 2:
                           for i in range(2,len(line.split('='))-1):
                               value = value + '=' + line.split('=')[i]
                           value = value + '='
                        confdict[key.strip()] = value.strip()
        else:
                print "FILE " + conf_file_name1 + " NOT FOUND! Exiting...\n"
                sys.exit(1)
        file.close()
        return confdict;

