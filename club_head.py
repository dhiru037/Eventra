import streamlit as st
import mysql.connector
import pandas as pd

mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="dhiru038",
    database="project1"
)
mycursor = mydb.cursor()
print("Connection Established")

def get_event_list(club_id):
    mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="dhiru038",
    database="project1"
    )
    mycursor = mydb.cursor() 

    mycursor.execute("select event_id, name, date, venue, about, proposal, fac_approval, dean_approval, remarks from event where club_id=%s",(club_id,))
    result=mycursor.fetchall()
    mycursor.close()
    mydb.close()
    return result
    
    
def event_creation(club_id):
    st.subheader("Event Creation")
    with st.form("EventCreation"):
        st.write("New Event Details")
        event_id=st.text_input("Event ID")
        name=st.text_input("Name")
        date=st.date_input("Date")
        venue=st.text_input("Venue")
        about=st.text_area("Description")
        proposal=st.text_input("Proposal link")
        create=st.form_submit_button("Create Event")
        if create:
            mydb = mysql.connector.connect(
            host = "localhost",
            user = "root",
            password = "dhiru038",
            database = "project1"
            )
            mycursor = mydb.cursor()
            sql=("insert into event values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)")
            values=(event_id,name,date,venue,about,proposal,'Pending','Pending','Event Created',club_id)
            mycursor.execute(sql,values)
            mydb.commit()
            st.success("Event Created!")
            st.balloons()
            mycursor.close()
            mydb.close()

def approval_status(club_id):
    st.subheader("Approval Status")
    result=get_event_list(club_id)
    df = pd.DataFrame(result,columns=("Event ID","Name","Date","Venue","Description","Proposal","Faculty Approval","Dean Approval","Remarks"))
    st.table(df)
    mydb = mysql.connector.connect(
    host = "localhost",
    user = "root",
    password = "dhiru038",
    database = "project1"
    )
    mycursor = mydb.cursor()
    with st.form("ReqApproval"):
        st.write("Request for Approval / Update Remarks")
        event_id=st.text_input("Event ID")
        remarks=st.text_area("Add remarks of updates on Proposal")
        reqApproval = st.form_submit_button("Update")
        if reqApproval:
            mycursor.execute("update event set remarks = %s where event_id = %s",(remarks,event_id,))
            mydb.commit()
            st.success("Remarks Updated!")
    mycursor.close()
    mydb.close()

def event_registration(event_id):
    st.subheader("Event Registrations")
    mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="dhiru038",
    database="project1"
    )
    mycursor = mydb.cursor() 
    mycursor.execute("select srn, name, phone_no, email, date from participant where event_id=%s;",(event_id,))
    result=mycursor.fetchall()
    df = pd.DataFrame(result,columns=("SRN","Name","PhoneNo","Email","Date of Registration"))
    st.table(df)
    mycursor.close()
    mydb.close()

def club_info(club_id):
    mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="dhiru038",
    database="project1"
    )
    mycursor = mydb.cursor()
    mycursor.execute("select club_name, vertical, about from club where club_id=%s",(club_id,))
    result=mycursor.fetchall()[0]
    mycursor.execute("select fac_name, faculty_id, phone_no, email from faculty where club_id=%s",(club_id,))
    result1=mycursor.fetchall()[0]
    mycursor.execute("select name, head_id, phone_no, email from club_head where club_id=%s",(club_id,))
    result2=mycursor.fetchall()[0]
    st.header("Club Info")
    st.divider()
    col1, col2, col3 = st.columns([1,1,1])
    with col1:
        st.subheader("Club")
        st.write("ID: "+club_id)
        st.write("Name: "+result[0])
        st.write("Vertical: "+result[1])
        st.write("About: "+result[2])
    with col2:
        st.subheader("Mentor")
        st.write("Faculty ID: "+result1[1])
        st.write("Name: "+result1[0])
        st.write("Contact: "+result1[2])
        st.write("Email: "+result1[3])
    with col3:
        st.subheader("Head")
        st.write("Member ID: "+result2[1])
        st.write("Name: "+result2[0])
        st.write("Contact: "+result2[2])
        st.write("Email: "+result2[3])
    mycursor.close()
    mydb.close()

def app():
    st.title(":rainbow[Eventra]")
    st.header("Club Head Dashboard")
    st.divider()
    club_id=st.sidebar.text_input("Club ID")
    if club_id:
        st.sidebar.title("Navigation")
        options = ["Club Info","Event Creation", "Approval Status", "Event Registrations"]
        choice = st.sidebar.selectbox("Select Option", options,placeholder="Choose")

        if choice == "Event Creation":
            event_creation(club_id)
        elif choice == "Approval Status":
            approval_status(club_id)
            
        elif choice == "Event Registrations":
            result1=get_event_list(club_id)
            event_ids=[item[0] for item in result1]
            event_id=st.selectbox("Event ID",event_ids,index=None,placeholder="Select an Event")
            if event_id:
                event_registration(event_id)
        
        elif choice == "Club Info":
            club_info(club_id)

if __name__ == "__main__":
    app()
