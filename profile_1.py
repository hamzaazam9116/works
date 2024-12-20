import tkinter as tk
from tkinter import messagebox
import sqlite3

def show_profile_window(username, root, return_to_home_callback):
    #withdraw the home page window
    root.withdraw()
    
    #get user details from the database
    conn = sqlite3.connect('DIYHub.db')
    c = conn.cursor()
    c.execute("SELECT * FROM Users WHERE username=?", (username,))
    user_details = c.fetchone()
    conn.close()

    profile_window = tk.Toplevel()
    profile_window.geometry("800x600")
    profile_window.title("Profile")

    #create StringVar variables for each entry field
    username_var = tk.StringVar(value=user_details[1])
    name_var = tk.StringVar(value=user_details[4])
    phone_var = tk.StringVar(value=user_details[5])
    address_var = tk.StringVar(value=user_details[8])
    description_var = tk.StringVar(value=user_details[9])

    username_label = tk.Label(profile_window, text="Username:")
    username_label.grid(row=0, column=0, padx=5, pady=5, sticky="w")
    username_entry = tk.Entry(profile_window, textvariable=username_var, state='disabled')
    username_entry.grid(row=0, column=1, padx=5, pady=5, sticky="ew")

    name_label = tk.Label(profile_window, text="Name:")
    name_label.grid(row=1, column=0, padx=5, pady=5, sticky="w")
    name_entry = tk.Entry(profile_window, textvariable=name_var)
    name_entry.grid(row=1, column=1, padx=5, pady=5, sticky="ew")

    phone_label = tk.Label(profile_window, text="Phone Number:")
    phone_label.grid(row=2, column=0, padx=5, pady=5, sticky="w")
    phone_entry = tk.Entry(profile_window, textvariable=phone_var)
    phone_entry.grid(row=2, column=1, padx=5, pady=5, sticky="ew")

    address_label = tk.Label(profile_window, text="Address:")
    address_label.grid(row=3, column=0, padx=5, pady=5, sticky="w")
    address_entry = tk.Entry(profile_window, textvariable=address_var)
    address_entry.grid(row=3, column=1, padx=5, pady=5, sticky="ew")

    description_label = tk.Label(profile_window, text="Description:")
    description_label.grid(row=4, column=0, padx=5, pady=5, sticky="w")
    description_entry = tk.Entry(profile_window, width=50, textvariable=description_var)
    description_entry.grid(row=4, column=1, padx=5, pady=5, sticky="ew")

    def return_to_home():
        #destroy the profile window and return to the homepage
        profile_window.destroy()
        root.deiconify()

    back_button = tk.Button(profile_window, text="Back", command=return_to_home)
    back_button.grid(row=6, column=0, columnspan=2, pady=10)

    def update_details():
        #update user details in the database
        conn = sqlite3.connect('DIYHub.db')
        c = conn.cursor()
        c.execute("UPDATE Users SET name=?, phone_number=?, address=?, description=? WHERE username=?", (name_var.get(), phone_var.get(), address_var.get(), description_var.get(), username_var.get()))
        conn.commit()
        conn.close()
        messagebox.showinfo("Update", "User details updated successfully.")

    update_button = tk.Button(profile_window, text="Update", command=update_details)
    update_button.grid(row=5, column=0, columnspan=2, pady=10)