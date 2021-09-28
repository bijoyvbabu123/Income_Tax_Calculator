import tkinter
from tkinter import ttk
from tkinter import messagebox
import sqlite3
import re

# needed functions
# validating entry for only numeric values
def only_numeric(letter):
    l = letter.replace(',', '')
    if bool(re.match('\d*\.\d*$', l)):
        return True
    if l.isdigit():
        return True
    if l == '':
        return True
    else:
        return False

# validating percentage only entry
def only_per(letter):
    if bool(re.match('\d*\.\d*$', letter)):
        return True
    if letter.isdigit():
        return True
    if letter == '':
        return True
    else:
        return False

# database creation and table initialization
def initialize_database_tables():
    db_connection = sqlite3.connect('data.db')
    db_cursor = db_connection.cursor()

    db_cursor.execute("""CREATE TABLE IF NOT EXISTS incometax (f REAL, t REAL, rate REAL)""")
    db_connection.commit()

    db_cursor.execute("""CREATE TABLE IF NOT EXISTS cesstax (rate REAL)""")
    db_connection.commit()

    db_cursor.execute("""SELECT * FROM cesstax""")
    data = db_cursor.fetchall()
    if not data:
        db_cursor.execute("""INSERT INTO cesstax VALUES (0)""")
        db_connection.commit()

    db_connection.close()

# sorting the table permanently
def sort_db_table():
    db_connection = sqlite3.connect('data.db')
    db_cursor = db_connection.cursor()

    db_cursor.execute("""CREATE TABLE s_incometax (f REAL, t REAL, rate REAL)""")
    db_connection.commit()
    db_cursor.execute("""INSERT INTO s_incometax (f, t, rate) SELECT f, t, rate FROM incometax ORDER BY f""")
    db_connection.commit()
    db_cursor.execute("""DROP TABLE incometax""")
    db_connection.commit()
    db_cursor.execute("""ALTER TABLE s_incometax RENAME TO incometax""")
    db_connection.commit()

    db_connection.close()

# updating tree and cess rate label
def update_tree():
    tree.delete(*tree.get_children())

    db_connection = sqlite3.connect('data.db')
    db_cursor = db_connection.cursor()

    db_cursor.execute("SELECT * FROM incometax")
    data = db_cursor.fetchall()
    
    for i in range(len(data)):
        row = []
        f = data[i][0]
        t = data[i][1]
        r = data[i][2]
        
        for j in [f, t, r]:
            row.append(j)

        if i%2 == 0:
            tree.insert(parent='', index='end', iid=i+1, values=row)
        else:
            tree.insert(parent='', index='end', iid=i+1, values=row, tags=('odd',))
    
    db_cursor.execute("""SELECT * FROM cesstax""")
    ce = db_cursor.fetchall()
    label_cess_rate.config(text='CESS Rate : '+str(ce[0][0])+'%')

    db_connection.close()
    check_tree_selection(event = None)

# function for adding price and rate into the tree
def add_range():
    window = tkinter.Toplevel()
    window.focus_set()
    window.resizable(width=False, height=False)
    window_width = 400
    window_height = 250
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    window_x = int((screen_width / 2) - (window_width / 2))
    window_y = int((screen_height / 2) - (window_height / 2)) - 50
    window.minsize(width=window_width, height=window_height)
    window.geometry(f'{window_width}x{window_height}+{window_x}+{window_y}')

    db_connection = sqlite3.connect('data.db')
    db_cursor = db_connection.cursor()

    db_cursor.execute("SELECT * FROM incometax")
    data = db_cursor.fetchall()    

    low = 0.00
    if data:
        low = data[-1][1]

    def addentry():
        valid = True
        
        if r.get() == '':
            r.insert(0, '0.00')
        
        high = 999999999999999.00  # this is the max value ;)
        if t.get() != '':
            high = float(t.get().replace(',',''))

        rate = float(r.get())
        
        if high < low:
            valid = False

        if(valid):
            db_cursor.execute("""INSERT INTO incometax VALUES (?,?,?)""",(low, high, rate))
            db_connection.commit()
            db_connection.close()
            sort_db_table()
            update_tree()
            window.destroy()
        
        else:
            messagebox.showwarning('Invalid Range', 'Please enter a valid range')
            window.focus_force()
            t.focus_set()

    fl = tkinter.Label(window, text='From : ', font='TkDefaultFont 12')
    fl.place(relx=0.05, rely=0.03)

    f = tkinter.Entry(window, font='TkDefaultFont 12', justify='right')
    f.place(relx=0.25, rely=0.03)
    f.config(validate='all', validatecommand=(window.register(only_numeric), '%P'))

    f.insert(0, low)
    f.config(state=tkinter.DISABLED)

    tl = tkinter.Label(window, text='To : ', font='TkDefaultFont 12')
    tl.place(relx=0.05, rely=0.23)

    t = tkinter.Entry(window, font='TkDefaultFont 12', justify='right')
    t.place(relx=0.25, rely=0.23)
    t.focus_set()
    t.config(validate='all', validatecommand=(window.register(only_numeric), '%P'))

    rl = tkinter.Label(window, text='Rate % : ', font='TkDefaultFont 12')
    rl.place(relx=0.05, rely=0.43)

    r = tkinter.Entry(window, font='TkDefaultFont 12', justify='center')
    r.place(relx=0.25, rely=0.43)
    r.config(validate='all', validatecommand=(window.register(only_per), '%P'))

    b = tkinter.Button(window, text='ADD', command=addentry, font='TkDefaultFont 12')
    b.place(relx=0.45, rely=0.7)

# finding tax and cess
def tax_and_cess(event):
    label_income_tax.config(text='Tax : '+'-'+' /-')
    label_cess.config(text='Cess : '+'-'+' /-')

    if income_entry.get() != '':
        income = float(income_entry.get().replace(',',''))

        db_connection = sqlite3.connect('data.db')
        db_cursor = db_connection.cursor()

        db_cursor.execute("SELECT * FROM incometax")
        data = db_cursor.fetchall()

        db_cursor.execute("""SELECT * FROM cesstax""")
        ce = db_cursor.fetchall()

        for i in data:
            if i[0] <= income <= i[1]:
                tax = (i[2]/100)*income
                label_income_tax.config(text='Tax : '+str(tax)+' /-')
                cess = (ce[0][0]/100)*tax
                label_cess.config(text='Cess : '+str(cess)+' /-')
                break

# checking tree selection
def check_tree_selection(event):
    if tree.selection():
        button_edit.config(state=tkinter.NORMAL)
        button_delete.config(state=tkinter.NORMAL)
    else:
        button_edit.config(state=tkinter.DISABLED)
        button_delete.config(state=tkinter.DISABLED)

#editing the cess rate
def cess_rate_edit():
    window = tkinter.Toplevel()
    window.focus_set()
    window.resizable(width=False, height=False)
    window_width = 400
    window_height = 250
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    window_x = int((screen_width / 2) - (window_width / 2))
    window_y = int((screen_height / 2) - (window_height / 2)) - 50
    window.minsize(width=window_width, height=window_height)
    window.geometry(f'{window_width}x{window_height}+{window_x}+{window_y}')

    def update_cess():
        if r.get() == '':
            r.insert(0, '0.00')
        rate = float(r.get())

        db_connection = sqlite3.connect('data.db')
        db_cursor = db_connection.cursor()

        db_cursor.execute("UPDATE cesstax SET rate="+str(rate))
        db_connection.commit()
        update_tree()
        window.destroy()

    l = tkinter.Label(window, text='Rate : ', font='TkDefaultFont 12')
    l.place(relx=0.15, rely=0.3)

    r = tkinter.Entry(window, font='TkDefaultFont 12', justify='center')
    r.place(relx=0.3, rely=0.3)
    r.focus_set()
    r.config(validate='all', validatecommand=(window.register(only_per), '%P'))

    b = tkinter.Button(window, text='SET', font='TkDefaultFont 12', command=update_cess)
    b.place(relx=0.45, rely=0.6)

# deleting from tree
def delete_range():
    row = int(tree.selection()[0])

    db_connection = sqlite3.connect('data.db')
    db_cursor = db_connection.cursor()

    db_cursor.execute("DELETE FROM incometax WHERE rowid="+str(row))
    db_connection.commit()

    sort_db_table()
    update_tree()

# edit rate of selected range
def edit_rate():
    window = tkinter.Toplevel()
    window.focus_set()
    window.resizable(width=False, height=False)
    window_width = 400
    window_height = 250
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    window_x = int((screen_width / 2) - (window_width / 2))
    window_y = int((screen_height / 2) - (window_height / 2)) - 50
    window.minsize(width=window_width, height=window_height)
    window.geometry(f'{window_width}x{window_height}+{window_x}+{window_y}')

    row = int(tree.selection()[0])
    def update_rate():
        if r.get() == '':
            r.insert(0, '0.00')
        rate = float(r.get())

        db_connection = sqlite3.connect('data.db')
        db_cursor = db_connection.cursor()

        db_cursor.execute("UPDATE incometax SET rate="+str(rate)+" where rowid="+str(row))
        db_connection.commit()

        update_tree()
        window.destroy()

    l = tkinter.Label(window, text='Rate : ', font='TkDefaultFont 12')
    l.place(relx=0.15, rely=0.3)

    r = tkinter.Entry(window, font='TkDefaultFont 12', justify='center')
    r.place(relx=0.3, rely=0.3)
    r.focus_set()
    r.config(validate='all', validatecommand=(window.register(only_per), '%P'))

    b = tkinter.Button(window, text='SET', font='TkDefaultFont 12', command=update_rate)
    b.place(relx=0.45, rely=0.6)

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
income_entry.config(validate='all', validatecommand=(root.register(only_numeric), '%P'))
income_entry.bind("<KeyRelease>", lambda event: tax_and_cess(event))

label_income_tax = tkinter.Label(root, text='Tax : '+'-'+' /-', font="TkDefaultFont 14")
label_income_tax.place(rely=0.3, relx=0.65)

label_cess = tkinter.Label(root, text='Cess : '+'-'+' /-', font="TkDefaultFont 14")
label_cess.place(rely=0.5, relx=0.65)

button_add = ttk.Button(root, text='Add', command=add_range)
button_add.place(relwidth=0.07, relheight=0.0256 * 2, rely=0.66, relx=0.1)

button_delete = ttk.Button(root, text='Delete', state=tkinter.DISABLED, command=delete_range)
button_delete.place(relwidth=0.07, relheight=0.0256 * 2, rely=0.66, relx=0.22)

button_edit = ttk.Button(root, text='Edit Rate', state=tkinter.DISABLED, command=edit_rate)
button_edit.place(relwidth=0.07, relheight=0.0256 * 2, rely=0.66, relx=0.34)

label_cess_rate = tkinter.Label(root, text='CESS Rate : '+'10'+'%', font="TkDefaultFont 20")
label_cess_rate.place(relx=0.02, rely=0.8)

button_cess_edit = ttk.Button(root, text='Edit', command=cess_rate_edit)
button_cess_edit.place(relwidth=0.07, relheight=0.0256*2, rely=0.8, relx=0.3)

treescroll = tkinter.Scrollbar(root, orient=tkinter.VERTICAL)
treescroll.place(relheight=0.6, relx=0.52, rely=0.03)

tree = ttk.Treeview(root, show=['headings'], selectmode='browse', yscrollcommand=treescroll.set)
tree.place(relwidth=0.5, relheight=0.6, relx=0.02, rely=0.03)

tree.bind('<FocusIn>', check_tree_selection)
tree.bind('<ButtonRelease-1>', check_tree_selection)
tree.bind('<KeyRelease>', check_tree_selection)

treescroll.config(command=tree.yview)

tree['columns'] = ('from', 'to', 'rate')
root.update()
tree.update()
tree.column('from', anchor=tkinter.E, width=int(tree.winfo_width() / 3))
tree.column('to', anchor=tkinter.E, width=int(tree.winfo_width() / 3))
tree.column('rate', anchor=tkinter.E, width=int(tree.winfo_width() / 3.1))
tree.heading('from', text='From')  # , anchor=tkinter.W
tree.heading('to', text='To')
tree.heading('rate', text='Rate %')

tree.tag_configure('odd', background="light sky blue")
update_tree()

root.mainloop()