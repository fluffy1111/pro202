'''
SERVER - Server is the one that
works behind the scenes.
It’s like the back-end of the
app

CLIENT - Client is the program that
the user uses. It’s like the
front-end of the app
'''

import socket
from threading import Thread
from tkinter import *

nickname = input("Choose your nickname: ")

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

ip_address = '127.0.0.1'
port = 8000

client.connect((ip_address, port))

print("Connected with the server...")

class GUI:
    def __init__(self):
        self.Window = Tk() #Tk() is used to create the main the main window of the app
        self.Window.withdraw()

        #----------------LOGIN SCREEN [Top Screen]---------------------------------
        self.login = Toplevel()
        self.login.title("Login")
        self.login.resizable(width=False, height=False) #we don't want the login window to be resizable
        self.login.configure(width=400, height=300)
        self.pls = Label(self.login,
					text = "Please login to continue",
					justify = CENTER,
					font = "Helvetica 14 bold")
        self.pls.place( relheight = 0.15,  #place is is used to position the objects
                        relx = 0.2,
                        rely = 0.07)

        self.labelName = Label(self.login,
							text = "Name: ",
							font = "Helvetica 12")
        self.labelName.place(relheight = 0.2,
							relx = 0.1,
							rely = 0.2)
        #Entry() object is used as input field
        self.entryName = Entry(self.login,
							font = "Helvetica 14")
        self.entryName.place(relwidth = 0.4,
							relheight = 0.12,
							relx = 0.35,
							rely = 0.2)
        self.entryName.focus()
        #lambda stops the code from running all the time. It is similar to the arrow function in JS
        self.go = Button(self.login,text="Continue",font = "Helvetica 14 bold" , command= lambda:self.goAhead(self.entryName.get()))
        self.go.place(relx = 0.4,rely = 0.55) 
        self.Window.mainloop()

    def goAhead(self,name):
        self.login.destroy()
        self.name = name
        recv = Thread(target = self.receive)
        self.layout(name)
    
    def receive():
        while True:
            try:
                message = client.recv(2048).decode('utf-8')
                if message == 'NICKNAME':
                    client.send(nickname.encode('utf-8'))
                else:
                    print(message)
            except:
                print("An error occured!")
                client.close()
                break

    def layout(self,name):
        
        self.name = name
        self.Window.deiconify()
        self.Window.title("CHATROOM")
        self.Window.resizable(width = False,
                              height = False)
        self.Window.configure(width = 470,
                              height = 550,
                              bg = "#17202A")
        self.textArea.place(relwidth = 1)
        self.textArea = Text(self.Window,
                         width = 20,
                         height = 2,
                         bg = "#17202A",
                         fg = "#EAECEE",
                         font = "Helvetica 14",
                         padx = 5,
                         pady = 5)
        self.textArea = Entry(self.labelName,
                              bg = "#2C3E50",
                              fg = "#EAECEE"
                              font = "Helvetica 13")
        scrollbar = Scrollbar(self.textArea)
        scrollbar.place(relheight = 1,
                        relx = 0.974)
        
    def sendButton(self, msg):
        self.textArea.config(state = DISABLED)
        self.msg=msg
        self.entryMsg.delete(0,END)
        snd = Thread(target = self.write)
        snd.start()
    
    def Show_message(self,message):
        self.textArea.config(state = NORMAL)
        self.textArea.insert(END, message+"\n\n")
        self.textArea.config(state = DISABLED)
        self.textArea.see(END)

    def write(self):
        self.textArea.config(state = DISABLED)
        while True:
            message = (f"{self.name}: {self.msg}")
            client.send(message.encode('utf-8'))
            self.show_message(message)
            break

    def receive(self):
        while True:
            try:
                message = client.recv(2048).decode('utf-8')
                if message == 'NICKNAME':
                    client.send(self.name.encode('utf-8'))
                else:
                    self.Show_message(message)
            except:
                print("An error occured!")
                client.close()
                break
        

        

g = GUI()



# def write():
#     while True:
#         message = '{}: {}'.format(nickname, input(''))
#         client.send(message.encode('utf-8'))

# receive_thread = Thread(target=receive)
# receive_thread.start()
# write_thread = Thread(target=write)
# write_thread.start()
