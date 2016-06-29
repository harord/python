import socket
import time

#d = '0xFDFDFDFD 0x00000001 0xFDFDFDFC 0xFDFDFDFC 45 123465798241231313313131313131231321313131313 0xFEFEFEFE 0xFEFEFEFE'

isPoster = 1

#read kpp data, kpp from aomenfengyun
kppFile = open('D:/kpp/data.dat', 'rb')
data = kppFile.read(30*1024)
kppFile.close()
print 'kpp data len : ', len(data)

#construct send data
#protocol data header and tail
header = chr(0xfd) * 4
version = chr(0x01) + chr(0x00)*3
revert = header * 2
tail = chr(0xfe) * 4
cril = tail

#match data header
if not isPoster:
	dataHeaderTitle = chr(0x13) + chr(0x00) + chr(0x04) + chr(0x00)  #0x00040013
	target = ("127.0.0.1", 4304)
else:
	dataHeaderTitle = chr(0x01) + chr(0x00) + chr(0x02) + chr(0x00)  #0x00020001
	target = ("182.137.253.26", 43171)
	#target = ("127.0.0.1", 43171)
	
dataHeaderTVID = chr(0x00) * 4 #0x00000000
dataHeaderTvFrameID = chr(0x00) * 4 #0x00000000
dataHeaderTVFrameRate = chr(0x00) * 4 #8000
dataHeaderTVName = 'hntv' * 8

#send data
sendData = dataHeaderTitle + dataHeaderTVID + dataHeaderTvFrameID + dataHeaderTVFrameRate + dataHeaderTVName + data

dataLen = ''
ll = len(sendData)
l1 = ll & 0x000000FF
dataLen += chr(l1)
l2 = (ll & 0x0000FF00) >> 8
dataLen += chr(l2)
l3 = (ll & 0x00FF0000) >> 16
dataLen += chr(l3)
l4 = (ll & 0xFF000000) >> 24
dataLen += chr(l4)
print 'total data len:', ll, dataLen, l1, l2, l3, l4

sss = header + version + revert + dataLen + sendData + cril + tail

sockCount = 10
while True:
	ss = []
	try:
		for i in range(sockCount):
			sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
			sock.settimeout(1.0)
			ss.append(sock)

		for sock in ss:
			sock.connect(target)
			print 'sock connect ok:', sock

		for sock in ss:
			try:
				sock.send(sss)
				print 'sock send data success:', sock
				time.sleep(1)
			except socket.error as msg:
				print 'send error', msg
				
		for sock in ss:
			try:
				sock.recv(1024)
				print 'socket recv success', sock
			except socket.timeout:
				print 'socket recv timeout', sock
			
	except socket.error as msg:
		print 'socket error', msg
		break
	finally:
		for sock in ss:
			sock.close()
			print 'socket close ', sock

for sock in ss:
	sock.close()
