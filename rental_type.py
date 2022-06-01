from tkinter import *
from tkinter import ttk
import sqlite3
from tkinter import messagebox


def view_rental_type():
    root = Tk()
    root.geometry("700x600")
    root.title("View Rental Packages")
    conn = sqlite3.connect('car_rental.db')
    cursor = conn.cursor()

    def query_database():
        conn = sqlite3.connect('car_rental.db')
        cursor = conn.cursor()
        for record in my_tree.get_children():
            my_tree.delete(record)
        data = []
        cursor.execute("select * from rental_type")
        for i in cursor:
            data.append(list(i))
        for record in data:
            my_tree.insert(parent='', index='end',
                           text="", values=(record[0], record[1], record[2]))

    my_menu = Menu(root)
    root.config(menu=my_menu)
# search menu
    search_menu = Menu(my_menu, tearoff=0)
    my_menu.add_cascade(label="Options", menu=search_menu)
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

    tree_frame = Frame(root)
    tree_frame.pack(pady=20)

    tree_scroll = Scrollbar(tree_frame)
    tree_scroll.pack(side=RIGHT, fill=Y)

    my_tree = ttk.Treeview(tree_frame, yscrollcommand=tree_scroll)
    my_tree.pack(pady=20)

    tree_scroll.config(command=my_tree.yview)

    my_tree['columns'] = ("Rental type", "Base price", "Tariff")

    my_tree.column("#0", width=0, stretch=NO)
    my_tree.column("Rental type", anchor=W, width=90, minwidth=70)
    my_tree.column("Base price", anchor=CENTER, width=200, minwidth=170)
    my_tree.column("Tariff", anchor=CENTER, width=90, minwidth=70)

    my_tree.heading("#0", text="", anchor=W)
    my_tree.heading("Rental type", text="RENTAL TYPE", anchor=W)
    my_tree.heading("Base price", text="BASE PRICE", anchor=CENTER)
    my_tree.heading("Tariff", text="TARIFF", anchor=CENTER)

    add_frame = Frame(root)
    add_frame.pack(pady=5)

    l_type = Label(add_frame, text="RENTAL TYPE")
    l_type.grid(row=0, column=0)

    l_price = Label(add_frame, text="BASE PRICE")
    l_price.grid(row=0, column=1)

    l_tariff = Label(add_frame, text="TARIFF")
    l_tariff.grid(row=0, column=2)

    e_type = Entry(add_frame)
    e_type.grid(row=1, column=0)

    e_price = Entry(add_frame)
    e_price.grid(row=1, column=1)

    e_tariff = Entry(add_frame)
    e_tariff.grid(row=1, column=2)

    def select_record(e):
        global o_type, o_price, o_tariff  # initial values will be stored here
        e_type.delete(0, END)
        e_price.delete(0, END)
        e_tariff.delete(0, END)
        selected = my_tree.focus()
        values = my_tree.item(selected, 'values')
        if values is not None:
            e_type.insert(0, values[0])
            e_price.insert(0, values[1])
            e_tariff.insert(0, values[2])
        o_type = e_type.get()
        o_price = e_price.get()
        o_tariff = e_tariff.get()

    def update_record():  # update in main table and related tables
        global o_type, o_price, o_tariff
        selected = my_tree.focus()
        if e_type.get() and e_price.get() and e_tariff.get() is not None:
            values = my_tree.item(
                selected, text="", values=(e_type.get(), e_price.get(), e_tariff.get()))
        cursor = conn.cursor()
        if e_type.get() == o_type:

            cursor.execute("""update rental_type set rental_type=:r_type,base_price=:r_price,tariff = :r_tariff where rental_type=:o_type""",
                           {
                               'o_type': o_type,
                               'r_type': e_type.get(),
                               'r_price': e_price.get(),
                               'r_tariff': e_tariff.get()
                           })
            conn.commit()
        else:
            try:
                cursor.execute("""update car set rental_type=:r_type where rental_type=:o_type""",
                               {
                                   'o_type': o_type,
                                   'r_type': e_type.get(),
                               })
                conn.commit()

                cursor.execute("""update rental_type set rental_type=:r_type,base_price=:r_price,tariff = :r_tariff where rental_type=:o_type""",
                               {
                                   'o_type': o_type,
                                   'r_type': e_type.get(),
                                   'r_price': e_price.get(),
                                   'r_tariff': e_tariff.get()
                               })
                conn.commit()
            except:
                messagebox.showerror("IntegrityError",
                                     "Rental Id must be unique!!")
        e_type.delete(0, END)
        e_price.delete(0, END)
        e_tariff.delete(0, END)

    def add_record():  # dont need to add in any other table

        if e_type.get() and e_price.get() and e_tariff.get() is not None:
            my_tree.insert(parent='', index='end',
                           text="", values=(e_type.get(), e_price.get(), e_tariff.get()))
        try:
            cursor.execute("""insert into rental_type values(:r_type,:r_price,:r_tariff) """,
                           {
                               'r_type': e_type.get(),
                               'r_price': e_price.get(),
                               'r_tariff': e_tariff.get()
                           })
            conn.commit()
        except:
            messagebox.showerror("IntegrityError",
                                 "Rental Id must be unique!!")

        e_type.delete(0, END)
        e_price.delete(0, END)
        e_tariff.delete(0, END)

    def del_record():
        x = my_tree.selection()[0]
        my_tree.delete(x)
        cursor.execute(
            "select rental_type from rental_type where rental_type = (select min(rental_type) from rental_type)")
        min_type = cursor.fetchone()[0]
        cursor.execute("""update car set rental_type=:min_type where rental_type=:o_type""",
                       {
                           'o_type': o_type,
                           'min_type': min_type,
                       })
        conn.commit()

        cursor.execute("""delete from rental_type where rental_type = :r_type""",
                       {
                           'r_type': e_type.get()
                       })
        conn.commit()
        e_type.delete(0, END)
        e_price.delete(0, END)
        e_tariff.delete(0, END)

    button_frame = LabelFrame(root, text="Commands", width=80)
    button_frame.pack(expand="yes", padx=20)

    update_rec = Button(button_frame, text="Save record",
                        command=update_record)
    update_rec.grid(row=0, column=1, padx=10, pady=10)

    add_rec = Button(button_frame, text="Add record", command=add_record)
    add_rec.grid(row=0, column=2, padx=10, pady=10)

    del_rec = Button(button_frame, text="Delete selected record",
                     command=del_record)
    del_rec.grid(row=0, column=3, padx=10, pady=10)

    my_tree.bind("<ButtonRelease-1>", select_record)

    query_database()
    root.mainloop()
    conn.close()
