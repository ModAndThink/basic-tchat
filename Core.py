import tkinter as tk
import tkinter.font as tkFont
from Client import *
import threading

def open_a_file(file):
    data = []
    file = open(file,"r")
    file = file.readlines()
    for i in file:
        data.append(i)
    return data

def write_data(file,data):
    file = open(file,"w")
    file.write(data)
    file.close()

class Application(object):
    def __init__(self):
        self.window = tk.Tk()
        
        self.frameMsg = tk.Frame(master=self.window,width=200,height=900)
        self.scrollBarMsg = tk.Scrollbar(master=self.frameMsg)
        self.listMsg = tk.Listbox(master=self.frameMsg,yscrollcommand=self.scrollBarMsg.set,width=100)

        self.scrollBarMsg.config(command=self.listMsg.yview)
        
        self.scrollBarMsg.pack(side = tk.RIGHT, fill = tk.Y)
        self.frameMsg.pack()
        self.listMsg.pack(side=tk.LEFT,fill=tk.BOTH)

        self.frameSend = tk.Frame(master=self.window)
        self.input = tk.Entry(master=self.frameSend,width=95)
        self.buttonSend = tk.Button(master=self.frameSend,text="->",command=self.sendMessage)

        self.frameSend.pack()
        self.input.pack(side=tk.LEFT,fill=tk.BOTH)
        self.buttonSend.pack(side=tk.RIGHT,fill=tk.Y)

        self.clientInstance = None

    def addMessage(self,pseudo,text):
        self.listMsg.insert(tk.END,pseudo+" : "+text)

    def loop_message(self,clientInstance):
        while True:
            try:
                msg = clientInstance.waitingForMessage()
                msg = msg.split("|")

                if len(msg)==2:
                    self.addMessage(msg[0],msg[1])
            except:
                pass
            if self.clientInstance==None:
                break

    def sendMessage(self):
        value = self.input.get()
        self.input.delete(0,len(value))
        if value != "":
            if value[0] != "!":
                msg = MyAccount.account.name+" : "+value
                self.listMsg.insert(tk.END,msg)

                if self.clientInstance != None:
                    self.clientInstance.send(MyAccount.account.name+"|"+value)
            elif value[0] == "!":
                command = value.split()
                if command[0] == "!help":
                    self.addMessage("The assistant","there's actualy no command")
                elif command[0]== "!rename":
                    if len(command)==2 and command[1]!="The assistant":
                        MyAccount.account.name = command[1]
                        write_data("Profil.txt",command[1])
                        self.addMessage("The assistant","name change with success")
                    elif len(command)==1:
                        self.addMessage("The assistant","missing parameter")
                    elif len(command)>2:
                        self.addMessage("The assistant","superflu parmeter")
                    else:
                        self.addMessage("The assistant","invalide name")
                elif command[0]== "!connectToLobby" and len(command) >= 2:
                    
                    self.clientInstance = Client(port=5050,ip=command[1])
                    self.addMessage("The assistant","connection with the lobby")
                    self.clientInstance.send("client trying to connect using the tchatApp, send the valid code")

                    msg = self.clientInstance.waitingForMessage()

                    if msg == "30939211271":
                        print("Server valid")
                        self.addMessage("The assistant","connection succesfull")
                        self.clientInstance.send(MyAccount.account.name)
                        self.clientInstance.send("The assistant|"+MyAccount.account.name+" join lobby.")
                        thread = threading.Thread(target=self.loop_message,args = (self.clientInstance,))
                        thread.start()
                    else:
                        self.clientInstance = None
                        print("Server invalid, disconnect")
                        self.addMessage("The assistant","connection not succesfull")
                elif command[0] == "!disconnect" and len(command)==1 and self.clientInstance != None:
                    self.clientInstance.send("The assistant|"+MyAccount.account.name+" leave lobby.")
                    self.clientInstance.left()
                    self.clientInstance = None
                    self.addMessage("The assistant","server left")

class AccountCreator(object):
    def __init__(self):
        data = open_a_file("Profil.txt")
        if len(data) == 0:
            self.window = tk.Tk()
            
            self.frame = tk.Frame(master=self.window,width=50,height=900)
            self.input = tk.Entry(master=self.frame,width=50)
            self.buttonSend = tk.Button(master=self.frame,text="->",command=self.createAccount)
            self.labelError = tk.Label(master=self.window,text="invalid name",font=tk.font.Font(size=10),fg="red")

            self.frame.pack()
            self.input.pack(side=tk.LEFT,fill=tk.BOTH)
            self.buttonSend.pack(side=tk.RIGHT,fill=tk.Y)
            self.window.mainloop()
        else:
            MyAccount(data[0])
            app = Application()
            app.addMessage("The assistant","hola, type !help if you want to know all the command")
            app.window.mainloop()

    def createAccount(self):
        value = self.input.get()
        if value != "" and value != "The assistant" and len(value.split())==1:
            write_data("Profil.txt",value)
            MyAccount(value)
            app = Application()
            app.addMessage("The assistant","hola, type !help if you want to know all the command")
            self.window.destroy()
            app.window.mainloop()
        else:
            self.labelError.pack(side=tk.LEFT)

class MyAccount(object):
    account = None
    def __init__(self,name=None):
        self.name = name
        MyAccount.account=self

AccountCreator()
