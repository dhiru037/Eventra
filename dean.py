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

def clubs_info():
    mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="dhiru038",
    database="project1"
    )
    mycursor = mydb.cursor()
    mycursor.execute("select club_id, club_name, fac_id, headed_by from club")
    result0=mycursor.fetchall()
    df=pd.DataFrame(result0,columns=("Club ID","Name","Mentor ID","Club Head ID"))
    st.table(df)
    options=[item[0] for item in result0]
    club_id=st.selectbox("Select Club",options,index=None,placeholder="For more details")
    if club_id:
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

def fac_approved():
    mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="dhiru038",
    database="project1"
    )
    mycursor = mydb.cursor()
    st.subheader("Events Approved by Club Mentor")
    mycursor.execute("select * from event where fac_approval='Approved';")
    result=mycursor.fetchall()
    df = pd.DataFrame(result,columns=("Event ID","Name","Date","Venue","Description","Faculty Approval","Dean Approval","Remarks","Club ID","Proposal"))
    st.table(df)

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
    mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="dhiru038",
    database="project1"
    )
    mycursor = mydb.cursor()
    st.subheader("Events")
    mycursor.execute("select * from event;")
    result=mycursor.fetchall()
    df = pd.DataFrame(result,columns=("Event ID","Name","Date","Venue","Description","Faculty Approval","Dean Approval","Remarks","Club ID","Proposal"))
    #st.table(df)
    options=[item[-2] for item in result]
    options.insert(0,"ALL")
    options=set(options)
    choice=st.selectbox("Filter by Clubs",options)
    if choice=="ALL":
        st.subheader("All events: ")
        st.table(df)
    else:
        st.subheader("Events hosted by "+str(choice))
        mycursor.execute("select * from event where club_id=%s;",(choice,))
        result1=mycursor.fetchall()
        df1 = pd.DataFrame(result1,columns=("Event ID","Name","Date","Venue","Description","Faculty Approval","Dean Approval","Remarks","Club ID","Proposal"))
        st.table(df1)
    
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
    st.title(":rainbow[Eventra]")
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
