import socket
import sys
import cv2

HEADER = 64
PORT = 5050
# Getting the local address of the computer since we are running the server on our local network
SERVER = socket.gethostbyname(socket.gethostname())
ADDR = (SERVER, PORT)
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = '!DISCONNECT'

try: 
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print('[STARTING] server is starting')
except socket.error as err:
    print("Socket creation failed with error: %s" % (err))
    sys.exit()

# Binding the socket with the local address of the computer
server.bind(ADDR)

server.listen()
print(f'[LISTENING] server is listening on {SERVER}')

def encodeImage(img):
    return cv2.imencode('.jpeg', img)[1].tobytes()

def send(message):
    msgLength = len(message)
    sendLength = str(msgLength).encode(FORMAT)
    sendLength += b' ' * (HEADER - len(sendLength))
    clientSocket.send(sendLength)
    # This print has been added because two send functions directly after each other causes an error for some reason
    print('Sending Packet........')
    if (message == '!DISCONNECT'):
        clientSocket.send(message.encode(FORMAT))
    else:
        clientSocket.send(message)

def sendVideo():
    vidcap = cv2.VideoCapture('video.mp4')
    success,image = vidcap.read()
    count = 0
    while success:
        send(encodeImage(image))   
        success,image = vidcap.read()
        count += 1

while True:
    clientSocket, clientAddress = server.accept()
    sendVideo()
    send(DISCONNECT_MESSAGE)
