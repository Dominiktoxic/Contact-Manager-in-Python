from cryptography.fernet import Fernet
import os
from tkinter import *
from tkinter import messagebox

class Contacts:
    def __init__(self):
        self.contacts = {}
        self.key = None
        self.keyfile = "key.key"
        self.contactsfile = "contacts.pass"
        
        # Checking for key
        if self.keyfile in os.listdir():
            with open(self.keyfile, "rb") as f:
                self.key = f.read()
        else:
            self.generate_key()
        
        # Checking for contacts
        if self.contactsfile in os.listdir():
            with open(self.contactsfile, "r") as f:
                for line in f.readlines():
                    name, contact = line.split("|")
                    contact = Fernet(self.key).decrypt(contact.encode()).decode()
                    self.contacts[name] = contact
        else:
            with open(self.contactsfile, "x") as f:
                pass
    
    def generate_key(self):
        self.key = Fernet.generate_key()
        
        with open(self.keyfile, "wb") as f:
            f.write(self.key)

    def add_contact(self, name, contact):
        if name == "" or contact == "":
            print("Process Failed.")
        else:
            with open(self.contactsfile, "a") as f:
                f.write(name + "|" + Fernet(self.key).encrypt(contact.encode()).decode() + "\n")
            self.contacts[name] = contact

    def view_contact(self, name):
        if name == "":
            pass
        else:
            try:
                messagebox.showinfo("Contact", f"Name: {name}\nContact: {self.contacts[name]}")
            except KeyError:
                print(f"Could not find a contact with the name: {name}")

contacts = Contacts()

# GUI

maxX = 750
maxY = 386

screen = Tk()

title = "Contacts Manager"
screen.title(title)

screen.maxsize(maxX, maxY)
screen.minsize(maxX, maxY)

header = Label(screen, text="Contacts Manager", font=("Arial Black", 50))
header.pack()

nameTitle = Label(screen, text="Name", font=("Arial Bold", 25))
nameTitle.pack()

nameEntry = Entry(screen, font=("Arial Bold", 21))
nameEntry.pack()

contactTitle = Label(screen, text="Contact", font=("Arial Bold", 25))
contactTitle.pack()

contactEntry = Entry(screen, font=("Arial Bold", 21))
contactEntry.pack()

submit = Button(screen, text="Submit", font=("Arial Bold", 21), command = lambda: contacts.add_contact(nameEntry.get(), contactEntry.get()))
submit.place(x = maxX / 2 - 60, y = 280)

retrieve = Button(screen, text="Retrieve Contact", font=("Arial Bold", 15), command = lambda: contacts.view_contact(nameEntry.get()))
retrieve.place(x = maxX / 2 + 186, y = 180)

screen.mainloop()