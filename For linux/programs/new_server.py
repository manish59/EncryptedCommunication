import socket
import base64
from Crypto.Signature import PKCS1_v1_5
from Crypto.Hash import SHA
from Crypto.PublicKey import RSA
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
import sys
sock=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
sock.connect((str(sys.argv[1]),int(sys.argv[2])))
def connection_establish():
	message=raw_input("Enter :")
	encrypted_message=encrypt_RSA(message)
	signature=sign_data(encrypted_message)
	sock.send(signature)
	print 
	sock.send(encrypted_message)
	confirmation_message=sock.recv(4096)
	print confirmation_message
	return confirmation_message
def sign_data(data):
	from Crypto.PublicKey import RSA
	from Crypto.Signature import PKCS1_v1_5
	from Crypto.Hash import SHA256
	from base64 import b64encode, b64decode
	key = open('private_key.txt', "r").read()
	rsakey = RSA.importKey(key)
	signer = PKCS1_v1_5.new(rsakey)
	digest = SHA256.new()
	digest.update(b64decode(data))
	sign = signer.sign(digest)
	sign1=b64encode(sign)
	return sign1	
def encrypt_RSA(message):
	from Crypto.PublicKey import RSA
	from Crypto.Cipher import PKCS1_OAEP
	key = open('public_key.txt', "r").read()
	rsakey = RSA.importKey(key)
	rsakey = PKCS1_OAEP.new(rsakey)
	encrypted = rsakey.encrypt(message)
	aa=encrypted.encode('base64')
	return aa
aa=connection_establish()
if aa=="You are not trusted visitor":
	sock.close
else:
	while True:
		a=raw_input("Enter your command :")
		if a=="end" or a=="exit":
			sock.send(a)
			recv=sock.recv(4096)
			print recv
			sock.close()
			break
		elif a==" " or a=="\t":
			continue
		else:
			sock.send(a)
			received=sock.recv(4096)
			if received=="You have entered unauthorised syntax":
				print received+" and your connection has been terminated"
				sock.close()
				break
			print received

