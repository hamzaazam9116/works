import sqlite3

def dbcreation():
    #connect to the SQLite database
    conn = sqlite3.connect('DIYHub.db')
    c = conn.cursor()

    #create the users table
    c.execute('''CREATE TABLE IF NOT EXISTS Users (
                 user_id INTEGER PRIMARY KEY AUTOINCREMENT,
                 username TEXT UNIQUE,
                 password TEXT,
                 email TEXT,
                 name TEXT,
                 phone_number TEXT,
                 service_user INTEGER,
                 service_provider INTEGER,
                 address TEXT,
                 description TEXT,
                 rating REAL
                 )''')

    #commit changes and close connection
    conn.commit()
    conn.close()

#call dbcreation function to create the table
dbcreation()

def insert_user(username, password, email, name, phone_number, is_service_user, is_service_provider):
    conn = sqlite3.connect('DIYHub.db') #connecting to database
    c = conn.cursor()

    #check if username already exists
    c.execute("SELECT * FROM Users WHERE username=?", (username,))
    existing_user = c.fetchone()

    if existing_user:
        conn.close()
        raise ValueError("Username already exists")

    #insert the new user
    c.execute("INSERT INTO Users (username, password, email, name, phone_number, service_user, service_provider) VALUES (?, ?, ?, ?, ?, ?, ?)", (username, password, email, name, phone_number, is_service_user, is_service_provider))

    conn.commit()
    conn.close()