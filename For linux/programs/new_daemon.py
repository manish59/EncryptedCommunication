#!/usr/bin/env python

import sys, time
from daemon import Daemon
import socket
import threading
import sys
import os
import socket
from Crypto.Signature import PKCS1_v1_5
from Crypto.Hash import SHA
from Crypto.PublicKey import RSA
import base64
from Crypto.Cipher import PKCS1_OAEP
from Crypto.Hash import SHA256
from base64 import b64decode
class MyDaemon(Daemon):
	def run(self):
		print 1
		sock=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
		print 2
		sock.bind(("0.0.0.0",9947))
		sock.listen(5)
		print 3
		def decrypt_RSA(package):
			key = open('/home/manu/Desktop/project/private_key.txt', "r").read()
			rsakey = RSA.importKey(key)
			rsakey = PKCS1_OAEP.new(rsakey)
			decrypted = rsakey.decrypt(b64decode(package))
			return decrypted
		def verify_sign(signature, data):
			pub_key = open('/home/manu/Desktop/project/public_key.txt', "r").read()
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
if __name__ == "__main__":
	daemon = MyDaemon('/tmp/daemon-example.pid')
	if len(sys.argv) == 2:
		if 'start' == sys.argv[1]:
			daemon.start()
		elif 'stop' == sys.argv[1]:
			daemon.stop()
		elif 'restart' == sys.argv[1]:
			daemon.restart()
		else:
			daemon.start()
		sys.exit(0)
	else:
		print "usage: %s start|stop|restart" % sys.argv[0]
		sys.exit(2)
