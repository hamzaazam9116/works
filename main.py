import tkinter as tk
from tkinter import messagebox
import sqlite3
from database import dbcreation, insert_user
from homepage import show_home_page
from profile_1 import show_profile_window

#connect to database
dbcreation()

def sign_up_page():
    #function to switch to sign-up page
    login_frame.pack_forget()
    sign_up_frame.pack()

def back_to_login():
    #function to switch back to login page
    sign_up_frame.pack_forget()
    login_frame.pack()

def sign_up():
    #sign up a new user
    username = new_username_entry.get()
    password = new_password_entry.get()
    confirm_password = confirm_password_entry.get()
    phone_number = phone_number_entry.get()
    email = email_entry.get()
    name = name_entry.get()
    is_service_user = service_user_var.get()
    is_service_provider = service_provider_var.get()

    if username == "" or password == "" or confirm_password == "" or phone_number == "" or email == "" or name == "":
        messagebox.showerror("Error", "Please fill in all fields.")
    elif password != confirm_password:
        messagebox.showerror("Error", "Passwords do not match.")
    elif len(username) < 4 or len(username) > 12:
        messagebox.showerror("Error", "Username must be between 4 and 12 characters long")
    else:
        try:
            #insert new user into the database
            insert_user(username, password, email, name, phone_number, is_service_user, is_service_provider)
            messagebox.showinfo("Success", "Sign up successful.")
            back_to_login()
        except ValueError as e:
            messagebox.showerror("Error", str(e))

def login():
    #log in an existing user    
    username = username_entry.get()
    password = password_entry.get()

    if username == "" or password == "":
        messagebox.showerror("Error", "Please fill in all fields.")
    else:
        #connect to the database
        conn = sqlite3.connect('DIYHub.db')
        c = conn.cursor()

        #check if username exists in the database
        c.execute("SELECT * FROM Users WHERE username=?", (username,))
        user = c.fetchone()

        #close database connection
        conn.close()

        if user:
            #check the password if user exists
            if user[2] == password:  # user[2] is the password stored in the database
                messagebox.showinfo("Success", "Login successful.")
                root.destroy()  # Close the login window
                show_home_page(username, show_profile_window)  # Open the home page with logged-in username and profile window function
            else:
                messagebox.showerror("Error", "Invalid password.")
        else:
            messagebox.showerror("Error", "Invalid username.")

#creating tkinter GUI
root = tk.Tk()
root.title("Login System")
root.geometry("1000x700")

#creating the rames
login_frame = tk.Frame(root)
sign_up_frame = tk.Frame(root)

#function to center the widgets vertically
def center_widgets(frame):
    frame.grid_rowconfigure(0, weight=1)
    frame.grid_columnconfigure(0, weight=1)

#login Page
center_widgets(login_frame)
tk.Label(login_frame, text="Username:").grid(row=1, column=0, pady=(200, 5))
username_entry = tk.Entry(login_frame)
username_entry.grid(row=2, column=0, pady=5)

tk.Label(login_frame, text="Password:").grid(row=3, column=0, pady=5)
password_entry = tk.Entry(login_frame, show="*")
password_entry.grid(row=4, column=0, pady=5)

login_button = tk.Button(login_frame, text="Login", command=login)
login_button.grid(row=5, column=0, pady=5)

sign_up_button = tk.Button(login_frame, text="Sign Up", command=sign_up_page)
sign_up_button.grid(row=6, column=0, pady=5)

login_frame.pack()

#sign-Up Page
center_widgets(sign_up_frame)

tk.Label(sign_up_frame, text="New Username:").grid(row=1, column=0, pady=(200, 5))
new_username_entry = tk.Entry(sign_up_frame)
new_username_entry.grid(row=2, column=0, pady=5)

tk.Label(sign_up_frame, text="New Password:").grid(row=3, column=0, pady=5)
new_password_entry = tk.Entry(sign_up_frame, show="*")
new_password_entry.grid(row=4, column=0, pady=5)

tk.Label(sign_up_frame, text="Confirm Password:").grid(row=5, column=0, pady=5)
confirm_password_entry = tk.Entry(sign_up_frame, show="*")
confirm_password_entry.grid(row=6, column=0, pady=5)

tk.Label(sign_up_frame, text="Name:").grid(row=7, column=0, pady=5)  # Label for name
name_entry = tk.Entry(sign_up_frame)  # Entry widget for name
name_entry.grid(row=8, column=0, pady=5)

tk.Label(sign_up_frame, text="Email:").grid(row=9, column=0, pady=5)  # Label for email
email_entry = tk.Entry(sign_up_frame)  # Entry widget for email
email_entry.grid(row=10, column=0, pady=5)

tk.Label(sign_up_frame, text="Phone Number:").grid(row=11, column=0, pady=5)  # Label for phone number
phone_number_entry = tk.Entry(sign_up_frame)  # Entry widget for phone number
phone_number_entry.grid(row=12, column=0, pady=5)

#checkboxes for service user and service provider
service_user_var = tk.BooleanVar()
tk.Checkbutton(sign_up_frame, text="Service User", variable=service_user_var).grid(row=13, column=0, pady=5)
service_provider_var = tk.BooleanVar()
tk.Checkbutton(sign_up_frame, text="Service Provider", variable=service_provider_var).grid(row=14, column=0, pady=5)

sign_up_button = tk.Button(sign_up_frame, text="Sign Up", command=sign_up)
sign_up_button.grid(row=15, column=0, pady=5)

back_button = tk.Button(sign_up_frame, text="Back to Login", command=back_to_login)
back_button.grid(row=16, column=0, pady=5)

root.mainloop()