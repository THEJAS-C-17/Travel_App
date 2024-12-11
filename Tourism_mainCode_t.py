#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3

# Create a SQLite database
conn = sqlite3.connect('transportation_data.db')
cursor = conn.cursor()
cursor.execute('''
CREATE TABLE IF NOT EXISTS routes (
id INTEGER PRIMARY KEY,
source TEXT,
destination TEXT,
distance REAL,
cost REAL
)
''')
conn.commit()

class TransportationManagement:
    def __init__(self, root):
        self.root = root
        self.root.title("Transportation Route Management")
        self.route_list = []
        self.create_widgets()
        self.load_data()

    def create_widgets(self):
        self.label = tk.Label(self.root, text="Transportation Routes", fg="blue")
        self.label.pack()

        self.tree = ttk.Treeview(self.root, columns=("Source", "Destination", "Distance", "Cost"))
        self.tree.heading("#1", text="Source")
        self.tree.heading("#2", text="Destination")
        self.tree.heading("#3", text="Distance")
        self.tree.heading("#4", text="Cost")
        self.tree.pack()

        self.refresh_button = tk.Button(self.root, text="Refresh Routes", command=self.load_data, bg="lightgray")
        self.refresh_button.pack()

        self.add_button = tk.Button(self.root, text="Add Route", command=self.add_route, bg="green")
        self.add_button.pack()

        self.delete_button = tk.Button(self.root, text="Delete Route", command=self.delete_route, bg="red")
        self.delete_button.pack()

        self.search_label = tk.Label(self.root, text="Search Source/Destination:", fg="green")
        self.search_label.pack()
        self.search_entry = tk.Entry(self.root)
        self.search_entry.pack()
        self.search_button = tk.Button(self.root, text="Search", command=self.search_route, bg="blue")
        self.search_button.pack()

    def load_data(self):
        cursor.execute("SELECT * FROM routes")
        self.route_list = cursor.fetchall()
        for item in self.tree.get_children():
            self.tree.delete(item)
        for route in self.route_list:
            self.tree.insert("", "end", values=route[1:])

    def add_route(self):
        add_window = tk.Toplevel(self.root)
        add_window.title("Add Route")

        source_label = tk.Label(add_window, text="Source:", fg="blue")
        source_label.pack()
        source_entry = tk.Entry(add_window)
        source_entry.pack()

        dest_label = tk.Label(add_window, text="Destination:", fg="blue")
        dest_label.pack()
        dest_entry = tk.Entry(add_window)
        dest_entry.pack()

        distance_label = tk.Label(add_window, text="Distance:", fg="blue")
        distance_label.pack()
        distance_entry = tk.Entry(add_window)
        distance_entry.pack()

        cost_label = tk.Label(add_window, text="Cost:", fg="blue")
        cost_label.pack()
        cost_entry = tk.Entry(add_window)
        cost_entry.pack()

        add_button = tk.Button(add_window, text="Add", command=lambda: self.insert_route(
            source_entry.get(), dest_entry.get(), distance_entry.get(), cost_entry.get()), bg="green")
        add_button.pack()

    def insert_route(self, source, dest, distance, cost):
        try:
            distance = float(distance)
            cost = float(cost)
            cursor.execute("INSERT INTO routes (source, destination, distance, cost) VALUES (?, ?, ?, ?)",
                           (source, dest, distance, cost))
            conn.commit()
            self.load_data()
        except ValueError:
            messagebox.showerror("Error", "Distance and Cost must be numeric.")

    def delete_route(self):
        selected_item = self.tree.selection()
        if selected_item:
            route_id = self.route_list[self.tree.index(selected_item[0])][0]
            cursor.execute("DELETE FROM routes WHERE id=?", (route_id,))
            conn.commit()
            self.load_data()

    def search_route(self):
        keyword = self.search_entry.get()
        if keyword:
            filtered_routes = [route for route in self.route_list if keyword.lower() in ' '.join(map(str, route)).lower()]
            for item in self.tree.get_children():
                self.tree.delete(item)
            for route in filtered_routes:
                self.tree.insert("", "end", values=route[1:])

if __name__ == "__main__":
    root = tk.Tk()
    app = TransportationManagement(root)
    root.mainloop()

# Close the database connection when done
conn.close()

