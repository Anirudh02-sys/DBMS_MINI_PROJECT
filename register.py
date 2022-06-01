
import tkinter
import tkinter.font as tkFont
from typing import Sized
import sqlite3
from tkinter import *
from PIL import ImageTk, Image
from tkinter import messagebox

conn = sqlite3.connect('car_rental.db')


def submit():
    x = 0
    try:
        if e_password.get() == e_cpassword.get() and e_password.get() != '':
            x = 1
            cursor = conn.cursor()
            cursor.execute("""insert into login(username,password) values(:us,:p)""",
                           {
                               'us': e_username.get(),
                               'p': e_password.get(),
                           })
            conn.commit()
            cursor.execute(
                'SELECT user_id FROM user WHERE user_id=(SELECT max(user_id) FROM user);')
            id = cursor.fetchone()[0]
            id += 1
            cursor.execute("""insert into user values(:id,:us)""",
                           {
                               'us': e_username.get(),
                               'id': id,
                           })
            conn.commit()

            cursor.execute("""SELECT strftime('%d/%m/%Y','now')"""
                           )
            date = cursor.fetchone()[0]
            cursor.execute("""insert into user_details values(:id,:fn,:ln,:dn,:sn,:c,:date)""",
                           {
                               'id': id,
                               'fn': e_fname.get(),
                               'ln': e_lname.get(),
                               'dn': e_doorno.get(),
                               'sn': e_street.get(),
                               'c': e_city.get(),
                               'date': date
                           })
            conn.commit()

            cursor.execute("""insert into user_contact(user_id,phno) values(:id,:pn)""",
                           {
                               'pn': e_phone.get(),
                               'id': id,
                           })
            conn.commit()
            e_username.delete(0, END)
            e_password.delete(0, END)
            e_cpassword.delete(0, END)
            e_street.delete(0, END)
            e_lname.delete(0, END)
            e_fname.delete(0, END)
            e_phone.delete(0, END)
            e_city.delete(0, END)
            e_doorno.delete(0, END)

        elif e_password.get() != e_cpassword.get() and e_password.get() != '':
            x = 2
        else:
            x = 3
    except:
        messagebox.askretrycancel(
            "Register", "Username already picked!")
        x = 0
        return
    if x == 1:
        messagebox.showinfo("Register", "Sucessfully Registered")
    elif x == 2:
        messagebox.askretrycancel(
            "Register", "Password not matching,Try again?")
    elif x == 3:
        messagebox.askretrycancel(
            "Register", "Please enter all details")


def register_window():
    global e_username, e_password, e_city, e_cpassword, e_doorno, e_fname, e_lname, e_phone, e_street
    window = Tk()
    window.title('Register')
    width = 507
    height = 466
    screenwidth = window.winfo_screenwidth()
    screenheight = window.winfo_screenheight()
    alignstr = '%dx%d+%d+%d' % (width, height,
                                (screenwidth - width) / 2, (screenheight - height) / 2)
    window.geometry(alignstr)
    window.resizable(width=False, height=False)

    l_reg = LabelFrame(window, text="Fill all details", width=200)
    l_reg.place(x=50, y=30)

    submitbtn = Button(window, text="Submit",
                       command=submit, height=5, width=10)
    submitbtn.place(x=400, y=200)

    l_username = Label(l_reg, text="Username")
    l_username.grid(row=0, column=0, padx=10, pady=10)

    l_password = Label(l_reg, text="Password")
    l_password.grid(row=1, column=0, padx=10, pady=10)

    l_cpassword = Label(l_reg, text="Confirm Password")
    l_cpassword.grid(row=2, column=0, padx=10, pady=10)

    l_fname = Label(l_reg, text="First Name")
    l_fname.grid(row=3, column=0, padx=10, pady=10)

    l_lname = Label(l_reg, text="Last Name")
    l_lname.grid(row=4, column=0, padx=10, pady=10)

    l_doorno = Label(l_reg, text="Door No")
    l_doorno.grid(row=5, column=0, padx=10, pady=10)

    l_street = Label(l_reg, text="Street Name")
    l_street.grid(row=6, column=0, padx=10, pady=10)

    l_city = Label(l_reg, text="City")
    l_city.grid(row=7, column=0, padx=10, pady=10)

    l_phone = Label(l_reg, text="Phone Number")
    l_phone.grid(row=8, column=0, padx=10, pady=10)

    e_username = Entry(l_reg)
    e_username.grid(row=0, column=1, padx=10, pady=10)

    e_password = Entry(l_reg, show="*")
    e_password.grid(row=1, column=1, padx=10, pady=10)

    e_cpassword = Entry(l_reg, show="*")
    e_cpassword.grid(row=2, column=1, padx=10, pady=10)

    e_fname = Entry(l_reg)
    e_fname.grid(row=3, column=1, padx=10, pady=10)

    e_lname = Entry(l_reg)
    e_lname.grid(row=4, column=1, padx=10, pady=10)

    e_doorno = Entry(l_reg)
    e_doorno.grid(row=5, column=1, padx=10, pady=10)

    e_street = Entry(l_reg)
    e_street.grid(row=6, column=1, padx=10, pady=10)

    e_city = Entry(l_reg)
    e_city.grid(row=7, column=1, padx=10, pady=10)

    e_phone = Entry(l_reg)
    e_phone.grid(row=8, column=1, padx=10, pady=10)

    window.mainloop()
