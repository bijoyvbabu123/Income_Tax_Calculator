import tkinter
from tkinter import ttk
from tkinter import messagebox
import sqlite3
import re

# needed functions

# database creation and table initialization
def initialize_database_tables():
    db_connection = sqlite3.connect('data.db')
    db_cursor = db_connection.cursor()

    db_cursor.execute("""CREATE TABLE IF NOT EXISTS incometax (f REAL, t REAL, rate REAL)""")
    db_connection.commit()

    db_cursor.execute("""CREATE TABLE IF NOT EXISTS cesstax (rate REAL)""")
    db_connection.commit()

# initial function calling
initialize_database_tables()

# the main window
root = tkinter.Tk()
root.title('Income Tax Calculator')

# window sizing and placing
root_width = 1000
root_height = 600
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
root_x = int((screen_width / 2) - (root_width / 2))
root_y = int((screen_height / 2) - (root_height / 2)) - 50
root.minsize(width=root_width, height=root_height)
root.geometry(f'{root_width}x{root_height}+{root_x}+{root_y}')
root.resizable(False, False)

# theme customization for ttk widgets
style = ttk.Style()
style.theme_use('clam')
style.configure("Treeview", background="white", fieldbackground="white", rowheight=25, font='TkDefaultFont 9 italic')
style.configure("Treeview.Heading", font='TkDefaultFont 10 bold')
style.map("Treeview", background=[('selected', 'RoyalBlue3')])

# the widgets
label_income = tkinter.Label(root, text='Income : ', font="TkDefaultFont 14")
label_income.place(rely=0.05, relx=0.6)

income_entry = tkinter.Entry(root, justify='right', font="TkDefaultFont 14")
income_entry.place(rely=0.05, relx=0.7, relwidth=0.2)
income_entry.focus_set()

label_income_tax = tkinter.Label(root, text='Tax : '+'10000'+' /-', font="TkDefaultFont 14")
label_income_tax.place(rely=0.3, relx=0.65)

label_income_tax = tkinter.Label(root, text='Cess : '+'10000'+' /-', font="TkDefaultFont 14")
label_income_tax.place(rely=0.5, relx=0.65)

button_edit = ttk.Button(root, text='Edit', state=tkinter.DISABLED)
button_edit.place(relwidth=0.07, relheight=0.0256 * 2, rely=0.66, relx=0.1)

button_delete = ttk.Button(root, text='Delete', state=tkinter.DISABLED)
button_delete.place(relwidth=0.07, relheight=0.0256 * 2, rely=0.66, relx=0.22)

button_delete = ttk.Button(root, text='Delete', state=tkinter.DISABLED)
button_delete.place(relwidth=0.07, relheight=0.0256 * 2, rely=0.66, relx=0.34)

label_cess = tkinter.Label(root, text='CESS Rate : '+'10'+'%', font="TkDefaultFont 20")
label_cess.place(relx=0.02, rely=0.8)

button_cess_edit = ttk.Button(root, text='Edit')
button_cess_edit.place(relwidth=0.07, relheight=0.0256*2, rely=0.8, relx=0.3)

treescroll = tkinter.Scrollbar(root, orient=tkinter.VERTICAL)
treescroll.place(relheight=0.6, relx=0.52, rely=0.03)

tree = ttk.Treeview(root, show=['headings'], selectmode='browse', yscrollcommand=treescroll.set)
tree.place(relwidth=0.5, relheight=0.6, relx=0.02, rely=0.03)

treescroll.config(command=tree.yview)

tree['columns'] = ('from', 'to', 'rate')
root.update()
tree.update()
tree.column('from', anchor=tkinter.E, width=int(tree.winfo_width() / 3))
tree.column('to', anchor=tkinter.E, width=int(tree.winfo_width() / 3))
tree.column('rate', anchor=tkinter.E, width=int(tree.winfo_width() / 3))
tree.heading('from', text='From')  # , anchor=tkinter.W
tree.heading('to', text='To')
tree.heading('rate', text='Rate %')

tree.tag_configure('odd', background="light sky blue")


root.mainloop()