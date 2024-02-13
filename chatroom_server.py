import socket 
from threading import Thread

# IP address, for local and public address.
LOCAL_ADDR = ('192.168.1.105', 10000)
LOCAL_ADDR_RESERVE = ('localhost', 10000)
ACTIVE = True
CLIENT_CONNECTED = True
# We can aslo add the data encoding type. For example:
ENCODING = 'utf-8'

# Clients that are connected will be appended into the list.
client_list = []
# Creating a TCP socket.
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# Trying to bind one of addr.
try:
    server.bind(LOCAL_ADDR)
    print(f'[SERVER ACTIVE] The server is activated with address {LOCAL_ADDR}')
except:
    server.bind(LOCAL_ADDR_RESERVE)
    print(f'[SERVER ACTIVE] The server is activated with address {LOCAL_ADDR_RESERVE}')
# Max value of connected devices. Self socket is counted as one of the connections.
server.listen(10)
# Starting thread with new connection. 
# If message from client is equal to '!end!' thread will be broken and connection closed.
# The client will be removed from the client_list.
# If the clients message is equal to '!end!' server send this message closes connection.
# Client --> after getting the '!end!' message breaks the connection and stops recv().

def new_client_thread(conn, addr):
    while CLIENT_CONNECTED:
        message = conn.recv(1024)
        if message.decode() == '!end!':
            conn.send('!end!'.encode())
            conn.close()
            client_list.remove(conn)
            print(f'[CLIENT SUCCESFULLY REMOVED] The client {addr} was removed.')
            print(f'[ONLINE_CLIENTS] Clients that are active at time: {len(client_list)}')
            break
        else:
            for client in client_list:
                client.send(message)


# While server is active, it will accept new connections and start threads for them to listen every of them.
while ACTIVE:
    conn, addr = server.accept()
    print(f'[NEW_CLIENT] {addr} was connected to the server.')
    if conn:
        client_list.append(conn)
        new_client = Thread(target=new_client_thread, args=(conn, addr))
        new_client.start()
    print(f'[ONLINE_CLIENTS] Clients that are active at time: {len(client_list)}')
server.close()


"""                               ____    ______  ____    ______     
                                /\  _`\  /\  _  \/\  _`\ /\__  _\    
                                \ \,\L\_ \ \ \L\ \ \ \L\ \/_/\ \/    
                                 \/_\__ \ \ \  __ \ \  _ <' \ \ \    
                                   /\ \L\  \ \ \/\ \ \ \L\ \ \_\ \__ 
                                   \ `\____ \ \_\ \_\ \____/ /\_____\
                                    \/_____/ \/_/\/_/\/___/  \/_____/
                                                                                                                                
"""










