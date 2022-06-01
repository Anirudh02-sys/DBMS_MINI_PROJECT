from tkinter import *
from tkinter import ttk
import sqlite3
from tkinter import messagebox


def user_menu(uid=None):
    page = Tk()
    page.geometry("1100x600")
    page.title("Available Cars")
    conn = sqlite3.connect('car_rental.db')
    cursor = conn.cursor()

    def query_database():
        global rent_btn
        conn = sqlite3.connect('car_rental.db')
        cursor = conn.cursor()
        for record in my_tree.get_children():
            my_tree.delete(record)
        data = []
        cursor.execute("""select reg_no,model_name,seats,automatic,colour,base_price,tariff from car_details as cd,car as c,rental_type as r where cd.car_id=c.car_id and c.rental_type = r.rental_type and cd.Rental_status = 'No'""")
        for i in cursor:
            data.append(list(i))
        for record in data:
            my_tree.insert(parent='', index='end',
                           text="", values=(record[0], record[1], record[2], record[3], record[4], record[5], record[6]))
        rent_btn = Button(page, text="Rent selected car",
                          command=rent_sub)
        rent_btn.pack(pady=20)

    my_menu = Menu(page)
    page.config(menu=my_menu)
# search menu


# add style
    style = ttk.Style()
# picking a theme
    style.theme_use('default')
# config the treeview colors
    style.configure("Treeview", background="#D3D3D3",
                    foreground="black", rowheight=25, fieldbackground="#D3D3D3")
# change selected color
    style.map('Treeview', background=[('selected', "#347083")])

    tree_frame = Frame(page)
    tree_frame.pack(pady=20)

    tree_scroll = Scrollbar(tree_frame)
    tree_scroll.pack(side=RIGHT, fill=Y)

    my_tree = ttk.Treeview(tree_frame, yscrollcommand=tree_scroll)
    my_tree.pack(pady=20)

    tree_scroll.config(command=my_tree.yview)

    my_tree['columns'] = ("reg_no", "model_name", "seats",
                          "automatic", "colour", "base_price", "tariff")

    my_tree.column("#0", width=0, stretch=NO)
    my_tree.column("reg_no", anchor=CENTER, width=140, minwidth=70)
    my_tree.column("model_name", anchor=CENTER, width=130, minwidth=170)
    my_tree.column("seats", anchor=CENTER, width=90, minwidth=70)
    my_tree.column("automatic", anchor=CENTER, width=200, minwidth=170)
    my_tree.column("colour", anchor=CENTER, width=90, minwidth=70)
    my_tree.column("base_price", anchor=CENTER, width=200, minwidth=170)
    my_tree.column("tariff", anchor=CENTER, width=90, minwidth=70)

    my_tree.heading("#0", text="", anchor=W)
    my_tree.heading("reg_no", text="REGISTRATION NUMBER", anchor=W)
    my_tree.heading("model_name", text="MODEL NAME", anchor=CENTER)
    my_tree.heading("seats", text="SEATS", anchor=W)
    my_tree.heading("automatic", text="AUTOMATIC(YES/NO)", anchor=W)
    my_tree.heading("colour", text="COLOUR", anchor=CENTER)
    my_tree.heading("base_price", text="BASE PRICE", anchor=CENTER)
    my_tree.heading("tariff", text="TARIFF", anchor=CENTER)

    def select_record(e):
        selected = my_tree.focus()
        values = my_tree.item(selected, 'values')

    def save(c1, time, amount):
        window.destroy()
        ltime.destroy()
        etime.destroy()
        confirm_btn.destroy()
        query_database()
        cursor.execute(
            'SELECT rental_id FROM rental WHERE rental_id=(SELECT max(rental_id) FROM rental);')
        id = cursor.fetchone()[0]
        id += 1
        cursor.execute("""SELECT strftime('%d/%m/%Y','now')"""
                       )
        date = cursor.fetchone()[0]
        cursor.execute("""SELECT strftime('%H:%M','now')"""
                       )
        time1 = cursor.fetchone()[0]

        cursor.execute("""insert into rental values(:r_id,:r_rno,:r_uid,:r_bt,:r_rd,:r_rh,:r_a) """, {
                       'r_id': id, 'r_rno': c1, 'r_uid': uid, 'r_bt': time1, 'r_rd': date, 'r_rh': time, 'r_a': amount})
        conn.commit()
        cursor.execute("""update car_details set rental_status = 'Yes' where reg_no = :r_rno""", {
            'r_rno': c1})
        conn.commit()

    def confirm(c1, c2, c3, c4, c5, c6, c7):
        global window
        time = int(etime.get())
        print(time)
        window = Toplevel(page)
        window.geometry("400x500")
        window.title('BILL')
        bill_lable = LabelFrame(window, text="Bill")
        bill_lable.place(x=50, y=30)
        reg_no_l = Label(bill_lable, text="REGISTRATION NO")
        reg_no_l.grid(row=0, column=0, padx=10, pady=10)
        model_l = Label(bill_lable, text="MODEL NAME")
        model_l.grid(row=1, column=0, padx=10, pady=10)
        seats_l = Label(bill_lable, text="SEATS")
        seats_l.grid(row=2, column=0, padx=10, pady=10)
        automatic_l = Label(bill_lable, text="AUTOMATIC(YES/NO)")
        automatic_l.grid(row=3, column=0, padx=10, pady=10)
        colour_l = Label(bill_lable, text="COLOUR")
        colour_l.grid(row=4, column=0, padx=10, pady=10)
        base_l = Label(bill_lable, text="BASE PRICE")
        base_l.grid(row=5, column=0, padx=10, pady=10)
        tariff_l = Label(bill_lable, text="TARIFF")
        tariff_l.grid(row=6, column=0, padx=10, pady=10)

        reg_no_e = Label(bill_lable, text=c1)
        reg_no_e.grid(row=0, column=1, padx=10, pady=10)
        model_e = Label(bill_lable, text=c2)
        model_e.grid(row=1, column=1, padx=10, pady=10)
        seats_e = Label(bill_lable, text=c3)
        seats_e.grid(row=2, column=1, padx=10, pady=10)
        automatic_e = Label(bill_lable, text=c4)
        automatic_e.grid(row=3, column=1, padx=10, pady=10)
        colour_e = Label(bill_lable, text=c5)
        colour_e.grid(row=4, column=1, padx=10, pady=10)
        base_e = Label(bill_lable, text=str(c6))
        base_e.grid(row=5, column=1, padx=10, pady=10)
        tariff_e = Label(bill_lable, text=str(c7))
        tariff_e.grid(row=6, column=1, padx=10, pady=10)
        if time <= 24:
            total_amount = c6
        else:
            total_amount = c6+(time-24)*c7

        amount_l = Label(bill_lable, text="AMOUNT")
        amount_l.grid(row=7, column=0, padx=10, pady=10)
        amount_e = Label(bill_lable, text=str(total_amount))
        amount_e.grid(row=7, column=1, padx=10, pady=10)
        savebtn = Button(window, text="Save and exit",
                         command=lambda: save(c1, time, total_amount))
        savebtn.place(x=180, y=390)

    def rent_sub():
        global etime, ltime, confirm_btn
        selected = my_tree.focus()
        values = my_tree.item(selected, 'values')
        try:
            rent_btn.destroy()
            for record in my_tree.get_children():
                my_tree.delete(record)
            data = []
            cursor.execute("""select reg_no,model_name,seats,automatic,colour,base_price,tariff from car_details as cd,car as c,rental_type as r where cd.car_id=c.car_id and c.rental_type = r.rental_type and cd.Rental_status = 'No' and reg_no = :val""", {
                'val': values[0]
            })
            for i in cursor:
                data.append(list(i))
            for record in data:
                my_tree.insert(parent='', index='end',
                               text="", values=(record[0], record[1], record[2], record[3], record[4], record[5], record[6]))
            c1 = record[0]
            c2 = record[1]
            c3 = record[2]
            c4 = record[3]
            c5 = record[4]
            c6 = record[5]
            c7 = record[6]
            ltime = Label(page, text="Enter Rental duration (in hours)")
            ltime.place(x=270, y=305)

            etime = Entry(page)
            etime.pack()

            confirm_btn = Button(page, text="Confirm Booking",
                                 command=lambda: confirm(c1, c2, c3, c4, c5, c6, c7))
            confirm_btn.pack(pady=10)
        except:
            query_database()
            messagebox.askretrycancel(
                "Booking", "Choose a car to rent")

    my_tree.bind("<ButtonRelease-1>", select_record)

    query_database()
    page.mainloop()
    conn.close()
