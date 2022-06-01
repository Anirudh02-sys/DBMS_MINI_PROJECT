from tkinter import *
from tkinter import ttk
from agency_details import view_agent_details
from rental_type import view_rental_type
from user_details import view_user_details
from rental_details import view_rental_details
from model_details import view_model_details
from car_details import view_car_details


def admin_view():
    root = Tk()
    root.title("Admin Page")
    root.geometry("500x400")

    list_frame = LabelFrame(root, text="Options", width=200)
    list_frame.pack(expand="yes")

    Lb1 = Listbox(list_frame)
    Lb1.insert(1, "View User details")
    Lb1.insert(2, "View/Update Agency details")
    Lb1.insert(3, "View/Update Models available")
    Lb1.insert(4, "View/Update Cars available")
    Lb1.insert(5, "View/Update Rental Packages")
    Lb1.insert(6, "View Rental details")

    Lb1.pack()
    Lb1.config(width=50)

    def selected_item():
        for i in Lb1.curselection():
            x = Lb1.get(i)
        if x == "View User details":
            view_user_details()
        elif x == "View/Update Agency details":
            view_agent_details()
        elif x == "View/Update Cars available":
            view_car_details()
        elif x == "View/Update Models available":
            view_model_details()
        elif x == "View Rental details":
            view_rental_details()
        elif x == "View/Update Rental Packages":
            view_rental_type()

    btn = Button(root, text='Open window', command=selected_item)
    btn.place(x=200, y=310)
    root.mainloop()
