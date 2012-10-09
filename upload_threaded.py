#!/usr/bin/python

import os, sys, time
import threading

ExitFlag = 0
class Uploader (threading.Thread):

   def __init__(self, fsock, thrd_name, local_name, local_path, remote_path, freq, se1, se2, vo, conn_timeout, send_timeout, bdii_timeout, srm_timeout,DeletePrevious):
      self.fsock = fsock
      self.thname = thrd_name
      self.local_name = local_name
      self.local_path = local_path
      self.remote_path = remote_path
      self.freq = freq
      self.se1 = se1
      self.se2 = se2
      self.vo = vo
      self.conn_timeout = conn_timeout
      self.send_timeout = send_timeout
      self.bdii_timeout = bdii_timeout
      self.srm_timeout  = srm_timeout
      self.DeletePrevious = DeletePrevious
      threading.Thread.__init__(self)

   def thprint(self,text):
      self.fsock.flush()
      self.blog = time.strftime("%a, %d %b %Y %H:%M:%S ", time.localtime()) + " : " + self.thname + " : " + text
      self.fsock.write(self.blog)
      self.fsock.flush()

   def run(self):
      self.thprint("Uploading file " + self.local_name + " with a frequency of " + str(self.freq) + "s. to SE " + self.se1 + " and to SE (replicas) " + self.se2 + '\n')
      self.thprint("Sleeping for " + str(self.freq) + " before uploading the first file\n")
      time.sleep(self.freq)
      self.reftime = 0
      self.previousfile = None
      while not ExitFlag:
         if (time.time() - self.reftime) > self.freq :  
            self.thprint("Wake up: time to upload my files\n")
            self.filetime = time.strftime("%d%b%Y_%H%M%S ", time.localtime())
            self.remote_name = self.local_name + self.filetime
            self.destcp_name = self.local_path + self.local_name + ".BAK"
            self.cmd = "cp " + self.local_path  + self.local_name + " " + self.destcp_name
            self.thprint("Creating " + self.local_name + " BAK copy..., cmd = " + self.cmd + '\n')
            self.status = os.system(self.cmd)
            self.thprint("status = " + str(self.status) + '\n')
            self.cmd = "lcg-cr -v --vo " + self.vo + " --connect-timeout " + self.conn_timeout + " --sendreceive-timeout " + self.send_timeout +" --bdii-timeout " + self.bdii_timeout + " --srm-timeout " + self.srm_timeout + " -d " + self.se1 + " -l lfn:" + self.remote_path + '/' + self.remote_name + " file:" + self.destcp_name
            self.thprint("Uploading " + self.local_name + " file to the grid..., cmd = " + self.cmd + '\n')
            self.status = os.system(self.cmd)
            self.thprint("status = " + str(self.status) + '\n')
            self.upload_status = self.status
            if self.upload_status != 0:
               self.thprint("WARNING: First upload trial failed. Trying the backup SE...")
               self.cmd = "lcg-cr -v --vo " + self.vo + " --connect-timeout " + self.conn_timeout + " --sendreceive-timeout " + self.send_timeout +" --bdii-timeout " + self.bdii_timeout + " --srm-timeout " + self.srm_timeout + " -d " + self.se2 + " -l lfn:" + self.remote_path + '/' + self.remote_name + " file:" + self.destcp_name
               self.thprint("Uploading " + self.local_name + " file to the grid using replica SE..., cmd = " + self.cmd + '\n')
               self.status2 = os.system(self.cmd)
               self.thprint("status = " + str(self.status2) + '\n')
               if self.status2 != 0:
                  self.thprint("ERRROR: Also the replica failed. It was not possible to upload the file on the grid.")
               self.upload_status = self.status2
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

            self.reftime = time.time()
            self.thprint("I did all that I could do to upload my file, waiting for the next iteration or the exit signal\n")
            self.previousfile = self.remote_name

         else:
            time.sleep(60)
            self.reftime = time.time()
      self.thprint("Exiting thread " + thrd_name)
