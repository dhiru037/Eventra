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


def clubs_info():
    # Establish database connection
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="Chandu@2605",
        database="project1"
    )
    mycursor = mydb.cursor()

    # Fetch club summary
    mycursor.execute("SELECT club_id, club_name, fac_id, headed_by FROM club")
    clubs_summary = mycursor.fetchall()

    st.markdown("""
    <style>
        .card {
            margin: 10px;
            padding: 20px;
            border-radius: 10px; /* Set background color to white */
            color: white; /* Set text color to black for better contrast */
            border: 1px solid #E1E1E1; /* Add a simple light grey border */
            box-shadow: 2px 2px 10px rgba(0,0,0,0.15);
        }
        .card:hover {
            box-shadow: 2px 2px 10px rgba(0,0,0,0.25);
        }
        .card-header {
            font-weight: bold;
            margin-bottom: 10px;
        }
    </style>
    """, unsafe_allow_html=True)

# Display each club in a card
    for club in clubs_summary:
        with st.container():
            st.markdown(f"<div class='card'><div class='card-header'>{club[1]} (ID: {club[0]})</div>Mentor ID: {club[2]}<br>Club Head ID: {club[3]}</div>", unsafe_allow_html=True)

    # Dropdown to select club for more details
    club_ids = [club[0] for club in clubs_summary]
    club_id = st.selectbox("Select Club for more details", club_ids, index=None, placeholder="Choose a club...")

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


def fac_approved():
    mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Chandu@2605",
    database="project1"
    )
    mycursor = mydb.cursor()
    st.subheader("Events Approved by Club Mentor")
    mycursor.execute("select * from event where fac_approval='Approved';")
    result = mycursor.fetchall()

    # Create a DataFrame
    df = pd.DataFrame(result, columns=("Event ID", "Name", "Date", "Venue", "Description", "Proposal","Faculty Approval", "Dean Approval", "Remarks", "Club ID"))

    # Define a style for the cards
    st.markdown("""
    <style>
    .event-card {
        margin-bottom: 10px;
        border-radius: 10px;
        padding: 16px;
        color: white;
        background-image: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        transition: transform 0.3s ease-in-out;
    }
    .event-card:hover {
        transform: translateY(-5px);
    }
    </style>
    """, unsafe_allow_html=True)

    # Loop through the DataFrame and create a card for each event
    for _, row in df.iterrows():
        st.markdown(f"""
        <div class="event-card">
            <h3>{row['Name']} (ID: {row['Event ID']})</h3>
            <p><b>Date:</b> {row['Date']}</p>
            <p><b>Venue:</b> {row['Venue']}</p>
            <p><b>Description:</b> {row['Description']}</p>
            <p><b>Faculty Approval:</b> {row['Faculty Approval']}</p>
            <p><b>Dean Approval:</b> {row['Dean Approval']}</p>
            <p><b>Remarks:</b> {row['Remarks']}</p>
            <p><a href="{row['Proposal']}" target="_blank">View Proposal</a></p>
        </div>
        """, unsafe_allow_html=True)

    with st.form("Approval"):
        st.write("Update Approval/Remarks")
        event_id=st.text_input("Event ID")
        status=st.selectbox("Status",["Pending","Edits Suggested","Approved"],index=None)
        remarks=st.text_area("Add remarks of updates on Proposal")
        reqApproval = st.form_submit_button("Update")
        if reqApproval:
            if status:
                mycursor.execute("update event set dean_approval = %s where event_id = %s",(status,event_id,))
                mydb.commit()
                st.success("Status Updated!")
            if remarks:
                mycursor.execute("update event set remarks = %s where event_id = %s",(remarks,event_id,))
                mydb.commit()
                st.success("Remarks Updated!")

    mycursor.close()
    mydb.close()



def new_events():
# Initialize session state for filter visibility
    if 'show_filters' not in st.session_state:
        st.session_state.show_filters = False

    # Establish database connection
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="Chandu@2605",
        database="project1"
    )
    mycursor = mydb.cursor()
    st.subheader("Events")

    # Fetch events data
    mycursor.execute("""
    SELECT e.*, c.club_name 
    FROM event e
    JOIN club c ON e.club_id = c.club_id;
    """)
    result = mycursor.fetchall()
    df = pd.DataFrame(result, columns=("Event ID", "Name", "Date", "Venue", "Description", "Faculty Approval", "Dean Approval", "Remarks", "Proposal", "Club ID", "Club Name"))
    
    
    # Convert 'Date' column to datetime format
    df['Date'] = pd.to_datetime(df['Date'])

    # Fetch unique filter options
    unique_clubs = df['Club ID'].unique().tolist()
    unique_dates = df['Date'].dt.date.unique().tolist()
    unique_venues = df['Venue'].unique().tolist()
    unique_dates.sort()

    # Add "ALL" options
    club_options = ['ALL'] + unique_clubs
    date_options = ['ALL'] + [date.strftime('%Y-%m-%d') for date in unique_dates]
    venue_options = ['ALL'] + unique_venues

    # Filter button
    if st.button('Filter'):
        # Toggle the display of the filters
        st.session_state.show_filters = not st.session_state.show_filters

    # Display filters if toggled
    if st.session_state.show_filters:
        selected_club = st.selectbox("Filter by Club", club_options, index=0)
        selected_date = st.selectbox("Filter by Date", date_options, index=0)
        selected_venue = st.selectbox("Filter by Venue", venue_options, index=0)

        # Apply filters
        if selected_club != "ALL":
            df = df[df['Club ID'] == selected_club]
        if selected_date != "ALL":
            df = df[df['Date'].dt.strftime('%Y-%m-%d') == selected_date]
        if selected_venue != "ALL":
            df = df[df['Venue'] == selected_venue]

    st.markdown("""
        <style>
        .card {
            margin-bottom: 10px;
            border-radius: 10px;
            color: #000000;
            padding: 15px;
            box-shadow: 2px 2px 10px rgba(0,0,0,0.3);
            background-image: linear-gradient(to right, #94B9FF, #CDFFD8);
            transition: transform .2s;
        }
        .card:hover {
            transform: scale(1.05);
        }
        .card-header {
            font-size: 20px;
            font-weight: bold;
            margin-bottom: 15px;
        }
        .card-body {
            font-size: 16px;
        }
        </style>
        """, unsafe_allow_html=True)

# Assuming 'df' is already defined and filtered based on the dropdown selection

    if df.empty:
        st.write("No events found with the selected filters.")
    else:
        for _, row in df.iterrows():
            # Create a card with hover effect
            card_id = f"card-{row['Event ID']}"
            st.markdown(f"""
                <div id="{card_id}" class="card" onmouseover="document.getElementById('{card_id}').style.boxShadow='0 4px 8px 0 rgba(0,0,0,0.2)';" 
                    onmouseout="document.getElementById('{card_id}').style.boxShadow='0 2px 4px 0 rgba(0,0,0,0.2)';">
                    <h2>{row['Name']} (Club: {row['Club Name']})</h2>
                </div>
                """, unsafe_allow_html=True)
            
            # Use an expander to show details when clicked
            with st.expander("Show Details"):
                st.write(f"**Date:** {row['Date'].strftime('%Y-%m-%d')}")
                st.write(f"**Venue:** {row['Venue']}")
                st.write(f"**Description:** {row['Description']}")
                st.write(f"**Faculty Approval:** {row['Faculty Approval']}")
                st.write(f"**Dean Approval:** {row['Dean Approval']}")
                st.write(f"**Remarks:** {row['Remarks']}")
                if row['Proposal']:
                    st.markdown(f"[View Proposal]({row['Proposal']})", unsafe_allow_html=True)

    st.markdown('### Approvals')
    
    with st.form("Approval"):
        st.write("Update Approval/Remarks")
        event_id=st.text_input("Event ID")
        status=st.selectbox("Status",["Pending","Edits Suggested","Approved"],index=None)
        remarks=st.text_area("Add remarks of updates on Proposal")
        reqApproval = st.form_submit_button("Update")
        if reqApproval:
            if status:
                mycursor.execute("update event set dean_approval = %s where event_id = %s",(status,event_id,))
                mydb.commit()
                st.success("Status Updated!")
            if remarks:
                mycursor.execute("update event set remarks = %s where event_id = %s",(remarks,event_id,))
                mydb.commit()
                st.success("Remarks Updated!")

    mycursor.close()
    mydb.close()
        

def app():
    col1, col2, col3 = st.columns([1, 2, 1])

    # Place the image in the middle column for center alignment
    with col2:
        logo_path = 'images/logo.png'  # Replace with your actual path to the logo file
        st.image(logo_path, width=300, output_format='PNG')  # Set width and format for the image

    # Add a divider after the logo if needed
    st.divider()
    st.header("Dean Dashboard")
    st.divider()
    options=["Clubs Info","Newly Created Events","Mentor Approved"]
    choice=st.sidebar.selectbox("Select option",options,index=None,placeholder="Choose")
    if choice == "Clubs Info":
        clubs_info()
    elif choice == "Newly Created Events":
        new_events()
    elif choice == "Mentor Approved":
        fac_approved()
    
    

if __name__ == "__main__":
    app()