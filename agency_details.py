from tkinter import *
from tkinter import ttk
import sqlite3
from tkinter import messagebox


def view_agent_details():
    root = Tk()
    root.geometry("700x600")
    root.title("Agent Details")
    conn = sqlite3.connect('car_rental.db')
    cursor = conn.cursor()

    def query_database():
        conn = sqlite3.connect('car_rental.db')
        cursor = conn.cursor()
        for record in my_tree.get_children():
            my_tree.delete(record)
        data = []
        cursor.execute("select * from agency")
        for i in cursor:
            data.append(list(i))
        for record in data:
            my_tree.insert(parent='', index='end',
                           text="", values=(record[0], record[1]))

    def search_records():
        lookup_record = search_entry.get()
        search.destroy()
        for record in my_tree.get_children():
            my_tree.delete(record)
        data = []
        cursor.execute(
            "select * from agency where agency_name like ?", (lookup_record,))
        for i in cursor:
            data.append(list(i))
        for record in data:
            my_tree.insert(parent='', index='end',
                           text="", values=(record[0], record[1]))

    def lookup():
        global search_entry, search
        search = Toplevel(root)
        search.title("Lookup Records")
        search.geometry("400x200")

        search_frame = LabelFrame(search, text="Agency NAME")
        search_frame.pack(padx=10, pady=10)

        search_entry = Entry(search_frame, font=("Helvetica", 18))
        search_entry.pack(pady=20, padx=20)

        search_button = Button(search, text="Search Records",
                               command=search_records)
        search_button.pack(pady=20, padx=20)

    my_menu = Menu(root)
    root.config(menu=my_menu)
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

    tree_frame = Frame(root)
    tree_frame.pack(pady=20)

    tree_scroll = Scrollbar(tree_frame)
    tree_scroll.pack(side=RIGHT, fill=Y)

    my_tree = ttk.Treeview(tree_frame, yscrollcommand=tree_scroll)
    my_tree.pack(pady=20)

    tree_scroll.config(command=my_tree.yview)

    my_tree['columns'] = ("ID", "Name")

    my_tree.column("#0", width=0, stretch=NO)
    my_tree.column("ID", anchor=W, width=90, minwidth=70)
    my_tree.column("Name", anchor=CENTER, width=200, minwidth=170)
    my_tree.heading("#0", text="", anchor=W)
    my_tree.heading("ID", text="AGENCY ID", anchor=W)
    my_tree.heading("Name", text="AGENCY NAME", anchor=CENTER)

    add_frame = Frame(root)
    add_frame.pack(pady=5)

    l_id = Label(add_frame, text="AGENCY ID")
    l_id.grid(row=0, column=0)

    l_name = Label(add_frame, text="AGENCY NAME")
    l_name.grid(row=0, column=1)

    e_id = Entry(add_frame)
    e_id.grid(row=1, column=0)

    e_name = Entry(add_frame)
    e_name.grid(row=1, column=1)

    def select_record(e):
        global o_id, o_name  # initial values will be stored here
        e_id.delete(0, END)
        e_name.delete(0, END)
        selected = my_tree.focus()
        values = my_tree.item(selected, 'values')
        if values is not None:
            e_id.insert(0, values[0])
            e_name.insert(0, values[1])
        o_id = e_id.get()
        o_name = e_name.get()

    def update_record():  # update in main table and related tables
        global o_id, o_name
        selected = my_tree.focus()
        if e_id.get() and e_name.get() is not None:
            values = my_tree.item(
                selected, text="", values=(e_id.get(), e_name.get()))
        cursor = conn.cursor()
        if e_id.get() == o_id:
            cursor.execute("""update agency set agency_name=:a_name,agency_id=:a_id where agency_id=:o_id""",
                           {
                               'o_id': o_id,
                               'a_id': e_id.get(),
                               'a_name': e_name.get()
                           })
            conn.commit()
        else:
            try:
                cursor.execute("""update car set agency_id=:a_id where agency_id=:o_id""",
                               {
                                   'o_id': o_id,
                                   'a_id': e_id.get(),
                                   'a_name': e_name.get()
                               })
                conn.commit()
                cursor.execute("""update agency set agency_name=:a_name,agency_id=:a_id where agency_id=:o_id""",
                               {
                                   'o_id': o_id,
                                   'a_id': e_id.get(),
                                   'a_name': e_name.get()
                               })
                conn.commit()
            except:
                messagebox.showerror("IntegrityError",
                                     "Agency Id must be unique!!")

        e_id.delete(0, END)
        e_name.delete(0, END)

    def add_record():  # dont need to add in any other table

        if e_id.get() and e_name.get() is not None:
            my_tree.insert(parent='', index='end',
                           text="", values=(e_id.get(), e_name.get()))
        try:
            cursor.execute("""insert into agency values(:a_id,:a_name) """,
                           {
                               'a_id': e_id.get(),
                               'a_name': e_name.get()
                           })
            conn.commit()
        except:
            messagebox.showerror("IntegrityError",
                                 "Agency Id must be unique!!")

        e_id.delete(0, END)
        e_name.delete(0, END)

    def del_record():
        x = my_tree.selection()[0]
        my_tree.delete(x)
        cursor.execute("""delete from rental where reg_no in (select reg_no from car_details where car_id in (select car_id from car where agency_id=:a_id))""",
                       {
                           'a_id': o_id,
                       })
        conn.commit()
        cursor.execute("""delete from car_details where car_id in (select car_id from car where agency_id=:a_id)""",
                       {
                           'a_id': o_id,
                       })
        conn.commit()
        cursor.execute("""delete from car where agency_id=:a_id""",
                       {
                           'a_id': o_id,
                       })
        conn.commit()
        cursor.execute("""delete from agency where agency_id=:a_id""",
                       {
                           'a_id': o_id,
                       })
        conn.commit()
        e_id.delete(0, END)
        e_name.delete(0, END)

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
