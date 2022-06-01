from tkinter import *
from tkinter import ttk
import sqlite3
from tkinter import messagebox


def view_car_details():
    root = Tk()
    root.geometry("900x600")
    root.title("View Car Details")
    conn = sqlite3.connect('car_rental.db')
    cursor = conn.cursor()

    def query_database():
        conn = sqlite3.connect('car_rental.db')
        cursor = conn.cursor()
        for record in my_tree.get_children():
            my_tree.delete(record)
        data = []
        cursor.execute("select * from car_details")
        for i in cursor:
            data.append(list(i))
        for record in data:
            my_tree.insert(parent='', index='end',
                           text="", values=(record[0], record[1], record[2], record[3], record[4], record[5]))

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

    tree_scroll = Scrollbar(tree_frame, orient=VERTICAL)
    tree_scroll.pack(side=RIGHT, fill=Y)
    tree_scroll1 = Scrollbar(tree_frame, orient=HORIZONTAL)
    tree_scroll1.pack(side=BOTTOM, fill=X)

    my_tree = ttk.Treeview(
        tree_frame, yscrollcommand=tree_scroll, xscrollcommand=tree_scroll1)
    my_tree.pack(pady=20)

    tree_scroll.config(command=my_tree.yview)
    tree_scroll1.config(command=my_tree.xview)

    my_tree['columns'] = ("reg_no", "car_id", "seats",
                          "automatic", "colour", "rental_status")

    my_tree.column("#0", width=0, stretch=NO)
    my_tree.column("reg_no", anchor=CENTER, width=140, minwidth=70)
    my_tree.column("car_id", anchor=CENTER, width=130, minwidth=170)
    my_tree.column("seats", anchor=CENTER, width=90, minwidth=70)
    my_tree.column("automatic", anchor=CENTER, width=200, minwidth=170)
    my_tree.column("colour", anchor=CENTER, width=90, minwidth=70)
    my_tree.column("rental_status", anchor=CENTER, width=200, minwidth=170)

    my_tree.heading("#0", text="", anchor=W)
    my_tree.heading("reg_no", text="REGISTRATION NUMBER", anchor=W)
    my_tree.heading("car_id", text="CAR ID", anchor=CENTER)
    my_tree.heading("seats", text="SEATS", anchor=W)
    my_tree.heading("automatic", text="AUTOMATIC(YES/NO)", anchor=W)
    my_tree.heading("colour", text="COLOUR", anchor=CENTER)
    my_tree.heading("rental_status", text="RENTAL STATUS", anchor=CENTER)

    add_frame = Frame(root)
    add_frame.pack(pady=5)

    l_reg = Label(add_frame, text="REGISTRATION NUMBER")
    l_reg.grid(row=0, column=0)

    l_cid = Label(add_frame, text="CAR ID")
    l_cid.grid(row=0, column=1)

    l_seats = Label(add_frame, text="SEATS")
    l_seats.grid(row=0, column=2)

    l_automatic = Label(add_frame, text="AUTOMATIC(YES/NO)")
    l_automatic.grid(row=0, column=3)

    l_colour = Label(add_frame, text="COLOUR")
    l_colour.grid(row=0, column=4)

    e_reg = Entry(add_frame, width=25)
    e_reg.grid(row=1, column=0)

    e_cid = Entry(add_frame)
    e_cid.grid(row=1, column=1)

    e_seats = Entry(add_frame)
    e_seats.grid(row=1, column=2)

    e_automatic = Entry(add_frame)
    e_automatic.grid(row=1, column=3)

    e_colour = Entry(add_frame)
    e_colour.grid(row=1, column=4)

    def select_record(e):
        # initial values will be stored here
        global o_reg, o_cid, o_seats, o_automatic, o_colour, rental_stat
        e_reg.delete(0, END)
        e_cid.delete(0, END)
        e_seats.delete(0, END)
        e_automatic.delete(0, END)
        e_colour.delete(0, END)

        selected = my_tree.focus()
        values = my_tree.item(selected, 'values')
        if values is not None:
            e_reg.insert(0, values[0])
            e_cid.insert(0, values[1])
            e_seats.insert(0, values[2])
            e_automatic.insert(0, values[3])
            e_colour.insert(0, values[4])
            rental_stat = values[5]
            print(rental_stat)

        o_reg = e_reg.get()
        o_cid = e_cid.get()
        o_seats = e_seats.get()
        o_automatic = e_automatic.get()
        o_colour = e_colour.get()

    def update_record():  # update in main table and related tables
        global o_reg, o_cid, o_seats, o_automatic, o_colour, rental_stat
        car_ids = []
        selected = my_tree.focus()
        if e_reg.get() is not None and e_cid.get() is not None and e_seats.get() is not None and e_automatic.get() is not None and e_colour.get() is not None:
            values = my_tree.item(
                selected, text="", values=(e_reg.get(), e_cid.get(), e_seats.get(), e_automatic.get(), e_colour.get()))
        cursor = conn.cursor()
        cursor.execute("select car_id from car")
        for i in cursor.fetchall():
            car_ids.append(i[0])

        if (int(e_cid.get()) in car_ids):
            if e_reg.get() == o_reg:
                cursor.execute("""update car_details set car_id=:m_id,seats = :seat,automatic = :auto,colour = :colour where reg_no = :o_reg""",
                               {
                                   'm_id': e_cid.get(),
                                   'seat': e_seats.get(),
                                   'auto': e_automatic.get(),
                                   'colour': e_colour.get(),
                                   'o_reg': o_reg
                               })
                conn.commit()
            else:
                try:
                    cursor.execute("""update rental set reg_no=:rno where reg_no = :o_reg""",
                                   {
                                       'rno': e_reg.get(),
                                       'o_reg': o_reg
                                   })
                    conn.commit()
                    cursor.execute("""update car_details set reg_no=:rno,car_id=:m_id,seats = :seat,automatic = :auto,colour = :colour where reg_no = :o_reg""",
                                   {
                                       'rno': e_reg.get(),
                                       'm_id': e_cid.get(),
                                       'seat': e_seats.get(),
                                       'auto': e_automatic.get(),
                                       'colour': e_colour.get(),
                                       'o_reg': o_reg
                                   })
                    conn.commit()
                except:
                    messagebox.showerror("IntegrityError",
                                         "Registration Number must be unique!!")

            conn.commit()
            e_reg.delete(0, END)
            e_cid.delete(0, END)
            e_seats.delete(0, END)
            e_automatic.delete(0, END)
            e_colour.delete(0, END)

        else:
            messagebox.askretrycancel(
                "Error", "Please ensure integrity is maintained!!!")

    def add_record():  # dont need to add in any other table
        global o_reg, o_cid, o_seats, o_automatic, o_colour
        car_ids = []
        reg_nos = []
        selected = my_tree.focus()
        cursor.execute("select car_id from car")
        for i in cursor.fetchall():
            car_ids.append(i[0])

        if e_reg.get() is not None and e_cid.get() is not None and e_seats.get() is not None and e_automatic.get() is not None and e_colour.get() is not None:
            values = my_tree.item(
                selected, text="", values=(e_reg.get(), e_cid.get(), e_seats.get(), e_automatic.get(), e_colour.get()))

        cursor.execute("select reg_no from car_details")
        for i in cursor.fetchall():
            reg_nos.append(i[0])

        if (int(e_cid.get()) in car_ids) and (int(e_reg.get()) not in reg_nos):
            cursor.execute("""insert into car_details(reg_no,car_id,seats,automatic,colour,rental_status) values(:rno,:m_id,:seat,:auto,:colour,:msg) """,
                           {
                               'rno': e_reg.get(),
                               'm_id': e_cid.get(),
                               'seat': e_seats.get(),
                               'auto': e_automatic.get(),
                               'colour': e_colour.get(),
                               'msg': 'No'

                           })
            conn.commit()

            e_reg.delete(0, END)
            e_cid.delete(0, END)
            e_seats.delete(0, END)
            e_automatic.delete(0, END)
            e_colour.delete(0, END)
        else:
            messagebox.askretrycancel(
                "Error", "Please ensure integrity is maintained!!!")

    def del_record():
        x = my_tree.selection()[0]
        my_tree.delete(x)
        cursor.execute("""delete from rental where  reg_no = :rno""",
                       {
                           'rno': e_reg.get()
                       })
        conn.commit()

        cursor.execute("""delete from car_details where reg_no = :rno""",
                       {
                           'rno': e_reg.get()
                       })
        conn.commit()

        conn.commit()
        e_reg.delete(0, END)
        e_cid.delete(0, END)
        e_seats.delete(0, END)
        e_automatic.delete(0, END)
        e_colour.delete(0, END)

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
