import socket
from threading import Thread
from tkinter import *


nickname=input("Enter your nickname: ")
client=socket.socket(socket.AF_INET, socket.SOCK_STREAM)

IPAddress = "127.0.0.1"
port=8001

client.connect((IPAddress, port))
print("Connected with the server...")

class GUI():
    def __init__(self):
        self.window = Tk()
        self.window.withdraw()

        self.login = Toplevel()
        self.login.title("Login")
        self.login.resizable(width=False, height=False)
        self.login.configure(width=400, height=300)

        self.pls = Label(self.login, text="Please login to continue", justify="center", font="Helvetica 14 bold")
        self.pls.place(relheight=0.15, relx=0.2, rely=0.07)

        self.labelname = Label(self.login, text="Name", font="Helvetica 12")
        self.labelname.place(relheight=0.2, relx=0.1, rely=0.2)

        self.entry = Entry(self.login, font="Helvetica 14")
        self.entry.place(relheight=0.12, relwidth=0.4, relx=0.35, rely=0.2)
        self.entry.focus()

        self.go = Button(self.login, text="Continue", font="Helvetica 14 bold", command=lambda:self.goahed(self.entry.get()))
        self.go.place(relx=0.4, rely=0.5)
        
        self.window.mainloop()

    def goahed(self, name):
        self.login.destroy()
        self.name=name
        rcv=Thread(target=self.recieve)
        rcv.start()

    def recieve(self):
        while True:
            try:
                message=client.recv(2048).decode("UTF-8")
                if message == "NICKNAME":
                    client.send(nickname.encode("utf-8"))
                else:
                    print(message)
            except:
                print("An error occurred")
                client.close()
                break

objectname = GUI()

'''def write():
    while True:
        message="{}: {}".format(nickname, input(""))
        client.send(message.encode("utf-8"))

recieveThread=Thread(target=recieve)
recieveThread.start()

writeThread=Thread(target=write)
writeThread.start()'''

 