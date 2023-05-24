import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import mysql.connector

db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="********",
    database="MarvelDB"
)

cursor = db.cursor()

create_table_query = """CREATE TABLE IF NOT EXISTS marvel_movies"""
cursor.execute(create_table_query)

with open("Marvel.txt", "r") as file:
    for line in file:
        line = line.strip()
        if line:
            data = line.split("\t")
            id = int(data[0])
            movie = data[1]
            date = data[2]
            mcu_phase = data[3]
            insert_query = "INSERT INTO marvel_movies (id, movie, date, mcu_phase) VALUES (%s, %s, %s, %s)"
            values = (id, movie, date, mcu_phase)
            cursor.execute(insert_query, values)
    db.commit()

def add_popup():
    popup = tk.Toplevel()
    popup.title("Add Movie")
    entry = tk.Entry(popup, width=30)
    entry.pack(padx=10, pady=10)
    ok_button = tk.Button(popup, text="Ok", command=lambda: add_movie(entry.get(), popup))
    ok_button.pack(padx=10, pady=5)
    cancel_button = tk.Button(popup, text="Cancel", command=popup.destroy)
    cancel_button.pack(padx=10, pady=5)

def add_movie(movie, popup):
        id = combo.get()
        insert_query = "INSERT INTO marvel_movies (id, movie) VALUES (%s, %s)"
        values = (id, movie)
        cursor.execute(insert_query, values)
        db.commit()
        messagebox.showinfo("Success", "Movie added successfully!")
        popup.destroy()

def list_all():
    select_query = "SELECT * FROM marvel_movies"
    cursor.execute(select_query)
    results = cursor.fetchall()
    textbox.delete(1.0, tk.END)
    for row in results:
        textbox.insert(tk.END, f"ID: {row[0]}, Movie: {row[1]}, Date: {row[2]}, MCU Phase: {row[3]}\n")

root = tk.Tk()
root.title("Marvel Movies")

frame = tk.Frame(root)
frame.pack(padx=10, pady=10)

combo = ttk.Combobox(frame, values=[str(i) for i in range(1, 100)], state="readonly")
combo.current(0)
combo.pack(side=tk.LEFT, padx=5)

add_button = tk.Button(frame, text="Add", command=add_popup)
add_button.pack(side=tk.LEFT, padx=5)

list_button = tk.Button(root, text="LIST ALL", command=list_all)
list_button.pack(padx=10, pady=5)

textbox = tk.Text(root, width=50, height=10)
textbox.pack(padx=10, pady=10)

root.mainloop()

db.close()
