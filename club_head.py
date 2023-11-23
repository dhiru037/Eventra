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
    st.subheader(f"Event Registrations for {event_id}")
    
    # Connect to the database
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="Chandu@2605",
        database="project1"
    )

    # Fetch event registration details
    mycursor = mydb.cursor()
    mycursor.execute("SELECT srn, name, phone_no, email, date FROM participant WHERE event_id=%s;", (event_id,))
    result = mycursor.fetchall()
    
    # Close the cursor and database connection
    mycursor.close()
    mydb.close()

    # Convert to DataFrame for better presentation in Streamlit
    if result:
        df = pd.DataFrame(result, columns=["SRN", "Name", "Phone No", "Email", "Date of Registration"])
        # Use Streamlit's built-in functionality to display data as a table
        st.dataframe(df.style.format(subset=['Email'], formatter=lambda x: f'{x}').set_properties(**{
            'background-color': 'black',
            'color': 'white',
            'border-color': 'gray'
        }), height=600)
    else:
        st.warning(f"No registrations found for event {event_id}.")



def club_info(club_id):
    # Connect to the database
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="Chandu@2605",
        database="project1"
    )
    
    # Function to get club details
    def get_club_details(club_id):
        mycursor = mydb.cursor(dictionary=True)
        mycursor.execute("SELECT club_name, vertical, about FROM club WHERE club_id=%s", (club_id,))
        result = mycursor.fetchone()
        mycursor.close()
        return result

    # Function to get mentor details
    def get_mentor_details(club_id):
        mycursor = mydb.cursor(dictionary=True)
        mycursor.execute("SELECT fac_name, faculty_id, phone_no, email FROM faculty WHERE club_id=%s", (club_id,))
        result = mycursor.fetchone()
        mycursor.close()
        return result

    # Function to get head details
    def get_head_details(club_id):
        mycursor = mydb.cursor(dictionary=True)
        mycursor.execute("SELECT name, head_id, phone_no, email FROM club_head WHERE club_id=%s", (club_id,))
        result = mycursor.fetchone()
        mycursor.close()
        return result
    
    def get_club_image_url(club_id):
        mycursor = mydb.cursor()
        mycursor.execute("SELECT image_url FROM club WHERE club_id = %s", (club_id,))
        result = mycursor.fetchone()
        mycursor.close()
        return result[0] if result else None
    
    def get_mentor_image_url(club_id):
        mycursor = mydb.cursor()
        mycursor.execute("SELECT image_url FROM faculty WHERE club_id = %s", (club_id,))
        result = mycursor.fetchone()
        mycursor.close()
        return result[0] if result else None
    
    def get_club_head_image_url(club_id):
        mycursor = mydb.cursor()
        mycursor.execute("SELECT image_url FROM club_head WHERE club_id = %s", (club_id,))
        result = mycursor.fetchone()
        mycursor.close()
        return result[0] if result else None

# Then use it in your Streamlit app
    club_image_url = get_club_image_url(club_id)
    mentor_image_url = get_mentor_image_url(club_id)
    club_head_image_url = get_club_head_image_url(club_id)
    club_details = get_club_details(club_id)
    mentor_details = get_mentor_details(club_id)
    head_details = get_head_details(club_id)

    st.subheader(f"Welcome, {club_details['club_name']}")

    # Custom CSS for the flip card
    flip_card_style = """
    <style>
    .flip-card {
      background-color: transparent;
      width: 225px;
      height: 250px;
      perspective: 1000px;
      margin: auto;
      border-radius: 15px; /* Rounded borders for the flip card */
      overflow: hidden; /* Ensures the inner content also gets rounded corners */
    }

    .flip-card-inner {
      position: relative;
      width: 100%;
      height: 100%;
      text-align: center;
      transition: transform 0.6s;
      transform-style: preserve-3d;
      box-shadow: 0 4px 8px 0 rgba(0,0,0,0.2);
      border-radius: 15px; /* Rounded borders for the inner card */
    }

    .flip-card:hover .flip-card-inner {
      transform: rotateY(180deg);
    }

    .flip-card-front, .flip-card-back {
      position: absolute;
      width: 100%;
      height: 100%;
      backface-visibility: hidden;
      border-radius: 15px; /* Rounded borders for the inner card */
    }

    .flip-card-front {
      background-color: #bbb;
      color: black;
      z-index: 2;
      display: flex;
      align-items: center;
      justify-content: center;
      border-radius: 15px; /* Rounded borders for the inner card */
    }

    .flip-card-back {
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        background-image: linear-gradient(to right, #2980b9, #6dd5fa);
        color: white;
        transform: rotateY(180deg);
        z-index: 1;
        padding: 20px;
        border-radius: 15px; /* Rounded borders for the inner card */
    }

    .flip-card-front img {
        width: 100%;
        height: 100%;
        object-fit: cover; /* Cover the box area, may crop the image */
        object-position: center; /* Center the image within the box */
    }
    </style>
    """

    # Inject custom CSS for flip card
    st.markdown(flip_card_style, unsafe_allow_html=True)

    # Process and display club information using flip cards
    with st.container():
        col1, col2, col3 = st.columns(3)

        # Flip card for Club Details
        with col1:
            st.markdown(f"""
            <div class="flip-card">
                <div class="flip-card-inner">
                    <div class="flip-card-front">
                        <img src="{club_image_url}" alt="Club Image" style="width:300px;height:200px;">
                    </div>
                    <div class="flip-card-back">
                        <h4>Club Details</h4>
                        <p>ID: {club_id}</p>
                        <p>Name: {club_details['club_name']}</p>
                        <p>Vertical: {club_details['vertical']}</p>
                        <p>About: {club_details['about']}</p>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)

        # Flip card for Mentor Details
        with col2:
            st.markdown(f"""
            <div class="flip-card">
                <div class="flip-card-inner">
                    <div class="flip-card-front">
                        <img src="{mentor_image_url}" alt="Mentor Image" style="width:300px;height:200px;">
                    </div>
                    <div class="flip-card-back">
                        <h4>Mentor Details</h4>
                        <p>Faculty ID: {mentor_details['faculty_id']}</p>
                        <p>Name: {mentor_details['fac_name']}</p>
                        <p>Contact: {mentor_details['phone_no']}</p>
                        <p>Email: {mentor_details['email']}</p>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)

        # Flip card for Head Details
        with col3:
            st.markdown(f"""
            <div class="flip-card">
                <div class="flip-card-inner">
                    <div class="flip-card-front">
                        <img src="{club_head_image_url}" alt="Head Image" style="width:300px;height:200px;">
                    </div>
                    <div class="flip-card-back">
                        <h4>Head Details</h4>
                        <p>Member ID: {head_details['head_id']}</p>
                        <p>Name: {head_details['name']}</p>
                        <p>Contact: {head_details['phone_no']}</p>
                        <p>Email: {head_details['email']}</p>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)

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
