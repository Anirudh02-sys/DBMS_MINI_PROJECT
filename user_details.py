from tkinter import *
from tkinter import ttk
import sqlite3
from tkinter import messagebox


def view_user_details():
    window = Tk()
    window.geometry("1100x400")
    window.title("Current Users")
    conn = sqlite3.connect('car_rental.db')
    cursor = conn.cursor()

    def query_database():
        conn = sqlite3.connect('car_rental.db')
        cursor = conn.cursor()
        for record in my_tree.get_children():
            my_tree.delete(record)
        data = []
        cursor.execute("""select u.user_id,username,fname,lname,door_no,street_name,city,phno,reg_date from user as u,user_details as ud,user_contact as uc where u.user_id=ud.user_id and u.user_id=uc.user_id and uc.user_id=ud.user_id;""")
        for i in cursor:
            data.append(list(i))
        for record in data:
            my_tree.insert(parent='', index='end',
                           text="", values=(record[0], record[1], record[2], record[3], record[4], record[5], record[6], record[7], record[8]))

    def search_records():
        lookup_record = search_entry.get()
        search.destroy()
        for record in my_tree.get_children():
            my_tree.delete(record)
        data = []
        cursor.execute(
            "select u.user_id,username,fname,lname,door_no,street_name,city,phno,reg_date from user as u,user_details as ud,user_contact as uc where u.user_id=ud.user_id and u.user_id=uc.user_id and uc.user_id=ud.user_id and ud.fname like ?", (lookup_record,))
        for i in cursor:
            data.append(list(i))
        for record in data:
            my_tree.insert(parent='', index='end',
                           text="", values=(record[0], record[1], record[2], record[3], record[4], record[5], record[6], record[7], record[8]))

    def lookup():
        global search_entry, search
        search = Toplevel(window)
        search.title("Lookup Records")
        search.geometry("400x200")

        search_frame = LabelFrame(search, text="First Name")
        search_frame.pack(padx=10, pady=10)

        search_entry = Entry(search_frame, font=("Helvetica", 18))
        search_entry.pack(pady=20, padx=20)

        search_button = Button(search, text="Search Records",
                               command=search_records)
        search_button.pack(pady=20, padx=20)

    my_menu = Menu(window)
    window.config(menu=my_menu)
# search menu
    search_menu = Menu(my_menu, tearoff=0)
    my_menu.add_cascade(label="Search", menu=search_menu)
    search_menu.add_command(label="Search", command=lookup)
    search_menu.add_separator()
    search_menu.add_command(label="Reset", command=query_database)


# add style
    style = ttk.Style()
# picking a theme
    style.theme_use('default')
# config the treeview colors
    style.configure("Treeview", background="#D3D3D3",
                    foreground="black", rowheight=25, fieldbackground="#D3D3D3")
# change selected color
    style.map('Treeview', background=[('selected', "#347083")])

    tree_frame = Frame(window)
    tree_frame.pack(pady=20)

    tree_scroll = Scrollbar(tree_frame, orient=VERTICAL)
    tree_scroll.pack(side=RIGHT, fill=Y)
    tree_scroll1 = Scrollbar(tree_frame, orient=HORIZONTAL)
    tree_scroll1.pack(side=BOTTOM, fill=X)

    my_tree = ttk.Treeview(
        tree_frame, yscrollcommand=tree_scroll, xscrollcommand=tree_scroll1)
    my_tree.pack(pady=20)

    tree_scroll.config(command=my_tree.yview)
    tree_scroll1.config(command=my_tree.xview)

    my_tree['columns'] = ("user_id", "username", "fname",
                          "lname", "door_no", "street_no", "city", "phno", "reg_date")

    my_tree.column("#0", width=0, stretch=NO)
    my_tree.column("user_id", anchor=CENTER, width=140, minwidth=70)
    my_tree.column("username", anchor=CENTER, width=130, minwidth=170)
    my_tree.column("fname", anchor=CENTER, width=90, minwidth=70)
    my_tree.column("lname", anchor=CENTER, width=200, minwidth=170)
    my_tree.column("door_no", anchor=CENTER, width=90, minwidth=70)
    my_tree.column("street_no", anchor=CENTER, width=200, minwidth=170)
    my_tree.column("city", anchor=CENTER, width=90, minwidth=70)
    my_tree.column("phno", anchor=CENTER, width=200, minwidth=170)
    my_tree.column("reg_date", anchor=CENTER, width=200, minwidth=100)

    my_tree.heading("#0", text="", anchor=W)
    my_tree.heading("user_id", anchor=CENTER, text="USER ID")
    my_tree.heading("username", anchor=CENTER, text="USERNAME")
    my_tree.heading("fname", anchor=CENTER, text="FIRST NAME")
    my_tree.heading("lname", anchor=CENTER, text="LAST NAME")
    my_tree.heading("door_no", anchor=CENTER, text="DOOR NUMBER")
    my_tree.heading("street_no", anchor=CENTER, text="STREET NUMBER")
    my_tree.heading("city", anchor=CENTER, text="CITY")
    my_tree.heading("phno", anchor=CENTER, text="PHONE NUMBER")
    my_tree.heading("reg_date", anchor=CENTER, text="REGISTRATION DATE")

    def select_record(e):
        selected = my_tree.focus()
        values = my_tree.item(selected, 'values')

    def exit_page():
        window.destroy()

    exitbtn = Button(window, text="Exit", command=exit_page)
    exitbtn.pack(pady=20)

    my_tree.bind("<ButtonRelease-1>", select_record)

    query_database()
    window.mainloop()
    conn.close()
