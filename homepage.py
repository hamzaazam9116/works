import tkinter as tk
import sqlite3
import profile_1
from profile_1 import show_profile_window

username_entry = None
root = None  #add a global variable for the root window

def search_database(name):
    #connect to the database
    conn = sqlite3.connect('DIYHub.db')
    c = conn.cursor()

    #search for service providers with matching username
    c.execute("SELECT * FROM Users WHERE username LIKE ? AND service_provider = 1", ('%' + name + '%',))
    users = c.fetchall()

    conn.close()

    return users

def search_users():
    global root
    search_name = freelancer_search_entry.get()
    users = search_database(search_name)
    if users:
        show_search_results(users)
    else:
        tk.messagebox.showinfo("Search Result", f"No service providers found matching the query.")

def show_user_details(user):
    details_window = tk.Toplevel()
    details_window.title("User Details")

    tk.Label(details_window, text="Name:").grid(row=0, column=0, sticky="w")
    tk.Label(details_window, text=user[4]).grid(row=0, column=1, sticky="w")

    tk.Label(details_window, text="Email:").grid(row=1, column=0, sticky="w")
    tk.Label(details_window, text=user[3]).grid(row=1, column=1, sticky="w")

    tk.Label(details_window, text="Phone Number:").grid(row=2, column=0, sticky="w")
    tk.Label(details_window, text=user[5]).grid(row=2, column=1, sticky="w")

    tk.Label(details_window, text="Address:").grid(row=3, column=0, sticky="w")
    tk.Label(details_window, text=user[8]).grid(row=3, column=1, sticky="w")

    tk.Label(details_window, text="Description:").grid(row=4, column=0, sticky="w")
    tk.Label(details_window, text=user[9]).grid(row=4, column=1, sticky="w")

def show_search_results(users):
    global root  #access the global root window
    root.withdraw()  #withdraw the home page window

    search_results_window = tk.Toplevel()
    search_results_window.geometry("1000x700")
    search_results_window.title("Search Results")

    result_label = tk.Label(search_results_window, text="Search Results:")
    result_label.pack()

    for user in users:
        user_label = tk.Label(search_results_window, text=user[4], cursor="hand2", fg="blue")
        user_label.pack()
        user_label.bind("<Button-1>", lambda event, arg=user: show_user_details(arg))

    #back button to return to the home page
    back_button = tk.Button(search_results_window, text="Back", command=lambda: return_to_home(root, search_results_window))
    back_button.pack()

def return_to_home(root, window):
    window.destroy()
    root.deiconify()  #restore the home page window

def show_home_page(username, show_profile_window):
    global root, home_frame, username_entry, logged_in_username
    logged_in_username = username  #set the logged-in username

    root = tk.Tk()  #create a new Tk instance
    root.title("DIY Hub")
    root.geometry("1000x700")

    home_frame = tk.Frame(root)
    home_frame.pack()

    def center_widgets(frame):
        frame.grid_rowconfigure(0, weight=1)
        frame.grid_columnconfigure(0, weight=1)

    center_widgets(home_frame)

    search_frame = tk.Frame(home_frame)
    search_frame.grid(row=0, column=0, pady=10, padx=10, sticky="ew")

    tk.Label(search_frame, text="Search Freelancer:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
    global freelancer_search_entry
    freelancer_search_entry = tk.Entry(search_frame)
    freelancer_search_entry.grid(row=0, column=1, padx=5, pady=5, sticky="ew")

    search_button = tk.Button(search_frame, text="Search", command=search_users)
    search_button.grid(row=0, column=2, padx=5, pady=5)

    #button for profile page
    profile_button = tk.Button(home_frame, text="Profile", command=lambda: show_profile_window(logged_in_username, root, return_to_home))
    profile_button.grid(row=0, column=5, pady=0, padx=10, sticky="e")

    root.mainloop()