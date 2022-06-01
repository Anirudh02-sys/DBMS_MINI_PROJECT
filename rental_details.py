from tkinter import *
from tkinter import ttk
import sqlite3
from tkinter import messagebox


def view_rental_details():
    window = Tk()
    window.geometry("1100x400")
    window.title("Rented Cars")
    conn = sqlite3.connect('car_rental.db')
    cursor = conn.cursor()

    def query_database():
        conn = sqlite3.connect('car_rental.db')
        cursor = conn.cursor()
        for record in my_tree.get_children():
            my_tree.delete(record)
        data = []
        cursor.execute("""select * from rental""")
        for i in cursor:
            data.append(list(i))
        for record in data:
            my_tree.insert(parent='', index='end',
                           text="", values=(record[0], record[1], record[2], record[3], record[4], record[5], record[6]))

    my_menu = Menu(window)
    window.config(menu=my_menu)
# search menu
    search_menu = Menu(my_menu, tearoff=0)
    my_menu.add_cascade(label="Search", menu=search_menu)
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

    my_tree['columns'] = ("rental_id", "reg_no", "user_id", "book_time", "rental_date",
                          "rental_hours", "amount")

    my_tree.column("#0", width=0, stretch=NO)
    my_tree.column("rental_id", anchor=CENTER, width=140, minwidth=70)
    my_tree.column("reg_no", anchor=CENTER, width=130, minwidth=170)
    my_tree.column("user_id", anchor=CENTER, width=90, minwidth=70)
    my_tree.column("book_time", anchor=CENTER, width=200, minwidth=170)
    my_tree.column("rental_date", anchor=CENTER, width=90, minwidth=70)
    my_tree.column("rental_hours", anchor=CENTER, width=200, minwidth=170)
    my_tree.column("amount", anchor=CENTER, width=200, minwidth=170)

    my_tree.heading("#0", text="", anchor=W)
    my_tree.heading("rental_id", anchor=CENTER, text="RENTAL ID")
    my_tree.heading("reg_no", anchor=CENTER, text="REGISTRATION NUMBER")
    my_tree.heading("user_id", anchor=CENTER, text="USER ID")
    my_tree.heading("book_time", anchor=CENTER, text="BOOK TIME")
    my_tree.heading("rental_date", anchor=CENTER, text="RENTAL DATE")
    my_tree.heading("rental_hours", anchor=CENTER, text="RENTAL HOURS")
    my_tree.heading("amount", anchor=CENTER, text="AMOUNT")

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
