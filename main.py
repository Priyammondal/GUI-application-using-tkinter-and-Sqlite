from tkinter import *
import sqlite3
from tkinter import ttk
window = Tk()
window.title("User Details")
window.geometry("450x180")
# window.resizable(False, False)
with sqlite3.connect("details.db") as db:
    cursor = db.cursor()
    cursor.execute(
        """CREATE TABLE IF NOT EXISTS users(id integer PRIMARY KEY AUTOINCREMENT, username text NOT NULL, password text NOT NULL);""")


def add_new_user():
    newUsername = username.get()
    newPassword = password.get()
    cursor.execute(
        "SELECT COUNT(*) from users WHERE username ='"+newUsername+"'")
    result = cursor.fetchone()
    if int(result[0]) > 0:
        error["text"] = "Error: Username already exists"
    elif (len(newUsername) == 0 or len(newPassword) == 0):
        error["text"] = "Error: Fill up the fields before add"
    else:
        error["text"] = "Added new user"
        cursor.execute(
            "INSERT INTO users (username,password) VALUES(?,?)", (newUsername, newPassword))
        db.commit()


def show_details():
    # fetch from database
    cursor.execute("SELECT * from users")
    rows = cursor.fetchall()
    total = cursor.rowcount
    print("Total data entries: "+str(total))

    frm = Frame(window)
    frm.pack()

    tv = ttk.Treeview(frm, columns=(1, 2, 3), show="headings", height="5")
    tv.pack()

    tv.heading(1, text="Id")
    tv.heading(2, text="Usename")
    tv.heading(3, text="Password")
    for i in rows:
        tv.insert("", "end", values=i)


# custom message
error = Message(text="", width=160)
error.place(x=30, y=10)
error.config(padx=0)
# username
label1 = Label(text="Enter Username:")
label1.place(x=30, y=40)
label1.config(bg="lightgreen", padx=0)

username = Entry(text="")
username.place(x=150, y=40, width=200, height=25)

# password
label2 = Label(text="Enter Password:")
label2.place(x=30, y=80)
label2.config(bg="lightgreen", padx=0)

password = Entry(text="")
password.place(x=150, y=80, width=200, height=25)

# button
button = Button(text="Add", command=add_new_user)
button.place(x=150, y=120, width=75, height=35)

button = Button(text="Show Details", command=show_details)
button.place(x=275, y=120, width=75, height=35)


window.mainloop()
