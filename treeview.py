from tkinter import *
from tkinter import ttk


root = Tk()
root.geometry("700x610")
root.title("Input User Details")
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

data = [[1, "John"], [3, "Antony"], [2, "Aathreya"],
        [4, "Megh"], [5, "BeanPoleKIng"]]
my_tree['columns'] = ("ID", "Name")
count = 0
my_tree.column("#0", width=0, stretch=NO)
my_tree.column("ID", anchor=W, width=90, minwidth=30)
my_tree.column("Name", anchor=CENTER, width=200, minwidth=170)
my_tree.heading("#0", text="", anchor=W)
my_tree.heading("ID", text="ID", anchor=W)
my_tree.heading("Name", text="Name", anchor=CENTER)
for record in data:
    my_tree.insert(parent='', index='end', iid=count,
                   text="", values=(record[0], record[1]))
    count += 1


add_frame = Frame(root)
add_frame.pack(pady=5)

l_id = Label(add_frame, text="ID")
l_id.grid(row=0, column=0)

l_name = Label(add_frame, text="Name")
l_name.grid(row=0, column=1)

e_id = Entry(add_frame)
e_id.grid(row=1, column=0)

e_name = Entry(add_frame)
e_name.grid(row=1, column=1)


def select_record():
    e_id.delete(0, END)
    e_name.delete(0, END)
    selected = my_tree.focus()
    values = my_tree.item(selected, 'values')
    e_id.insert(0, values[0])
    e_name.insert(0, values[1])


def update_record():
    selected = my_tree.focus()
    values = my_tree.item(selected, text="", values=(e_id.get(), e_name.get()))
    e_id.delete(0, END)
    e_name.delete(0, END)


def add_record():
    global count
    my_tree.insert(parent='', index='end', iid=count,
                   text="", values=(e_id.get(), e_name.get()))
    count += 1
    e_id.delete(0, END)
    e_name.delete(0, END)


def del_record():
    x = my_tree.selection()[0]
    my_tree.delete(x)


select_rec = Button(root, text="Select record", command=select_record)
select_rec.pack(pady=20)

update_rec = Button(root, text="Save record", command=update_record)
update_rec.pack(pady=20)

add_rec = Button(root, text="Add record", command=add_record)
add_rec.pack(pady=20)

del_rec = Button(root, text="Delete selected record", command=del_record)
del_rec.pack(pady=10)

root.mainloop()
