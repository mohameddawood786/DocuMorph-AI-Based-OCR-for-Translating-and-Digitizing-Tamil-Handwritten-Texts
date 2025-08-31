import streamlit as st
import sqlite3
import re
import xx
import conversion

# ----- DB Functions -----
def create_connection(db_file):
    return sqlite3.connect(db_file)

def user_exists(conn, email):
    cur = conn.cursor()
    cur.execute("SELECT * FROM users WHERE email=?", (email,))
    return bool(cur.fetchone())

def validate_email(email):
    return re.match(r'^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$', email)

def validate_phone(phone):
    return re.match(r'^[6-9]\d{9}$', phone)

def create_user(conn, user):
    cur = conn.cursor()
    cur.execute(''' INSERT INTO users(name, password, email, phone) VALUES(?,?,?,?) ''', user)
    conn.commit()

def validate_user(conn, name, password):
    cur = conn.cursor()
    cur.execute("SELECT * FROM users WHERE name=? AND password=?", (name, password))
    user = cur.fetchone()
    return (True, user[1]) if user else (False, None)

# ----- Main App -----
def show_login():
    st.title("Login / Register")
    conn = create_connection("dbs.db")
    conn.execute('''CREATE TABLE IF NOT EXISTS users (
                        id INTEGER PRIMARY KEY,
                        name TEXT NOT NULL,
                        password TEXT NOT NULL,
                        email TEXT NOT NULL UNIQUE,
                        phone TEXT NOT NULL)''')

    option = st.radio("Choose", ["Login", "Register"])

    if option == "Register":
        name = st.text_input("Name")
        password = st.text_input("Password", type="password")
        confirm = st.text_input("Confirm Password", type="password")
        email = st.text_input("Email")
        phone = st.text_input("Phone Number")

        if st.button("Register"):
            if password != confirm:
                st.error("Passwords do not match.")
            elif user_exists(conn, email):
                st.error("User already exists.")
            elif not validate_email(email) or not validate_phone(phone):
                st.error("Invalid email or phone.")
            else:
                create_user(conn, (name, password, email, phone))
                st.success("Registered! Please log in.")

    elif option == "Login":
        name = st.text_input("Name")
        password = st.text_input("Password", type="password")
        if st.button("Login"):
            valid, user = validate_user(conn, name, password)
            if valid:
                st.session_state.logged_in = True
                st.session_state.user = user
                st.rerun()
            else:
                st.error("Invalid credentials")

    conn.close()

def show_main_menu():
    st.title(f"Welcome, {st.session_state.user} 👋")
    option = st.selectbox("Choose an option", ["-- Select --", "Extraction", "Conversion"])

    if option == "Extraction":
        xx.run_extraction()

    elif option == "Conversion":
        conversion.run_conversion()

# Initialize session state
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.user = None

# Routing
if not st.session_state.logged_in:
    show_login()
else:
    show_main_menu()
