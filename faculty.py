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

    mycursor.execute("select event_id, name, date, venue, about, fac_approval, dean_approval, remarks, proposal from event where club_id=%s",(club_id,))
    result=mycursor.fetchall()
    mycursor.close()
    mydb.close()
    return result

def get_club_id(fac_id):
    mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="dhiru038",
    database="project1"
    )
    mycursor = mydb.cursor()
    mycursor.execute("select club_id from faculty where faculty_id=%s",(fac_id,))
    club_id=mycursor.fetchall()[0][0]
    mycursor.close()
    mydb.close()
    return club_id

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

def approval_status(club_id):
    st.subheader("Approval Status")
    result=get_event_list(club_id)
    df = pd.DataFrame(result,columns=("Event ID","Name","Date","Venue","Description","Faculty Approval","Dean Approval","Remarks","Proposal"))
    st.table(df)
    mydb = mysql.connector.connect(
    host = "localhost",
    user = "root",
    password = "dhiru038",
    database = "project1"
    )
    mycursor = mydb.cursor()
    with st.form("Approval"):
        st.write("Update Approval/Remarks")
        event_id=st.text_input("Event ID")
        status=st.selectbox("Status",["Pending","Edits Suggested","Approved"],index=None)
        remarks=st.text_area("Add remarks of updates on Proposal")
        reqApproval = st.form_submit_button("Update")
        if reqApproval:
            if status:
                mycursor.execute("update event set fac_approval = %s where event_id = %s",(status,event_id,))
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