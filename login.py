import mysql.connector
import streamlit as st
import subprocess
from mysql.connector import Error


mydb = mysql.connector.connect(
    host = "localhost",
    user = "root",
    password = "Chandu@2605",
    database = "project1"
)
mycursor = mydb.cursor()
print("Connection Established")

# Function to create a connection to the MySQL database
def create_server_connection(host_name, user_name, user_password, db_name):
    connection = None
    try:
        connection = mysql.connector.connect(
            host='localhost',
            user='root',
            passwd='Chandu@2605',
            database='project1'
        )
        st.success("MySQL Database connection successful")
    except Error as err:
        st.error(f"Error: '{err}'")
    return connection



def app():
    mycursor.execute("select name, head_id from club_head")
    result = mycursor.fetchall()
    mycursor.execute("select fac_name, faculty_id from faculty")
    result1=mycursor.fetchall()
    mycursor.close()
    mydb.close()
    
    col1, col2, col3 = st.columns([1,2,1])
    with col2:  # Using the center column to display the image
        logo_path = 'images/logo.png'  # The path to your logo file
        st.image(logo_path, width=300, output_format='PNG')

    #st.header("College Event Management Platform")
    st.subheader("Login")
    name = st.text_input("Name")
    password = st.text_input("Password", type='password', help="Your ID is your password")
    if st.button("Login"):
        if name=="Dean" and password=="dean123":
            st.write("Welcome Dean!")
            subprocess.run(["streamlit","run","dean.py"])
        elif (name,password) in result1:
            st.write("Welcome Club Mentor!")
            subprocess.run(["streamlit","run","faculty.py"])
        elif (name,password) in result:
            st.write("Welcome Club Head!")
            subprocess.run(["streamlit","run","club_head.py"])
        else:
            st.error("Check credentials and try again!")


if __name__ == "__main__":
    app()