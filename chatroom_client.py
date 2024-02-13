from tkinter import messagebox
import socket
import customtkinter as ctk
from threading import Thread
from datetime import datetime

sample = ['']
ENCODING = 'utf-8'
# Adding client to list to lighten managing with it.
client_list = []
# GUI settings. Dark theme as default.
ctk.set_appearance_mode('dark')
root = ctk.CTk()
root.title('Chatroom')
root.geometry('650x500')
# App consist from 4 GUI parts. There are Sidebar, Header, Body, Footer.
# By the way you can fill Sidebar with new Widgets and functionalities.
# Sidebar--->
# Dark and Light theme switcher function.


def switcher():
    if switch_var.get() == 'on':
        ctk.set_appearance_mode('light')
        switch.configure(text='Light')
        header.configure(fg_color='white')
        sidebar.configure(fg_color='white')
    else:
        ctk.set_appearance_mode('dark') 
        switch.configure(text='Dark')
        header.configure(fg_color='grey')
        sidebar.configure(fg_color='grey')


switch_var = ctk.StringVar(value='off')
sidebar = ctk.CTkFrame(master=root, fg_color='grey')
sidebar.place(relx=0, rely=0, relwidth=0.3, relheight=1)

switch = ctk.CTkSwitch(master=sidebar, text='Dark', command=switcher, onvalue='on', offvalue='off', variable=switch_var)
switch.pack(padx=10, pady=15)
# Header--->
header = ctk.CTkFrame(master=root, fg_color='grey')
header.place(relx=0.3, rely=0, relwidth=0.7, relheight=0.1)
client_name = ctk.CTkLabel(master=header, text='Welcome to local Chatroom!', font=ctk.CTkFont(size=34))
client_name.pack()
# Body--->
body = ctk.CTkScrollableFrame(master=root)
body.place(relx=0.3, rely=0.1, relwidth=0.7, relheight=0.82)
# Footer--->
footer = ctk.CTkFrame(master=root)
footer.place(relx=0.3, rely=0.93, relwidth=0.7, relheight=0.06 )
# Text entry for user's inputs.
text_entry = ctk.CTkEntry(master=footer, placeholder_text='write your mail...')
text_entry.place(relx=0, rely=0, relwidth=0.85, relheight=1)


# Function of sending that is included into button's command
# send_msg--->get text from entry->format it->send to client->create widget->clear the entry. 


def send_msg():
    try:
        current_time = f"[{str(datetime.now().hour)}:{str(datetime.now().minute)}:{str(datetime.now().second)}]   "
        message_text = text_entry.get()
        sample.append(message_text)
        message_text = current_time + message_text
        client_list[0].send(text_entry.get().encode())
        if len(text_entry.get()) > 55:
            message_text = message_text[:55] + '\n' + message_text[55:]
        label = ctk.CTkLabel(master=body, text=message_text, anchor='w', justify='right', corner_radius=5)
        label.pack(ipady=3, pady=2, anchor=ctk.E)
        text_entry.delete(0, 'end')
    except Exception as x:
        messagebox.showwarning(title='Connection Error!', message=x)


# Message sending button that call the function send_msg().
sending_button = ctk.CTkButton(master=footer, text='Send', command=send_msg)
sending_button.place(relx=0.85, rely=0, relwidth=0.15, relheight=1)
# Function for connection to the server.


def main():
    def connect_to_server():
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            server.connect(('localhost', 10000))
            print('localhost is active')
        except:
            server.connect(('192.168.1.105', 10000))
            print('192.168.1.105 is active')
        while True:
            if server:
                current_time = f"[{str(datetime.now().hour)}:{str(datetime.now().minute)}:{str(datetime.now().second)}]   "
                client_list.append(server)
                income = server.recv(1024).decode()
                if income == '!end!':
                    break
                if income != sample[-1]:
                    print(income)
                    message_text = current_time + income
                    if len(text_entry.get()) > 55:
                        message_text = message_text[:55] + '\n' + message_text[55:]
                    label = ctk.CTkLabel(master=body, text=message_text, anchor='w',
                                     justify='right', corner_radius=5)
                    label.pack(ipady=3, pady=2, anchor=ctk.W)
    connect_to_server()

# Starting Thread. 
sock = Thread(target=main)
sock.start()
# Detecting 'q' key pressing. On 'q' key pressed end the session.


def key_pressed(event):
    if event.char == 'q':
        root.destroy()
        client_list[0].send('!end!'.encode())


root.bind("<Key>", key_pressed)
root.mainloop()

"""                                  ____     ______  ____    ______     
                                    /\  _`\  /\  _  \/\  _`\ /\__  _\    
                                    \ \,\L\_ \ \ \L\ \ \ \L\ \/_/\ \/    
                                     \/_\__ \ \ \  __ \ \  _ <' \ \ \    
                                       /\ \L\  \ \ \/\ \ \ \L\ \ \_\ \__ 
                                       \ `\____ \ \_\ \_\ \____/ /\_____\
                                        \/_____/ \/_/\/_/\/___/  \/_____/
"""


