import mysql.connector
from datetime import date
import streamlit as st
import pandas as pd


mydb = mysql.connector.connect(
    host = "localhost",
    user = "root",
    password = "dhiru038",
    database = "project1"
)
mycursor = mydb.cursor()
print("Connection Established")

mycursor.execute("select e.event_id, e.name, e.date, e.venue, e.about, c.club_name from event e join club c on e.club_id = c.club_id where e.fac_approval='Approved' and e.dean_approval='Approved';")
result = mycursor.fetchall()
#print(result)

mycursor.execute("select name, srn from participant;")
result1 = mycursor.fetchall()

mycursor.close()
mydb.close()

if 'clicked' not in st.session_state:
    st.session_state.clicked = False

def click_button():
    st.session_state.clicked = True

def get_part_list(srn):
    mydb = mysql.connector.connect(
    host = "localhost",
    user = "root",
    password = "dhiru038",
    database = "project1"
    )
    mycursor = mydb.cursor()
    mycursor.execute("select p.event_id, event.name, p.date, event.date from participant p join event on p.event_id=event.event_id where srn=%s;",(srn,))
    result = mycursor.fetchall()
    mycursor.close()
    mydb.close()
    return result

def event_registration(name,srn,phone_no,email,event_id):
    mydb = mysql.connector.connect(
    host = "localhost",
    user = "root",
    password = "dhiru038",
    database = "project1"
    )
    mycursor = mydb.cursor()
    mycursor.execute("select srn, event_id from participant")
    check=mycursor.fetchall()
    if (srn,event_id) not in check:
        mycursor.execute("insert into participant values(%s,%s,%s,%s,%s,%s)",(srn,name,phone_no,email,event_id,date.today(),))
        mydb.commit()
        st.success("Registered!")
    else:
        st.error("Already registered for this event!")
    mycursor.close()
    mydb.close()


def dashboard(name,srn,phone_no,email):
    tab1,tab3= st.tabs(["**Events**","**Registered Events**"])
    with tab1:
        for item in result:
            st.subheader(item[1])
            st.write("Event ID: "+item[0])
            st.write("Date: "+str(item[2]))
            st.write("Venue: "+item[3])
            st.write("Description: "+item[4])
            st.write("Hosted by: "+item[5])
            st.button("Register Now!", on_click=click_button,key=item[0])
            if st.session_state.clicked:
                event_registration(name,srn,phone_no,email,item[0])
                
            st.divider()
        
    with tab3:
        if srn in [item[1] for item in result1]:
            participant_list=get_part_list(srn)
            df = pd.DataFrame(participant_list,columns=("Event ID","Event Name","Date of Registration","Date of Event"))
            st.table(df)
    




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
