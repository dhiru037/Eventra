import mysql.connector
import streamlit as st
import subprocess

mydb = mysql.connector.connect(
    host = "localhost",
    user = "root",
    password = "dhiru038",
    database = "project1"
)
mycursor = mydb.cursor()
print("Connection Established")

mycursor.execute("select e.event_id, e.name, e.date, e.venue, e.about, e.price, c.club_name from event e join club c on e.club_id = c.club_id;")
result = mycursor.fetchall()
print(result)

mycursor.close()
mydb.close()

def dashboard(name,srn,phone_no,email):
    tab1,tab2,tab3,tab4 = st.tabs(["**Events**","**Register**","**Registered Events**","**Profile**"])
    with tab1:
        for item in result:
            st.subheader(item[1])
            st.write("Event ID: "+item[0])
            st.write("Date: "+str(item[2]))
            st.write("Venue: "+item[3])
            st.write("Description: "+item[4])
            #st.write("Price: "+str(item[5]))
            st.write("Hosted by: "+item[6])
            st.divider()
    with tab2:
        st.subheader("Register Here!")
        st.button("HI")
        #with st.form()
        #option=st.selectbox("**Event**",[item[1] for item in result],index=None,placeholder="Choose your event!")
        
    with tab3:
        pass
    with tab4:
        pass




def app():
    st.title(":rainbow[*Eventra*]")
    st.subheader("Register for your favourite events here!")
    name=st.sidebar.text_input("Name")
    srn=st.sidebar.text_input("SRN")
    phone_no=st.sidebar.text_input("Phone Number")
    email=st.sidebar.text_input("Email")
    if st.sidebar.button("Enter"):
        dashboard(name,srn,phone_no,email)

if __name__ == "__main__":
    app()