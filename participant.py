import mysql.connector
from datetime import date
import streamlit as st
import pandas as pd

mydb = mysql.connector.connect(
    host = "localhost",
    user = "root",
    password = "Chandu@2605",
    database = "project1"
)
mycursor = mydb.cursor()
print("Connection Established")


#print(result)

def upcoming_events(name,srn,phone,email):
    mydb = mysql.connector.connect(
    host = "localhost",
    user = "root",
    password = "Chandu@2605",
    database = "project1"
    )
    mycursor = mydb.cursor()
    print("Connection Established")

    mycursor.execute("select e.event_id, e.name, e.date, e.venue, e.about, c.club_name from event e join club c on e.club_id = c.club_id where e.fac_approval='Approved' and e.dean_approval='Approved';")
    result = mycursor.fetchall()
    df=pd.DataFrame(result,columns=("Event ID","Name","Date","Venue","Description","Hosted by"))
    st.table(df)
    with st.form("Registration"):
        st.subheader("Register Here!")
        options=[item[1] for item in result]
        choice=st.selectbox("Select your event!",options,index=None)
        submit=st.form_submit_button("Register!")
        if submit:
            mycursor.execute("select event_id from event where name=%s",(choice,))
            event_id=mycursor.fetchone()[0]
            mycursor.execute("SELECT * FROM participant WHERE srn=%s AND event_id=%s", (srn, event_id,))
            existing_registration = mycursor.fetchone()
            if existing_registration:
                st.error("Oops! You've already registered for this event, select a different event")
            else: 
                
                mycursor.execute("insert into participant values(%s,%s,%s,%s,%s,%s)",(srn,name,phone,email,event_id,date.today(),))
                mydb.commit()
                st.success("Registered!")
        

def registered_events(name,srn,phone,email):
    mydb = mysql.connector.connect(
    host = "localhost",
    user = "root",
    password = "Chandu@2605",
    database = "project1"
    )
    mycursor = mydb.cursor()
    mycursor.execute("select p.event_id, event.name, p.date, event.date from participant p join event on p.event_id=event.event_id where srn=%s;",(srn,))
    result1 = mycursor.fetchall()
    mycursor.close()
    mydb.close()
    
    df = pd.DataFrame(result1,columns=("Event ID","Event Name","Date of Registration","Date of Event"))
    st.table(df)

def app():
    col1, col2, col3 = st.columns([1, 2, 1])

    # Place the image in the middle column for center alignment
    with col2:
        logo_path = 'images/logo.png'  # Replace with your actual path to the logo file
        st.image(logo_path, width=300, output_format='PNG')  # Set width and format for the image
    #st.subheader("~ Home for all your favourite events! ~")
    st.divider()
    
    st.sidebar.title("Details")
    name=st.sidebar.text_input("Name")
    srn=st.sidebar.text_input("SRN")
    phone=st.sidebar.text_input("Contact No")
    email=st.sidebar.text_input("Email")
    if email:
        options=["Upcoming Events","Registered Events"]
        choice=st.selectbox("Choose Option",options,index=None,placeholder="Option")
        if choice=="Upcoming Events":
            upcoming_events(name,srn,phone,email)
        elif choice=="Registered Events":
            registered_events(name,srn,phone,email)

    
    




if __name__ == "__main__":
    app()
