from tkinter import *
from tkinter import ttk
import sqlite3
from tkinter import messagebox


def view_model_details():
    root = Tk()
    root.geometry("700x600")
    root.title("View Model Details")
    conn = sqlite3.connect('car_rental.db')
    cursor = conn.cursor()

    def query_database():
        conn = sqlite3.connect('car_rental.db')
        cursor = conn.cursor()
        for record in my_tree.get_children():
            my_tree.delete(record)
        data = []
        cursor.execute("select * from car")
        for i in cursor:
            data.append(list(i))
        for record in data:
            my_tree.insert(parent='', index='end',
                           text="", values=(record[0], record[1], record[2], record[3]))

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

    my_tree['columns'] = ("car_id", "model_name", "agency_id", "rental_type")

    my_tree.column("#0", width=0, stretch=NO)
    my_tree.column("car_id", anchor=W, width=90, minwidth=70)
    my_tree.column("model_name", anchor=CENTER, width=200, minwidth=170)
    my_tree.column("agency_id", anchor=CENTER, width=90, minwidth=70)
    my_tree.column("rental_type", anchor=CENTER, width=90, minwidth=70)

    my_tree.heading("#0", text="", anchor=W)
    my_tree.heading("car_id", text="CAR ID", anchor=W)
    my_tree.heading("model_name", text="MODEL NAME", anchor=CENTER)
    my_tree.heading("agency_id", text="AGENCY ID", anchor=CENTER)
    my_tree.heading("rental_type", text="RENTAL TYPE", anchor=CENTER)

    add_frame = Frame(root)
    add_frame.pack(pady=5)

    l_car = Label(add_frame, text="CAR ID")
    l_car.grid(row=0, column=0)

    l_model = Label(add_frame, text="MODEL NAME")
    l_model.grid(row=0, column=1)

    l_agency = Label(add_frame, text="AGENCY ID")
    l_agency.grid(row=0, column=2)

    l_type = Label(add_frame, text="RENTAL TYPE")
    l_type.grid(row=0, column=3)

    e_car = Entry(add_frame)
    e_car.grid(row=1, column=0)

    e_model = Entry(add_frame)
    e_model.grid(row=1, column=1)

    e_agency = Entry(add_frame)
    e_agency.grid(row=1, column=2)

    e_type = Entry(add_frame)
    e_type.grid(row=1, column=3)

    def select_record(e):
        global o_car, o_model, o_agency, o_type  # initial values will be stored here
        e_type.delete(0, END)
        e_car.delete(0, END)
        e_model.delete(0, END)
        e_agency.delete(0, END)

        selected = my_tree.focus()
        values = my_tree.item(selected, 'values')
        if values is not None:
            e_car.insert(0, values[0])
            e_model.insert(0, values[1])
            e_agency.insert(0, values[2])
            e_type.insert(0, values[3])

        o_car = e_car.get()
        o_model = e_model.get()
        o_agency = e_agency.get()
        o_type = e_type.get()

    def update_record():  # update in main table and related tables
        global o_car, o_model, o_agency, o_type
        rental_types = []
        agency_ids = []
        selected = my_tree.focus()
        if e_type.get() is not None and e_model.get() is not None and e_car.get() is not None and e_type.get() is not None:
            values = my_tree.item(
                selected, text="", values=(e_car.get(), e_model.get(), e_agency.get(), e_type.get()))
        cursor = conn.cursor()
        cursor.execute("select rental_type from rental_type")
        for i in cursor.fetchall():
            rental_types.append(i[0])
        cursor.execute("select agency_id from agency")
        for i in cursor.fetchall():
            agency_ids.append(i[0])

        if (int(e_agency.get()) in agency_ids) and (int(e_type.get()) in rental_types):
            if e_car.get() == o_car:
                print("yess")
                cursor.execute("""update car set car_id=:m_id, model_name =:m_name,agency_id = :a_id,rental_type = :r_type where car_id = :o_car""",
                               {
                                   'm_id': e_car.get(),
                                   'm_name': e_model.get(),
                                   'a_id': e_agency.get(),
                                   'r_type': e_type.get(),
                                   'o_car': o_car
                               })
                conn.commit()
            else:
                try:
                    cursor.execute("""update car_details set car_id=:m_id where car_id = :o_car""",
                                   {
                                       'o_car': o_car,
                                       'm_id': e_car.get()
                                   })
                    conn.commit()

                    cursor.execute("""update car set car_id=:m_id, model_name =:m_name,agency_id = :a_id,rental_type = :r_type where car_id = :o_car""",
                                   {
                                       'm_id': e_car.get(),
                                       'm_name': e_model.get(),
                                       'a_id': e_agency.get(),
                                       'r_type': e_type.get(),
                                       'o_car': o_car
                                   })
                    conn.commit()
                except:
                    messagebox.showerror("IntegrityError",
                                         "Car Id must be unique!!")

            conn.commit()
            e_type.delete(0, END)
            e_car.delete(0, END)
            e_model.delete(0, END)
            e_agency.delete(0, END)

        else:
            messagebox.askretrycancel(
                "Error", "Please ensure integrity is maintained!!!")

    def add_record():  # dont need to add in any other table
        rental_types = []
        agency_ids = []
        cursor.execute("select rental_type from rental_type")
        for i in cursor.fetchall():
            rental_types.append(i)
        cursor.execute("select agency_id from agency")
        for i in cursor.fetchall():
            agency_ids.append(i)
        if e_type.get() is not None and e_model.get() is not None and e_car.get() is not None and e_type.get() is not None:
            my_tree.insert(parent='', index='end',
                           text="", values=(e_car.get(), e_model.get(), e_agency.get(), e_type.get()))
        if (e_agency.get() in agency_ids) and (e_type.get() in rental_types):
            try:
                cursor.execute("""insert into car values(:m_id,:m_name,:a_id,:r_type) """,
                               {
                                   'm_id': e_car.get(),
                                   'm_name': e_model.get(),
                                   'a_id': e_agency.get(),
                                   'r_type': e_type.get()
                               })
                conn.commit()
                e_type.delete(0, END)
                e_car.delete(0, END)
                e_model.delete(0, END)
                e_agency.delete(0, END)
            except:
                messagebox.showerror("IntegrityError",
                                     "Car Id must be unique!!")

        else:
            messagebox.askretrycancel(
                "Error", "Please ensure integrity is maintained!!!")

    def del_record():
        x = my_tree.selection()[0]
        my_tree.delete(x)
        cursor.execute("""delete from rental where  car_id = :m_id""",
                       {
                           'm_id': e_car.get()
                       })
        conn.commit()

        cursor.execute("""delete from car_details where car_id = :m_id""",
                       {
                           'm_id': e_car.get()
                       })
        conn.commit()

        cursor.execute("""delete from car where car_id = :m_id""",
                       {
                           'm_id': e_car.get()
                       })
        conn.commit()
        e_type.delete(0, END)
        e_car.delete(0, END)
        e_model.delete(0, END)
        e_agency.delete(0, END)

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
