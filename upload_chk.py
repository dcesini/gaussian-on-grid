#!/usr/bin/python

import os, sys, time

flog = open('upload.log', 'w')

ChkName = sys.argv[1]
UploadFreq =  sys.argv[2]
SE1 = sys.argv[3]

STEP = int(UploadFreq)

DeletePrevious = True

timestr = time.strftime("%a, %d %b %Y %H:%M:%S ", time.localtime())

flog.write("Upload chk utility started on: " + timestr + '\n')
flog.write("Uploading file " + ChkName + " with a frequency of " + UploadFreq + "s. to SE " + SE1 + '\n')
flog.write("Sleeping for " + UploadFreq + "s.  before uploading the first chunk\n")
flog.flush()

previousChk = None

while True:

# Uploading the chk and deleting previous instance

   filetime = time.strftime("%d%b%Y_%H%M%S ", time.localtime())
   ChkChunkName = ChkName + filetime
   cmd = "cp ./Gaussian/" + ChkName + " ./Gaussian/" + ChkName + ".BAK"
   flog.write("Creating CHK BAK copy..., cmd = " + cmd + '\n')
   status = os.system(cmd)
   flog.write("status = " + str(status) + '\n')
   flog.flush()
   cmd = "lcg-cr -v --vo comput-er.it --connect-timeout 30 --sendreceive-timeout 30 --bdii-timeout 30 --srm-timeout 30 -d " + SE1 + " -l lfn:/grid/comput-er.it/cesini/gauss/" + ChkChunkName + " file:./Gaussian/" + ChkName + ".BAK"
   flog.write("Uploading chk file to the grid..., cmd = " + cmd + '\n')
   flog.flush()
   status = os.system(cmd)
   flog.write("status = " + str(status) + '\n')
   cmd = "rm -f ./Gaussian/" +  ChkName + ".BAK"
   flog.write("Deleting CHK BAK copy..., cmd = " + cmd + '\n')
   status = os.system(cmd)
   flog.write("status = " + str(status) + '\n')
   flog.flush()

   if status == 0:
      if (DeletePrevious == True) & (previousChk != None):
         cmd = "lcg-del -a  lfn:/grid/comput-er.it/cesini/gauss/" + previousChk 
         flog.write("Detected deletion enabled: deleteing previous chk file from the grid..., cmd = " + cmd + '\n')
         flog.flush()
         status = os.system(cmd)
         flog.write("status = " + str(status) + '\n')

   flog.write("At " + time.strftime("%a, %d %b %Y %H:%M:%S ", time.localtime()) + " sleeping for " + UploadFreq + " before uploading the next chunk\n")
   flog.flush()
   previousChk = ChkChunkName
   time.sleep(STEP)
