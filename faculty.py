import streamlit as st
import mysql.connector
import pandas as pd 

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

def get_club_id(fac_id):
    mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Chandu@2605",
    database="project1"
    )
    mycursor = mydb.cursor()
    mycursor.execute("select club_id from faculty where faculty_id=%s",(fac_id,))
    club_id=mycursor.fetchall()[0][0]
    mycursor.close()
    mydb.close()
    return club_id

def club_info(club_id):
    # Connect to the database
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="Chandu@2605",
        database="project1"
    )
    
    def get_club_details(club_id):
        with mydb.cursor(dictionary=True) as mycursor:
            mycursor.execute("SELECT club_name, vertical, about, image_url FROM club WHERE club_id=%s", (club_id,))
            return mycursor.fetchone()

    # Function to get mentor details
    def get_mentor_details(club_id):
        with mydb.cursor(dictionary=True) as mycursor:
            mycursor.execute("SELECT fac_name, faculty_id, phone_no, email, image_url FROM faculty WHERE club_id=%s", (club_id,))
            return mycursor.fetchone()

    # Function to get head details
    def get_head_details(club_id):
        with mydb.cursor(dictionary=True) as mycursor:
            mycursor.execute("SELECT name, head_id, phone_no, email, image_url FROM club_head WHERE club_id=%s", (club_id,))
            return mycursor.fetchone()

    # Retrieve all details
    club_details = get_club_details(club_id)
    mentor_details = get_mentor_details(club_id)
    head_details = get_head_details(club_id)

    if not club_details or not mentor_details or not head_details:
        st.error('No details available for the selected club.')
        return  # Exit the function if any details are missing
    
    if club_id:
        st.markdown("""
    <style>
    .flip-card {
      background-color: transparent;
      width: 225px;
      height: 250px;
      perspective: 1000px;
      margin: auto;
      border-radius: 15px;
      overflow: hidden;
    }

    .flip-card-inner {
      position: relative;
      width: 100%;
      height: 100%;
      text-align: center;
      transition: transform 0.6s;
      transform-style: preserve-3d;
      box-shadow: 0 4px 8px 0 rgba(0,0,0,0.2);
      border-radius: 15px;
    }

    .flip-card:hover .flip-card-inner {
      transform: rotateY(180deg);
    }

    .flip-card-front, .flip-card-back {
      position: absolute;
      width: 100%;
      height: 100%;
      backface-visibility: hidden;
      border-radius: 15px;
    }

    .flip-card-front {
      background-color: #bbb;
      color: black;
      z-index: 2;
      display: flex;
      align-items: center;
      justify-content: center;
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
    }

    .flip-card-front img, .flip-card-back img {
        width: 100%;
        height: 100%;
        object-fit: cover;
        border-radius: 15px;
    }
    </style>
    """, unsafe_allow_html=True)

    st.subheader(f"{club_details['club_name']}")

    col1, col2, col3 = st.columns(3)

    # Flip card for Club Details
    with col1:
        st.markdown(f"""
        <div class="flip-card">
            <div class="flip-card-inner">
                <div class="flip-card-front">
                    <img src="{club_details['image_url']}" alt="Club Image">
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
                    <img src="{mentor_details['image_url']}" alt="Mentor Image">
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
                    <img src="{head_details['image_url']}" alt="Head Image">
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

        mycursor.close()

    # Close the database connection
    mydb.close()


def approval_status(club_id):
    st.subheader("Approval Status")

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

    # Retrieve events
    events = get_event_list(club_id)

    # Custom CSS for flip cards and cards
    flip_card_css = """
    <style>
        .flip-card {
            background-color: transparent;
            width: 220px;
            height: 380px;
            perspective: 1000px;
            margin-bottom: 20px;
            border-radius: 10px;
            overflow: hidden;
        }
        .flip-card-inner {
            position: relative;
            width: 100%;
            height: 100%;
            text-align: center;
            transition: transform 0.6s;
            transform-style: preserve-3d;
        }
        .flip-card:hover .flip-card-inner {
            transform: rotateY(180deg);
        }
        .flip-card-front, .flip-card-back {
            position: absolute;
            width: 100%;
            height: 100%;
            backface-visibility: hidden;
            border-radius: 10px;
            display: flex;
            align-items: center;
            justify-content: center;
            flex-direction: column;
            padding: 10px;
        }
        .flip-card-front {
            background-image: linear-gradient(to right, #ff7e5f, #feb47b); 
            color: white;
        }
        .flip-card-back {
            background-color: black;
            color: white;
            transform: rotateY(180deg);
            
        }
    </style>
    """
    st.markdown(flip_card_css, unsafe_allow_html=True)

    # Process and display events
    for event in events:
        with st.container():
            col1, col2 = st.columns([1, 2])

            with col1:
                # Display event details in a flip card component
                st.markdown(f"""
                    <div class="flip-card">
                        <div class="flip-card-inner">
                            <div class="flip-card-front">
                                <h4>{event['name']}</h4>
                            </div>
                            <div class="flip-card-back">
                                <p><b>Event ID:</b> {event['event_id']}</p>
                                <p><b>Date:</b> {event['date']}</p>
                                <p><b>Venue:</b> {event['venue']}</p>
                                <p><b>Faculty Approval:</b> {event['fac_approval']}</p>
                                <p><b>Dean Approval:</b> {event['dean_approval']}</p>
                            </div>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)

            with col2:
                # Form to update event approval status and remarks
                with st.form(key=f"form_{event['event_id']}"):
                    st.write(f"Update for Event ID: {event['event_id']}")
                    if event['proposal']:
                        st.markdown(f"[View Proposal]({event['proposal']})", unsafe_allow_html=True)
                    new_status = st.selectbox(
                        "Status",
                        ["Pending", "Edits Suggested", "Approved"],
                        key=f"status_{event['event_id']}"
                    )
                    new_remarks = st.text_area("Remarks", key=f"remarks_{event['event_id']}")
                    submit_button = st.form_submit_button(label="Update")

                    if submit_button:
                        # Update the database with new status and remarks
                        mycursor = mydb.cursor()
                        if new_status:
                            mycursor.execute(
                                "UPDATE event SET fac_approval = %s WHERE event_id = %s",
                                (new_status, event['event_id'])
                            )
                        if new_remarks:
                            mycursor.execute(
                                "UPDATE event SET remarks = %s WHERE event_id = %s",
                                (new_remarks, event['event_id'])
                            )
                        mydb.commit()
                        mycursor.close()
                        st.success(f"Event ID {event['event_id']} updated successfully!")

    # Close the database connection
    mydb.close()

    # Close the database connection
    mydb.close()


def app():
    col1, col2, col3 = st.columns([1, 2, 1])

    # Place the image in the middle column for center alignment
    with col2:
        logo_path = 'images/logo.png'  # Replace with your actual path to the logo file
        st.image(logo_path, width=300, output_format='PNG')  # Set width and format for the image

    # Add a divider after the logo if needed
    st.divider()
    st.header("Club Mentor Dashboard")
    st.divider()
    fac_id=st.sidebar.text_input("Faculty ID")
    
    if fac_id:
        club_id=get_club_id(fac_id)
        st.sidebar.title("Navigation")
        options = ["Club Info","Approval Status"]
        choice = st.sidebar.selectbox("Selcet Option",options)

        if choice== "Club Info":
            club_info(club_id)
        elif choice == "Approval Status":
            approval_status(club_id)


if __name__ == "__main__":
    app()