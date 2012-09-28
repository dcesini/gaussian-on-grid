#!/usr/bin/python

import os, sys, time
import readconf
import threading


#saveout = sys.stdout
fsock = open('upload_threaded.log', 'a')
#sys.stdout = fsock

conf_file = sys.argv[1]
confdict = readconf.readconf(conf_file)

DeletePrevious = confdict['DELETE_PREVIOUS_UPLOADED']

timestr = time.strftime("%a, %d %b %Y %H:%M:%S ", time.localtime())

fsock.write("Upload chk utility started on: " + timestr + '\n')
fsock.flush()
#sys.stdout.flush()

class Uploader (threading.Thread):

   def __init__(self, thrd_name, local_name, local_path, remote_path, freq, se1, se2, vo):
      self.name = thrd_name
      self.local_name = local_name
      self.local_path = local_path
      self.remote_path = remote_path
      self.freq = freq
      self.se1 = se1
      self.se2 = se2
      self.vo = vo
      threading.Thread.__init__(self)

   def thprint(self,text):
      fsock.flush()
      self.blog = time.strftime("%a, %d %b %Y %H:%M:%S ", time.localtime()) + " : " + self.name + " : " + text
      fsock.write(self.blog)
      fsock.flush()

   def run(self):
      self.thprint("Uploading file " + self.local_name + " with a frequency of " + str(self.freq) + "s. to SE " + self.se1 + '\n')
      self.thprint("Sleeping for " + str(self.freq) + " before uploading the first file\n")
      self.DeletePrevious = DeletePrevious
      self.previousfile = None
      while True:
         self.thprint("Starting " + self.name)
         self.filetime = time.strftime("%d%b%Y_%H%M%S ", time.localtime())
         self.remote_name = self.local_name + self.filetime
         self.destcp_name = self.local_path + self.local_name + ".BAK"
         self.cmd = "cp " + self.local_path  + self.local_name + " " + self.destcp_name
         self.thprint("Creating " + self.local_name + " BAK copy..., cmd = " + self.cmd + '\n')
         self.status = os.system(self.cmd)
         self.thprint("status = " + str(self.status) + '\n')
         self.cmd = "lcg-cr -v --vo " + self.vo + " --connect-timeout 300 --sendreceive-timeout 900 --bdii-timeout 300 --srm-timeout 300 -d " + self.se1 + " -l lfn:" + self.remote_path + '/' + self.remote_name + " file:" + self.destcp_name
         self.thprint("Uploading " + self.local_name + " file to the grid..., cmd = " + self.cmd + '\n')
         self.status = os.system(self.cmd)
         self.thprint("status = " + str(self.status) + '\n')
         self.upload_status = self.status
         self.cmd = "rm -f " + self.destcp_name
         self.thprint("Deleting " + self.local_name + " BAK copy..., cmd = " + self.cmd + '\n')
         self.status = os.system(self.cmd)
         self.thprint("status = " + str(self.status) + '\n')
         if self.upload_status == 0:
            if (self.DeletePrevious == "True") & (self.previousfile != None):
               self.cmd = "lcg-del -a  lfn:" + self.remote_path + '/' + self.previousfile
               self.thprint("Detected deletion enabled: deleteing previous file from the grid..., cmd = " + self.cmd + '\n')
               self.status = os.system(self.cmd)
               self.thprint("status = " + str(self.status) + '\n')

         self.thprint("At " + time.strftime("%a, %d %b %Y %H:%M:%S ", time.localtime()) + " sleeping for " + str(self.freq) + "s.  before uploading the next chunk\n")
         self.previousfile = self.remote_name
         time.sleep(self.freq)
#         print "Exiting " + self.name


# Create new threads
upload_chk = Uploader("upload_chk", confdict['GAUSS_CHK_FILE'], confdict['GAUSS_CHK_PATH'], confdict['GRID_LFN_PATH'], int(confdict['CHK_UPLOAD_FREQ']), confdict['OUTPUT_SE'], confdict['REPLICA_SE'], confdict['VO'])

upload_int = Uploader("upload_int", confdict['GAUSS_INT_FILE'], confdict['GAUSS_SCRATCH_PATH'], confdict['GRID_LFN_PATH'], int(confdict['INT_UPLOAD_FREQ']), confdict['OUTPUT_SE'], confdict['REPLICA_SE'], confdict['VO'])

upload_rwf = Uploader("upload_rwf", confdict['GAUSS_RWF_FILE'], confdict['GAUSS_SCRATCH_PATH'], confdict['GRID_LFN_PATH'], int(confdict['RWF_UPLOAD_FREQ']), confdict['OUTPUT_SE'], confdict['REPLICA_SE'], confdict['VO'])

upload_d2e = Uploader("upload_d2e", confdict['GAUSS_D2E_FILE'], confdict['GAUSS_SCRATCH_PATH'], confdict['GRID_LFN_PATH'], int(confdict['D2E_UPLOAD_FREQ']), confdict['OUTPUT_SE'], confdict['REPLICA_SE'], confdict['VO'])

upload_log = Uploader("upload_log", confdict['GAUSS_LOG_FILE'], "./" , confdict['GRID_LFN_PATH'], int(confdict['D2E_UPLOAD_FREQ']), confdict['OUTPUT_SE'], confdict['REPLICA_SE'], confdict['VO'])

# Start new Threads
upload_chk.start()
upload_int.start()
upload_rwf.start()
upload_d2e.start()
upload_log.start()

# restoring sys.out and closing socket file
#sys.stdout = saveout
#fsock.close()
