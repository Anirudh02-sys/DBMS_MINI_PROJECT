import tkinter
import tkinter.font as tkFont
from typing import Sized
import sqlite3
from tkinter import *
from PIL import ImageTk, Image
from tkinter import messagebox
from admin import admin_view
from register import register_window
from user_page import user_menu

conn = sqlite3.connect('car_rental.db')
cursor = conn.cursor()


def submit1():
    us = e_username.get()
    p = e_pass.get()
    a = e_admin.get()
    if a:
        cursor.execute("""Select * from login where username=:us and password=:p and admin_pin=:a""",
                       {
                           'us': us,
                           'p': p,
                           'a': a
                       })
        row = cursor.fetchone()
        if row:
            page.destroy()
            admin_view()
        else:
            messagebox.askretrycancel(
                "Login", "Please enter correct details")
    else:
        cursor.execute("""Select username,password from login where username=:us and password=:p""",
                       {
                           'us': us,
                           'p': p,
                       })
        row = cursor.fetchone()
        if row:
            page.destroy()
            cursor.execute("""Select user_id from user where username=:us""",
                           {
                               'us': us,
                           })
            uid = cursor.fetchone()[0]
            user_menu(uid)
        else:
            messagebox.askretrycancel(
                "Login", "Please enter correct details")


def user_login_window():
    global e_username, e_pass, e_admin, page
    page = Toplevel(root)
    page.title('Login')
    # setting window size
    width = 507
    height = 466
    screenwidth = page.winfo_screenwidth()
    screenheight = page.winfo_screenheight()
    alignstr = '%dx%d+%d+%d' % (width, height,
                                (screenwidth - width) / 2, (screenheight - height) / 2)
    page.geometry(alignstr)
    page.resizable(width=False, height=False)

    l_username = Label(page, text="Username")
    l_username.place(x=110, y=90, width=70, height=25)

    l_pass = Label(page, text="Password")
    l_pass.place(x=110, y=170, width=70, height=25)

    l_admin = Label(page, text="Admin Pin")
    l_admin.place(x=110, y=250, width=70, height=25)

    e_username = Entry(page, width=35)
    e_username.place(x=280, y=90, width=70, height=25)

    e_pass = Entry(page, width=35, show="*")
    e_pass.place(x=280, y=170, width=70, height=25)

    e_admin = Entry(page, width=35, show="*")
    e_admin.place(x=280, y=250, width=70, height=25)

    submitbtn = Button(page, text="Submit", bg="White",
                       command=submit1)
    submitbtn.place(x=280, y=320, width=70, height=25)


def register_open():
    register_window()


root = Tk()
root.title("Car Rental Services")
global img
canvas1 = Canvas(root, width=400, height=400)

canvas1.pack(fill="both", expand=True)
image = Image.open(
    r"C:\Users\91950\OneDrive\Documents\DBMS_MINI_PROJECT\jammu-kashmir-car-rental.jpg")
image = image.resize((898, 602), Image.ANTIALIAS)
img = ImageTk.PhotoImage(image)
canvas1.create_image(0, 0, image=img,
                     anchor="nw")

canvas1.create_text(
    455, 80, text="AAA CAR RENTAL SERVICES", font=("Helvetica Neue", 40, 'italic'), fill="cadet blue")

width = 898
height = 602
screenwidth = root.winfo_screenwidth()
screenheight = root.winfo_screenheight()
alignstr = '%dx%d+%d+%d' % (width, height,
                            (screenwidth - width) / 2, (screenheight - height) / 2)
root.geometry(alignstr)
root.resizable(width=False, height=False)
# create button that will be placed
button = Button(root, text="Login", bg='White', fg='Black',
                command=user_login_window)

button.place(x=360, y=240, width=100, height=35)
button = Button(root, text="Register", bg='White', fg='Black',
                command=register_open)
button.place(x=360, y=200, width=100, height=35)

member_frame = LabelFrame(root, text="Team Members", width=30)
member_frame.pack(expand="yes", padx=30)

member_1 = Label(member_frame, text="Anirudh K")
member_1.grid(row=0, column=1, padx=10, pady=10)

member_2 = Label(member_frame, text="Antony R")
member_2.grid(row=0, column=2, padx=10, pady=10)

member_3 = Label(member_frame, text="Aravind Allagapan")
member_3.grid(row=0, column=3, padx=10, pady=10)

root.mainloop()
