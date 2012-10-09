#!/usr/bin/python


# This is the submission wrapper script for g09:
# Needs a configuration file as input. see gaus_wrapper.conf as an example


import os, sys, time

saveout = sys.stdout
fsock = open('gauss_wrapper.log', 'w')   # no longer used, but kept as empty file, grid job std output goes to std.out file
#sys.stdout = fsock

conf_file = sys.argv[1]

import readconf

#initialisation of variables, taken from the conf file

confdict = readconf.readconf(conf_file)

################################################################################
##  Now it is time to download the G09 EXECUTABLE from the grid using an lfn  ##
################################################################################

#the location can be parametrized
cmd = "lcg-cp -v --vo " + confdict['VO'] + " --connect-timeout " + confdict['CONNECT_TIMEOUT'] + "  --sendreceive-timeout " + confdict['SENDRECEIVE_TIMEOUT'] + " --bdii-timeout " + confdict['BDII_TIMEOUT'] + " --srm-timeout " + confdict['SRM_TIMEOUT'] + "   lfn:" + confdict['GRID_LFN_PATH'] + "/G09.tgz file:./G09.tgz"

print "luaching cmd = " + cmd
fsock.flush()
status = os.system(cmd)
print status
fsock.flush()

################################################################################
##       Now it is time to untar the G09 EXECUTABLE just downloaded           ##
################################################################################

cmd = "tar -xzf G09.tgz"
print "untarring g09, cmd = " + cmd
fsock.flush()
status = os.system(cmd)
print status
fsock.flush()


################################################################################
##        Now we create the needed directory structure ./Gaussian             ##
################################################################################


cmd = "mkdir " + confdict['GAUSS_CHK_PATH']
print "creating chk dir, cmd = " + cmd
fsock.flush()
status = os.system(cmd)
print status
fsock.flush()


################################################################################
##  Now it is time to download a previously created CHK file to read geom at  ##
#             restart. Condition on a variable read fromconfile               ##
################################################################################

if confdict['USE_GRID_CHK'] == 'True':

   cmd = "lcg-cp -v --vo " + confdict['VO'] + " --connect-timeout " + confdict['CONNECT_TIMEOUT'] + " --sendreceive-timeout " + confdict['SENDRECEIVE_TIMEOUT'] + " --bdii-timeout " + confdict['BDII_TIMEOUT'] + " --srm-timeout " + confdict['SRM_TIMEOUT'] + "   " + "lfn:" + confdict['GRID_LFN_PATH'] + '/' + confdict['GRID_CHK_FILE'] + " file:" + confdict['GAUSS_CHK_PATH'] + '/' + confdict['GAUSS_CHK_FILE']
   print "luaching cmd = " + cmd
   fsock.flush()
   status = os.system(cmd)
   print status
   fsock.flush()

################################################################################
##        Now we create the needed directory structure ./gauss_scratch        ##
################################################################################


cmd = "mkdir " + confdict['GAUSS_SCRATCH_PATH']
print "creating scratch dir, cmd = " + cmd
fsock.flush()
status = os.system(cmd)
print status
fsock.flush()


################################################################################
##  Now it is time to download a previously created INT, RWF, D2E files       ##
#            for restart. Condition on a variable read fromconfile            ##
################################################################################

if confdict['USE_GRID_INT'] == 'True':

   cmd = "lcg-cp -v --vo " + confdict['VO'] + " --connect-timeout " + confdict['CONNECT_TIMEOUT'] + " --sendreceive-timeout " + confdict['SENDRECEIVE_TIMEOUT'] + " --bdii-timeout " + confdict['BDII_TIMEOUT'] + " --srm-timeout " + confdict['SRM_TIMEOUT'] + "   " + "lfn:" + confdict['GRID_LFN_PATH'] + '/' + confdict['GRID_INT_FILE'] + " file:" + confdict['GAUSS_SCRATCH_PATH'] + '/' + confdict['GAUSS_INT_FILE']
   print "luaching cmd = " + cmd
   fsock.flush()
   status = os.system(cmd)
   print status
   fsock.flush()

if confdict['USE_GRID_RWF'] == 'True':

   cmd = "lcg-cp -v --vo " + confdict['VO'] + " --connect-timeout " + confdict['CONNECT_TIMEOUT'] + " --sendreceive-timeout " + confdict['SENDRECEIVE_TIMEOUT'] + " --bdii-timeout " + confdict['BDII_TIMEOUT'] + " --srm-timeout " + confdict['SRM_TIMEOUT'] + "   " + "lfn:" + confdict['GRID_LFN_PATH'] + '/' + confdict['GRID_RWF_FILE'] + " file:" + confdict['GAUSS_SCRATCH_PATH'] + '/' + confdict['GAUSS_RWF_FILE']
   print "luaching cmd = " + cmd
   fsock.flush()
   status = os.system(cmd)
   print status
   fsock.flush()

if confdict['USE_GRID_D2E'] == 'True':

   cmd = "lcg-cp -v --vo " + confdict['VO'] + " --connect-timeout " + confdict['CONNECT_TIMEOUT'] + " --sendreceive-timeout " + confdict['SENDRECEIVE_TIMEOUT'] + " --bdii-timeout " + confdict['BDII_TIMEOUT'] + " --srm-timeout " + confdict['SRM_TIMEOUT'] + "   " + "lfn:" + confdict['GRID_LFN_PATH'] + '/' + confdict['GRID_D2E_FILE'] + " file:" + confdict['GAUSS_SCRATCH_PATH'] + '/' + confdict['GAUSS_D2E_FILE']
   print "luaching cmd = " + cmd
   fsock.flush()
   status = os.system(cmd)
   print status
   fsock.flush()


################################################################################
##        Now we start di uploader subprocess that will upload periodically   ##
##                the restart files, the chk and those in scratch dirs        ##
##  to minimize concurrency on those file they are first copied in .BAK and   ##
##                           the .BAK is uploaded.                            ##
##      The pid is kept to kill the process when G09 has completed            ##
##          popen seems no to work for grid job, so a os.system is used       ##
##        need to investigate the use of the multiprocessing python module    ##
##            everything is conditioned by a variable in the conf file        ##
##                                                                            ##
##                                                                            ##
##                Note that only one SE can be given to the uploader,         ##
##                          this have to be improved                          ##
##                     This was improved, replica SE used                     ##
################################################################################

## moving here the uploader - no need to run a separate process

#pid = None

#saveout = sys.stdout
fsock_up = open('upload_threaded.log', 'a')

DeletePrevious = confdict['DELETE_PREVIOUS_UPLOADED']

timestr = time.strftime("%a, %d %b %Y %H:%M:%S ", time.localtime())

fsock_up.write("Upload chk utility started on: " + timestr + '\n')
fsock_up.flush()

import upload_threaded


if confdict['USE_PERIODIC_UPLOADER'] == "True" :

   # Create new threads
   upload_chk = upload_threaded.Uploader(fsock_up, "upload_chk", confdict['GAUSS_CHK_FILE'], confdict['GAUSS_CHK_PATH'], confdict['GRID_LFN_PATH'], int(confdict['CHK_UPLOAD_FREQ']), confdict['OUTPUT_SE'], confdict['REPLICA_SE'], confdict['VO'], confdict['CONNECT_TIMEOUT'], confdict['SENDRECEIVE_TIMEOUT'], confdict['BDII_TIMEOUT'], confdict['SRM_TIMEOUT'],DeletePrevious)

   upload_int = upload_threaded.Uploader(fsock_up, "upload_int", confdict['GAUSS_INT_FILE'], confdict['GAUSS_SCRATCH_PATH'], confdict['GRID_LFN_PATH'], int(confdict['INT_UPLOAD_FREQ']), confdict['OUTPUT_SE'], confdict['REPLICA_SE'], confdict['VO'], confdict['CONNECT_TIMEOUT'], confdict['SENDRECEIVE_TIMEOUT'], confdict['BDII_TIMEOUT'], confdict['SRM_TIMEOUT'],DeletePrevious)

   upload_rwf = upload_threaded.Uploader(fsock_up, "upload_rwf", confdict['GAUSS_RWF_FILE'], confdict['GAUSS_SCRATCH_PATH'], confdict['GRID_LFN_PATH'], int(confdict['RWF_UPLOAD_FREQ']), confdict['OUTPUT_SE'], confdict['REPLICA_SE'], confdict['VO'], confdict['CONNECT_TIMEOUT'], confdict['SENDRECEIVE_TIMEOUT'], confdict['BDII_TIMEOUT'], confdict['SRM_TIMEOUT'],DeletePrevious)

   upload_d2e = upload_threaded.Uploader(fsock_up, "upload_d2e", confdict['GAUSS_D2E_FILE'], confdict['GAUSS_SCRATCH_PATH'], confdict['GRID_LFN_PATH'], int(confdict['D2E_UPLOAD_FREQ']), confdict['OUTPUT_SE'], confdict['REPLICA_SE'], confdict['VO'], confdict['CONNECT_TIMEOUT'], confdict['SENDRECEIVE_TIMEOUT'], confdict['BDII_TIMEOUT'], confdict['SRM_TIMEOUT'],DeletePrevious)

   upload_log = upload_threaded.Uploader(fsock_up,"upload_log", confdict['GAUSS_LOG_FILE'], "./" , confdict['GRID_LFN_PATH'], int(confdict['D2E_UPLOAD_FREQ']), confdict['OUTPUT_SE'], confdict['REPLICA_SE'], confdict['VO'], confdict['CONNECT_TIMEOUT'], confdict['SENDRECEIVE_TIMEOUT'], confdict['BDII_TIMEOUT'], confdict['SRM_TIMEOUT'],DeletePrevious)


   # threads list
   th_list = [upload_chk, upload_int, upload_rwf, upload_d2e, upload_log]
   # Start new Threads
   for th in th_list:
      th.start()   

#   cmd = "./" + confdict['UPLOADER_EXECUTABLE_NAME'] + ' ' + conf_file + ' &'
#   print "spawning the chk chunk uploader subprocess, cmd = ", cmd
   #proc1 = subprocess.Popen([cmd, ChkName, UploadFreq, SE1])
#   status = os.system(cmd)
#   status = os.system("ps auxwf | grep " + confdict['UPLOADER_EXECUTABLE_NAME'] + " | grep -v grep | awk '{print $2}' > uploader_pidfile")
#   pidfile = open("./uploader_pidfile", 'r')
#   pid = pidfile.readline().strip().rstrip()
#   pidfile.close()
#   print "uploader running with pid = ", pid
#   fsock.flush()

################################################################################
##             Setting up the environment and launching g09                   ##
################################################################################

cmd = "export g09root=./ GAUSS_SCRDIR=./gauss_scratch; . $g09root/g09/bsd/g09.profile; g09 " + confdict['GAUSS_COM_FILE']
print "setting up the environment for g09 and launching Gaussian, cmd = " + cmd
fsock.flush()
status = os.system(cmd)
print status
fsock.flush()


################################################################################
##             G09 is now done, killing the uploader                          ##
################################################################################

#External uploader not used anymore, sending exit signal to uploading threads

#if (confdict['USE_PERIODIC_UPLOADER'] == "True") & (pid != None) :
if confdict['USE_PERIODIC_UPLOADER'] == "True" :

   # Notify threads it's time to exit
   print "Notify threads it's time to exit"
   fsock.flush()
   upload_threaded.ExitFlag = 1

   # Wait for all threads to complete
   for th in th_list:
      th.join()


#   pid_str = str(pid)
#   if pid_str.isdigit():
#      cmd = "kill -9 " + str(pid)
#      print "killing the uploader subprocess, cmd = " + cmd
#      fsock.flush()
#      status = os.system(cmd)
#      print status
#      fsock.flush()
#   else:
#      print "Not Killing the uploader subprocess, pid is not a number"
#      fsock.flush()

################################################################################
##                   Time to upload output files                              ##
##    Note that just one se can be defined, this should beimproved            ##
################################################################################

def upload_file(remote_file_name, local_file_name, sock):
   cmd = "lcg-cr -v --vo " + confdict['VO'] + " --connect-timeout " + confdict['CONNECT_TIMEOUT'] + " --sendreceive-timeout " + confdict['SENDRECEIVE_TIMEOUT'] + " --bdii-timeout " + confdict['BDII_TIMEOUT'] + " --srm-timeout " + confdict['SRM_TIMEOUT'] + "  -d " + confdict['OUTPUT_SE'] + " -l lfn:" + confdict['GRID_LFN_PATH'] + "/" + remote_file_name + " file:./" + local_file_name
   print "Uploading log file to the grid..., cmd = " + cmd
   sock.flush()
   status = os.system(cmd)
   print status
   sock.flush()
   if status != 0:
      sock.flush()
      cmd = "lcg-cr -v --vo " + confdict['VO'] + " --connect-timeout " + confdict['CONNECT_TIMEOUT'] + " --sendreceive-timeout " + confdict['SENDRECEIVE_TIMEOUT'] + " --bdii-timeout " + confdict['BDII_TIMEOUT'] + " --srm-timeout " + confdict['SRM_TIMEOUT'] + "  -d " + confdict['REPLICA_SE'] + " -l lfn:" + confdict['GRID_LFN_PATH'] + "/" + remote_file_name + " file:./" + local_file_name
      print "WARNING: First upload trial failed. Trying the backup SE..." + "cmd is : " + cmd 
      status2 = os.system(cmd)
      print status2
      sock.flush()
      if status2 != 0:
         print "ERRROR: Also the replica failed. It was not possible to upload the file on the grid. File was: ", local_file_name

### Uploading the g09 log file first....


upload_file(confdict['GAUSS_LOG_FILE'], confdict['GAUSS_LOG_FILE'], fsock)


## Uploading the final chk file

upload_file(confdict['GAUSS_CHK_FILE'], confdict['GAUSS_CHK_PATH'] + '/' + confdict['GAUSS_CHK_FILE'], fsock)

## List scratch_dir

cmd = "ls -ltr " + confdict['GAUSS_SCRATCH_PATH'] + " >> std.out" 
print "Listing scratch dir..., cmd = " + cmd
fsock.flush()
status = os.system(cmd)
print status
fsock.flush()

## Uploading the final int file

upload_file(confdict['GAUSS_INT_FILE'], confdict['GAUSS_SCRATCH_PATH'] + '/' + confdict['GAUSS_INT_FILE'], fsock)

## Uploading the final rwf file

upload_file(confdict['GAUSS_RWF_FILE'], confdict['GAUSS_SCRATCH_PATH'] + '/' + confdict['GAUSS_RWF_FILE'], fsock)

## Uploading the final d2e file

upload_file(confdict['GAUSS_D2E_FILE'], confdict['GAUSS_SCRATCH_PATH'] + '/' + confdict['GAUSS_D2E_FILE'], fsock)

################################################################################
##                           THAT'S ALL FOLKS!!!                              ##
################################################################################

print "END of gauss_wrapper.py"
fsock.flush()
sys.stdout = saveout
fsock.close()
