import socket
soc = socket.socket()
serverName = 'localhost'
port = 6066

soc.connect((serverName, port))
print(soc.recv(1024))

soc.send("yes\n")

print(soc.recv(25))

currentMap = []
for i in range(961):
	message = soc.recv(4)
	currentMap.append(int(message[2:]))

for i, i2 in enumerate(currentMap):
	print(i, i2)