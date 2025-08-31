import streamlit as st

import base64
import cv2

# ================ Background image ===

st.markdown(f'<h1 style="color:#000000;text-align: center;font-size:36px;font-family:concat">{"AI-Based OCR Solution for Digitizing and Translating Handwritten Documents in Regional Language"}</h1>', unsafe_allow_html=True)


def add_bg_from_local(image_file):
    with open(image_file, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read())
    st.markdown(
    f"""
    <style>
    .stApp {{
        background-image: url(data:image/{"png"};base64,{encoded_string.decode()});
        background-size: cover
    }}
    </style>
    """,
    unsafe_allow_html=True
    )
add_bg_from_local('back1.jpg')

# ----------------------

st.markdown(f'<h1 style="color:#0000FF;text-align: center;font-size:28px;font-family:Caveat, sans-serif;">{"Register Here !!!"}</h1>', unsafe_allow_html=True)



import streamlit as st
import sqlite3
import re

# Function to create a database connection
def create_connection(db_file):
    conn = None
    try:
        conn = sqlite3.connect(db_file)
    except sqlite3.Error as e:
        print(e)
    return conn

# Function to create a new user
def create_user(conn, user):
    sql = ''' INSERT INTO users(name, password, email, phone)
              VALUES(?,?,?,?) '''
    cur = conn.cursor()
    cur.execute(sql, user)
    conn.commit()
    return cur.lastrowid

# Function to check if a user already exists
def user_exists(conn, email):
    cur = conn.cursor()
    cur.execute("SELECT * FROM users WHERE email=?", (email,))
    if cur.fetchone():
        return True
    return False

# Function to validate email
def validate_email(email):
    pattern = r'^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$'
    return re.match(pattern, email)

# Function to validate phone number
def validate_phone(phone):
    pattern = r'^[6-9]\d{9}$'
    return re.match(pattern, phone)

# Main function
def main():
    # st.title("User Registration")

    # Create a database connection
    conn = create_connection("dbs.db")

    if conn is not None:
        # Create users table if it doesn't exist
        conn.execute('''CREATE TABLE IF NOT EXISTS users
                     (id INTEGER PRIMARY KEY,
                     name TEXT NOT NULL,
                     password TEXT NOT NULL,
                     email TEXT NOT NULL UNIQUE,
                     phone TEXT NOT NULL);''')

        # User input fields
        name = st.text_input("Enter your name")
        password = st.text_input("Enter your password", type="password")
        confirm_password = st.text_input("Confirm your password", type="password")
        email = st.text_input("Enter your email")
        phone = st.text_input("Enter your phone number")

        col1, col2 = st.columns(2)

        with col1:
                
            aa = st.button("REGISTER")
            
            if aa:
                
                if password == confirm_password:
                    if not user_exists(conn, email):
                        if validate_email(email) and validate_phone(phone):
                            user = (name, password, email, phone)
                            create_user(conn, user)
                            st.success("User registered successfully!")
                        else:
                            st.error("Invalid email or phone number!")
                    else:
                        st.error("User with this email already exists!")
                else:
                    st.error("Passwords do not match!")
                
                conn.close()
                # st.success('Successfully Registered !!!')
            # else:
                
                # st.write('Registeration Failed !!!')     
        
        with col2:
                
            aa = st.button("LOGIN")
            
            if aa:
                import subprocess
                subprocess.run(['python','-m','streamlit','run','Login.py'])



  
if __name__ == '__main__':
    main()











 
        
        
        