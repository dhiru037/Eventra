import streamlit as st
import mysql.connector
import pandas as pd
from datetime import datetime

mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Chandu@2605",
    database="project1"
)
mycursor = mydb.cursor()
print("Connection Established")

def get_event_list(club_id):
    mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Chandu@2605",
    database="project1"
    )
    mycursor = mydb.cursor() 

    mycursor.execute("select event_id, name, date, venue, about, fac_approval, dean_approval, remarks, proposal from event where club_id=%s",(club_id,))
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
            password = "Chandu@2605",
            database = "project1"
            )
            mycursor = mydb.cursor()
            sql=("insert into event values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)")
            values=(event_id,name,date,venue,about,'Pending','Pending','Event Created',club_id,proposal)
            mycursor.execute(sql,values)
            mydb.commit()
            st.success("Event Created!")
            st.balloons()
            mycursor.close()
            mydb.close()



def approval_status(club_id):
    # Connect to the database
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="Chandu@2605",
        database="project1"
    )

    # Function to get the event list
    def get_event_list(club_id):
        mycursor = mydb.cursor(dictionary=True)
        mycursor.execute("SELECT * FROM event WHERE club_id = %s", (club_id,))
        result = mycursor.fetchall()
        mycursor.close()
        return result

    st.subheader("Approval Status")

    # Retrieve events
    events = get_event_list(club_id)

    # Process and display events
    for event in events:
        with st.container():
            # Use columns to create a card-like layout
            col1, col2 = st.columns([2, 3])
            # Style the container to look like a card
            with col1:
                st.markdown(f"""
                    <div style="border: 1px solid #ccc; border-radius: 5px; padding: 10px; margin: 10px 0;">
                        <p style="font-size: 14px;"><b>Event Name:</b> {event['name']}</p>
                        <p style="font-size: 14px;"><b>Date:</b> {event['date']}</p>
                        <p style="font-size: 14px;"><b>Venue:</b> {event['venue']}</p>
                    </div>
                    """, unsafe_allow_html=True)

            with col2:
                with st.expander("See Details"):
                    st.write(f"About : {event['about']}")
                    st.write(f"Faculty Approval: {event['fac_approval']}")
                    st.write(f"Dean Approval: {event['dean_approval']}")
                    st.text_area("Remarks", value=event['remarks'], disabled=True)
                    if event['proposal']:
                        st.markdown(f"[View Proposal]({event['proposal']})", unsafe_allow_html=True)

                # Update remarks form for each event
                with st.form(f"update_{event['event_id']}"):
                    remarks = st.text_area("Update Remarks", key=f"remarks_{event['event_id']}")
                    submitted = st.form_submit_button("Update")
                    if submitted:
                        # Perform the update
                        mycursor = mydb.cursor()
                        mycursor.execute(
                            "UPDATE event SET remarks = %s WHERE event_id = %s",
                            (remarks, event['event_id'],)
                        )
                        mydb.commit()
                        st.success("Remarks updated successfully!")
                        mycursor.close()

    # Close the database connection
    mydb.close()


def event_registration(event_id):
    st.subheader("Event Registrations")
    mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Chandu@2605",
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
    password="Chandu@2605",
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
