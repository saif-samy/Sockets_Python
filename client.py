import socket
import sys
import cv2
import numpy as np
import time

HEADER = 64
PORT = 5050
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = '!DISCONNECT'
SERVER = socket.gethostbyname(socket.gethostname())
ADDR = (SERVER, PORT)

try: 
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print('[STARTING] client is starting')
except socket.error as err:
    print("Socket creation failed with error: %s" % (err))
    sys.exit()

try:
    client.connect(ADDR)
except:
    print('Error connecting to server!')
    sys.exit()

images_arr = []
count = 0
connected = True
start_time = time.time()
while connected:
    msgLength = client.recv(64)
    if msgLength:
        msgLength = int(msgLength)
        msg = client.recv(msgLength)
        try:
            if msg.decode(FORMAT) == '!DISCONNECT':
                connected = False
                print('[DISCONNECTED]')
        except:
            print('Packet Size:', msgLength, 'Packet Number:', count + 1)
            count += 1
            images_arr.append(msg)
client.close()
print("--- %s seconds ---" % (time.time() - start_time))


img = images_arr[0]
img = np.frombuffer(img, np.uint8)
img = cv2.imdecode(img, 3)
height, width, layers = img.shape
size = (width,height)
out = out = cv2.VideoWriter('project.avi',cv2.VideoWriter_fourcc(*'DIVX'), 30, size)

for i in range(len(images_arr)):
    img = images_arr[i]
    img = np.frombuffer(img, np.uint8)
    img = cv2.imdecode(img, 3)
    out.write(img)
out.release()
        
