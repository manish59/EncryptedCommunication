### Run Python scripts as a service example (ryrobes.com)
### Usage : python aservice.py install (or / then start, stop, remove)

import win32service
import win32serviceutil
import win32api
import win32con
import win32event
import win32evtlogutil
import os, sys, string, time

class aservice(win32serviceutil.ServiceFramework):
   
   _svc_name_ = "Daemon_Server"
   _svc_display_name_ = "Exectuing command"
   _svc_description_ = "Created by manish"
         
   def __init__(self, args):
           win32serviceutil.ServiceFramework.__init__(self, args)
           self.hWaitStop = win32event.CreateEvent(None, 0, 0, None)          

   def SvcStop(self):
           self.ReportServiceStatus(win32service.SERVICE_STOP_PENDING)
           win32event.SetEvent(self.hWaitStop)                    
         
   def SvcDoRun(self):
      import servicemanager      
      servicemanager.LogMsg(servicemanager.EVENTLOG_INFORMATION_TYPE,servicemanager.PYS_SERVICE_STARTED,(self._svc_name_, ''))
     
      #self.timeout = 640000    #640 seconds / 10 minutes (value is in milliseconds)
      self.timeout = 1    #120 seconds / 2 minutes
      # This is how long the service will wait to run / refresh itself (see script below)

      while 1:
         # Wait for service stop signal, if I timeout, loop again
         rc = win32event.WaitForSingleObject(self.hWaitStop, self.timeout)
         # Check to see if self.hWaitStop happened
         if rc == win32event.WAIT_OBJECT_0:
            # Stop signal encountered
            servicemanager.LogInfoMsg("SomeShortNameVersion - STOPPED!")  #For Event Log
            break
         else:
			 while True:
				import socket
				import threading
				import sys
				import os
				import socket
				from Crypto.Signature import PKCS1_v1_5
				import platform
				from Crypto.Hash import SHA
				from Crypto.PublicKey import RSA
				import base64
				from Crypto.Cipher import PKCS1_OAEP
				from Crypto.Hash import SHA256
				from base64 import b64decode
				sock=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
				sock.bind(("0.0.0.0",9947))
				sock.listen(5)
				def decrypt_RSA(package):
					key = open('private_key.txt', "r").read()
					rsakey = RSA.importKey(key)
					rsakey = PKCS1_OAEP.new(rsakey)
					decrypted = rsakey.decrypt(b64decode(package))
					return decrypted
				def verify_sign(signature, data):
					pub_key = open('public_key.txt', "r").read()
					rsakey = RSA.importKey(pub_key)
					signer = PKCS1_v1_5.new(rsakey)
					digest = SHA256.new()
					# Assumes the data is base64 encoded to begin with
					digest.update(b64decode(data))
					if signer.verify(digest, b64decode(signature)):
						return True
					else:	
						return False
				def connection_establish(cli_sock,cli_addr):
					signature=cli_sock.recv(4096)
					message=cli_sock.recv(4096)
					aaa=decrypt_RSA(message)
					if aaa=="manish":
						if verify_sign(signature,message):
							cli_sock.send("You are a trusted visitor ")
							command_sending(cli_sock,cli_addr)
						else:
								cli_sock.send("You are not trusted visitor ")
					else :
						cli_sock.send("You are not trusted visitor")
				def command_sending(cli_sock,cli_addr):
					while True:
						b=cli_sock.recv(4096)
						list1=["date","ls","cal","exit","end","shutdown"]
						if b in list1:
							if b=="end" or b=="exit":
								cli_sock.send("Connection termination ...!")
								break
							elif b=="shutdown":
								c=os.system("shutdown -P now")
								cli_sock.send("You have shutdown the remote system succefully")
							else :
									c=os.popen(b)
									d=c.read()
									cli_sock.send(d)
						else:
							cli_sock.send("You have entered unauthorised syntax")
							cli_sock.close()
							break
				print 4
				while True:
					print 6
					cli_sock,cli_addr=sock.accept()
					a=threading.Thread(target=connection_establish(cli_sock,cli_addr))
					a.start()
				
def ctrlHandler(ctrlType):
   return True
                 
if __name__ == '__main__':  
   win32api.SetConsoleCtrlHandler(ctrlHandler, True)  
   win32serviceutil.HandleCommandLine(aservice)
