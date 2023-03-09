import tkinter as tk
from tkinter import ttk
from sqlalchemy import create_engine
import os
from db import DB, create_tables
from crypto import Encrypt, Decrypt
from cryptography.fernet import InvalidToken


class PageOne(tk.Frame):
    def __init__(self, master, date):
        super().__init__(master)
        self.grid()
        self.date = date
        self.ask_password()
     
    def create_widgets(self,event):
        self.password_to_safe = self.password_to_decrypt.get()
        self.label_to_decrypt.destroy()
        self.password_to_decrypt.destroy()
        self.accept_to_decrypt.destroy()
        ttk.Label(self,text='portal').grid(row=0,column=0,padx=5)
        self.portal = ttk.Entry(self)
        self.portal.grid(row=0, column=1, pady=5)

        ttk.Label(self,text='login').grid(row=1,column=0,padx=5)
        self.login = ttk.Entry(self)
        self.login.grid(row=1, column=1, pady=5)

        ttk.Label(self,text='password').grid(row=2,column=0,padx=5)
        self.password = ttk.Entry(self, show='*')
        self.password.grid(row=2, column=1, pady=5)

        self.button = ttk.Button(self, text='Add credentials')
        self.button.bind('<Button-1>', self.on_click)
        self.button.grid(row=3, column=1, columnspan=2)
    
    def on_click(self, event):
        enc = Encrypt(self.password.get())
        self.date.add_credentials(
            self.portal.get(),
            self.login.get(),
            enc.execute(self.password_to_safe))
        self.portal.delete(0,'end')
        self.login.delete(0,'end')
        self.password.delete(0,'end')
    
    def ask_password(self):
        self.label_to_decrypt = ttk.Label(self, text="Haslo do szyfrowania")
        self.label_to_decrypt.grid(row=2, column=2)
        self.password_to_decrypt = ttk.Entry(self, show='*')
        self.password_to_decrypt.grid(row=3, column=2)
        self.accept_to_decrypt = ttk.Button(self, text='Accept')
        self.accept_to_decrypt.bind("<Button-1>", self.create_widgets)
        self.accept_to_decrypt.grid(row=4,column=2)

class PageTwo(tk.Frame):
    def __init__(self, master, date):
        super().__init__(master)
        self.grid()
        self.date = date
        self.ask_password()
    def ask_password(self):
        self.asking = ttk.Label(self, text="Haslo do odszyfrowania")
        self.asking.grid(row=2, column=2)
        self.password_to_decrypted = ttk.Entry(self, show='*')
        self.password_to_decrypted.grid(row=3, column=2)
        self.accept = ttk.Button(self, text='Accept')
        self.accept.bind("<Button-1>", self.create_widgets)
        self.accept.grid(row=4,column=2)

    def create_widgets(self, event):
        self.decrypt_pass = self.password_to_decrypted.get()
        self.asking.destroy()
        self.password_to_decrypted.destroy()
        self.accept.destroy()
        credentials = self.date.load_password()

        self.tree = ttk.Treeview(self,
                            columns=('portal', 'login'),
                            show='headings',
                            height=8
        )

        self.tree.heading('portal', text='portal')
        self.tree.heading('login', text='login')

        for credential in credentials:
            self.tree.insert('','end', values=(credential[0], credential[1], credential[2]))
        self.tree.bind('<<TreeviewSelect>>', self.on_select)
        self.tree.grid()
        self.tree.after(10000, quit)
    
    def on_select(self, event):
        item = self.tree.selection()[0]
        self.clipboard_clear()
        try:
            dec = Decrypt(self.tree.item(item, 'values')[2])
            self.clipboard_append(dec.execute(self.decrypt_pass))
        except InvalidToken:
            self.tree.destroy()
            self.ask_password()

def main():

    engine = create_engine('sqlite:///datebase.db', echo=True, future=True)
    if not os.path.exists('datebase.db'):
        create_tables(engine)
    
    date = DB(engine)
    root = tk.Tk()
    root.title('Password Manager')
    root.geometry('400x300')
    tabsystem = ttk.Notebook(root)
    tabsystem.grid(row=1, column=1)
    page_one = tk.Frame(tabsystem)
    page_two = tk.Frame(tabsystem)
    tabsystem.add(page_one, text='Add Password')
    tabsystem.add(page_two, text='Credentials')
    app1 = PageOne(page_one, date)
    app2 = PageTwo(page_two, date)
    root.mainloop()

if __name__=="__main__":
    main()