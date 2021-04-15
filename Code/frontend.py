import streamlit as st
import pandas as pd
import hashlib
import mysql.connector as mysql
from streamlit import caching
import os

def make_hashes(password):
	return hashlib.sha256(str.encode(password)).hexdigest()

def check_hashes(password,hashed_text):
	if make_hashes(password) == hashed_text:
		return hashed_text
	return False

# Database Details
sportify = {"database": "sportify_db"
			,"account": "accounts_db"
			,"admin": "administrator_db"
			,"borrow": "borrowequip_db"
			,"coach": "coach_db"
			,"collegeEquip": "collegeequip_db"
			,"collegeOrder": "collegeorders_db"
			,"event": "events_db"
			,"favourite": "favorite_db"
			,"friend": "friend_db"
			,"issue": "issueequip_db"
			,"judge": "judges_db"
			,"participate": "participation_db"
			,"referee": "referee_db"
			,"sports": "sports_db"
			,"trains": "trains_db"
			,"user": "user_db"
			,"userEquip": "userequip_db"
			,"userOrder": "userorders_db"
			,"vendor": "vendor_db"
			,"venue": "venue_db"
			,"booking": "venuebooking_db"
			}

# DB Management
db = mysql.connect(
    host = "127.0.0.1",
    user = "root",
    passwd = "calmag",
    # passwd = os.environ.get("DB_PASSWORD"),
    database = sportify["database"],
    auth_plugin="mysql_native_password"
)
cursor = db.cursor()

# DB  Functions
def create_usertable():
	cursor.execute('CREATE TABLE IF NOT EXISTS accounts_db(Username TEXT, Account_Password TEXT, User_Type TEXT);')


def add_userdata(username,password,user_type):
	cursor.execute('INSERT INTO accounts_db(Username, Account_Password, User_Type) VALUES (%s,%s,%s);',(username,password,user_type))
	db.commit()

def login_user(username,password,user_type):
	cursor.execute("SELECT * FROM accounts_db WHERE Username= %s AND Account_Password= %s AND User_type= %s;",(username,password,user_type))
	data = cursor.fetchall()
	return data

# All Queries

# Vendor
def VenderQueries(username):
	#cursor.execute('CREATE TABLE IF NOT EXISTS vendor_db(Vendor_ID INT NOT NULL PRIMARY KEY AUTO_INCREMENT, Username TEXT, Shop_name VARCHAR(255) NOT NULL, Email VARCHAR(255) NOT NULL, Phone_number CHAR(15) NOT NULL, Equipments_repaired INT DEFAULT 0, Address VARCHAR(255) NOT NULL);')
	cursor.execute("SELECT * FROM vendor_db WHERE username= %s",(username,))
	profile_created = cursor.fetchall()
	if(profile_created):
		queries = ["View Profile", "Update Profile", "Check College Orders", "Check User Orders"]
	else:
		queries = ["Update Profile", "View Profile", "Check College Orders", "Check User Orders"]

	query = st.selectbox("Query", queries)

	if query == "Update Profile":
		st.subheader(query)
		shop_name = st.text_input("Shop Name", max_chars=255)
		email = st.text_input("Email", max_chars=255)
		phone = st.text_input("Phone", max_chars=15)
		address = st.text_input("Address", max_chars=255)
	
		if st.button("Update"):
			if not profile_created:
				cursor.execute('INSERT INTO vendor_db(Username, Shop_name, Email, Phone_number, Address) VALUES (%s,%s,%s,%s,%s)',(username,shop_name,email,phone,address))
				db.commit()
				st.success("You have successfully created a valid Account")
				profile_created = True
			else:
				cursor.execute('UPDATE vendor_db SET Shop_name = %s, Email = %s, Phone_number = %s, Address = %s WHERE Username = %s',(shop_name,email,phone,address,username))
				db.commit()
				st.success("You have successfully updated your account")
	
	elif query == "View Profile":
		cursor.execute("SELECT * FROM vendor_db WHERE username= %s",(username,))
		profile = cursor.fetchall()
		st.text("Username: {}".format(profile[0][1]))
		st.text("Shop Name: {}".format(profile[0][2]))
		st.text("Email: {}".format(profile[0][3]))
		st.text("Phone: {}".format(profile[0][4]))
		st.text("Address: {}".format(profile[0][6]))

	elif query == "Check College Orders":
		order_type = st.selectbox("Type of Order", ["Buy Order", "Repair Order"])
		if order_type == "Repair Order":
			cursor.execute("SELECT Vendor_ID FROM vendor_db WHERE username= %s",(username,))
			vendor_id = cursor.fetchall()[0][0]
			cursor.execute("SELECT * FROM collegeorders_db WHERE Vendor_ID= {} AND Type= 'Repair'".format(vendor_id,))
			buy_order = cursor.fetchall()
			buy_order = pd.DataFrame(buy_order, columns=["Order_ID", "Type", "Order_Status", "Equipment_ID", "Vendor_ID"])
			st.dataframe(buy_order)
			selected_indices = st.multiselect('Select rows:', buy_order.Order_ID)

			if st.button("Update Status"):
				for index in selected_indices:
					cursor.execute('UPDATE collegeorders_db SET Order_Status = "Complete" WHERE Equipment_ID = {}'.format(index))
					db.commit()
					cursor.execute('UPDATE collegeequip_db SET Ongoing_Repair = 0, Cond = "Good" WHERE Equipment_ID = {}'.format(index))
					db.commit()
					st.success("Successfully updated the order status")
		
		elif order_type == "Buy Order":
			cursor.execute("SELECT Vendor_ID FROM vendor_db WHERE username= %s",(username,))
			vendor_id = cursor.fetchall()[0][0]
			cursor.execute("SELECT * FROM collegeorders_db WHERE Vendor_ID= {} AND Type= 'Buy'".format(vendor_id,))
			buy_order = cursor.fetchall()
			buy_order = pd.DataFrame(buy_order, columns=["Order_ID", "Type", "Order_Status", "Equipment_ID", "Vendor_ID"])
			st.dataframe(buy_order)
			selected_indices = st.multiselect('Select rows:', buy_order.Order_ID)

			if st.button("Update Status"):
				for index in selected_indices:
					cursor.execute('UPDATE collegeorders_db SET Order_Status = "Complete" WHERE Equipment_ID = {}'.format(index))
					db.commit()
					cursor.execute('UPDATE collegeequip_db SET Ongoing_Repair = 0, Cond = "Good" WHERE Equipment_ID = {}'.format(index))
					db.commit()
					st.success("Successfully updated the order status")


	elif query == "Check User Orders":
		order_type = st.selectbox("Type of Order", ["Buy Order", "Repair Order"])
		if order_type == "Repair Order":
			cursor.execute("SELECT Vendor_ID FROM vendor_db WHERE username= %s",(username,))
			vendor_id = cursor.fetchall()[0][0]
			cursor.execute("SELECT * FROM userorders_db WHERE Vendor_ID= {} AND Type= 'Repair'".format(vendor_id,))
			buy_order = cursor.fetchall()
			buy_order = pd.DataFrame(buy_order, columns=["Order_ID", "Type", "Order_Status", "User_ID", "Equipment_ID", "Vendor_ID"])
			st.dataframe(buy_order)
			selected_indices = st.multiselect('Select rows:', buy_order.Equipment_ID)

			if st.button("Update Status"):
				for index in selected_indices:
					cursor.execute('UPDATE userorders_db SET Order_Status = "Complete" WHERE Equipment_ID = {}'.format(index))
					db.commit()
					cursor.execute('UPDATE userequip_db SET Ongoing_Repair = 0, Cond = "Good" WHERE Equipment_ID = {}'.format(index))
					db.commit()
					st.success("Successfully updated the order status")
		
		elif order_type == "Buy Order":
			cursor.execute("SELECT Vendor_ID FROM vendor_db WHERE username= %s",(username,))
			vendor_id = cursor.fetchall()[0][0]
			cursor.execute("SELECT * FROM userorders_db WHERE Vendor_ID= {} AND Type= 'Buy'".format(vendor_id,))
			buy_order = cursor.fetchall()
			buy_order = pd.DataFrame(buy_order, columns=["Order_ID", "Type", "Order_Status", "User_ID", "Equipment_ID", "Vendor_ID"])
			st.dataframe(buy_order)
			selected_indices = st.multiselect('Select rows:', buy_order.Equipment_ID)

			if st.button("Update Status"):
				for index in selected_indices:
					cursor.execute('UPDATE userorders_db SET Order_Status = "Complete" WHERE Equipment_ID = {}'.format(index))
					db.commit()
					cursor.execute('UPDATE userequip_db SET Ongoing_Repair = 0, Cond = "Good" WHERE Equipment_ID = {}'.format(index))
					db.commit()
					st.success("Successfully updated the order status")

def Coach_Queries(username):
	cursor.execute("SELECT * from coach_db WHERE username = %s;", (username,))
	coach_profile_created = cursor.fetchall()
	if(coach_profile_created):
		queries = ["View Profile", "Update Profile", "Change Availability Status", "Check Current Students", "Check Feedbacks"]
	else:
		queries = ["Update Profile", "View Profile",  "Change Availability Status", "Check Current Students", "Check Feedbacks"]

	query = st.selectbox("Query", queries)

	if query == "Update Profile":
		st.subheader(query)
		first_name = st.text_input("First Name", max_chars=9)
		last_name = st.text_input("Last Name", max_chars=13)
		gender = st.text_input("Gender", max_chars=6)
		email = st.text_input("Email", max_chars=31)
		phone_number = st.text_input("Phone Number", max_chars = 12)
		date_of_birth = st.text_input("Date of Birth (YYYY-MM-DD)")
		intial_availability_status = "Available"
		specialize_sport_id = st.text_input("Specialization Sport ID")
	
		if st.button("Update"):
			if not coach_profile_created:
				cursor.execute('INSERT INTO coach_db(First_Name, Last_Name, Gender, Email, Phone_number, Date_of_Birth, Availability_Status, Specialization_Sport_ID, username) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s);',(first_name, last_name, gender, email, phone_number, date_of_birth, intial_availability_status, specialize_sport_id, username))
				db.commit()
				st.success("You have successfully created a valid Account")
				coach_profile_created = True
			else:
				cursor.execute('UPDATE coach_db SET First_Name = %s, Last_Name = %s, Gender = %s, Email = %s, Phone_number = %s, Date_of_Birth = %s, Specialization_Sport_ID = %s WHERE username = %s;',(first_name, last_name, gender, email, phone_number, date_of_birth, specialize_sport_id))
				db.commit()
				st.success("You have successfully updated your account")
	
	elif query == "View Profile":
		cursor.execute("SELECT cdb.username, cdb.First_Name, cdb.Last_Name, cdb.Gender, cdb.Email, cdb.Phone_number, cdb.Date_of_Birth, cdb.Availability_Status,sdb.Name as Sport_Name FROM sports_db sdb NATURAL JOIN (SELECT * FROM coach_db WHERE username = %s) as cdb WHERE sdb.Sport_ID = cdb.Specialization_Sport_ID;",(username,))
		coach_profile = cursor.fetchall()
		st.text("Username : {}".format(coach_profile[0][0]))
		st.text("First Name: {}".format(coach_profile[0][1]))
		st.text("Last Name: {}".format(coach_profile[0][2]))
		st.text("Gender: {}".format(coach_profile[0][3]))
		st.text("Email: {}".format(coach_profile[0][4]))
		st.text("Phone_number: {}".format(coach_profile[0][5]))
		st.text("Date of Birth : {}".format(coach_profile[0][6]))
		st.text("Current Availability Status : {}".format(coach_profile[0][7]))
		st.text("Specialized Sport : {}".format(coach_profile[0][8]))

	elif query == "Change Availability Status":
		st.subheader(query)
		cursor.execute('SELECT * FROM coach_db WHERE username = %s;', (username,))
		coach_record = cursor.fetchall()
		coach_id = coach_record[0][0]
		st.text("Your current Availability Status : {}".format(coach_record[0][7]))
		choices = ['Available', 'Not Available']
		choice_button = st.radio('Set availability status to :', choices)

		if(st.button("Confirm Changes")):
			if(choice_button == 'Available'):
				cursor.execute("UPDATE coach_db SET Availability_Status = 'Available' WHERE Coach_ID = %s;", (coach_id,))
				db.commit()
				st.success("You availability status has been set to 'Available' :thumbsup:")
			else:
				cursor.execute("UPDATE coach_db SET Availability_Status = 'Not Available' WHERE Coach_ID = %s;", (coach_id,))
				db.commit()
				st.success("You availability status has been set to 'Not Available' :thumbsup:")

	elif query == "Check Current Students":
		st.subheader(query)
		cursor.execute("SELECT * FROM coach_db where username = %s;", (username,))
		coach_id = cursor.fetchall()[0][0]
		cursor.execute("SELECT udb.First_Name, udb.Last_Name, udb.Email, udb.Phone_Number, udb.Date_of_Birth, udb.Gender, udb.Address, trains_db.Start_Date from user_db udb NATURAL JOIN trains_db WHERE trains_db.Coach_ID = %s;", (coach_id,))
		current_students = cursor.fetchall()
		current_students = pd.DataFrame(current_students, columns=["First Name", "Last Name", "Email", "Phone_Number", "Date_of_Birth", "=Gender", "Address", "Training Start Date"])
		st.dataframe(current_students)
	elif query == "Check Feedbacks":
		st.subheader(query)
		cursor.execute("SELECT * FROM coach_db where username = %s;", (username,))
		coach_id = cursor.fetchall()[0][0]
		cursor.execute("SELECT udb.First_Name, udb.Last_Name, udb.Gender, udb.Phone_Number, udb.Email, udb.Address, fbck.Feedback_Text FROM user_db udb NATURAL JOIN coachfeedback_db fbck where Coach_ID = %s;", (coach_id,))
		feedbacks = cursor.fetchall()
		feedbacks = pd.DataFrame(feedbacks, columns=["First Name", "Last Name", "Gender", "Phone_Number", "Email", "Address", "Feedback"])
		st.dataframe(feedbacks)
		
def user_queries(username):
    cursor.execute("SELECT * FROM user_db WHERE username= %s", (username,))
    profile_created = cursor.fetchall()
    if(profile_created):
        queries = ["View Profile", "Update Profile", "Add An Event", "Choose An Event", "Place An order",
               "Take College Inventory", "Borrow From Peers","Hire Coach"]
    else:
        queries = ["Update Profile","View Profile", "Add An Event", "Choose An Event", "Place An order",
               "Take College Inventory", "Borrow From Peers","Hire Coach"]
    query = st.selectbox('QUERY', queries)

    if(query == "Update Profile"):
        st.subheader(query)
        first_name = st.text_input("First Name",max_chars=255)
        last_name = st.text_input("last Name",max_chars=255)
        email = st.text_input("Email",max_chars=255)
        phone_number = st.text_input("Phone Number",max_chars=15)
        dob = st.text_input('Date of Birth - format(YY_MM_DD)',max_chars=255)
        gender = st.text_input("Gender",max_chars=255)
        date_of_joining = st.text_input("Date of Joining - format(YY_MM_DD)",max_chars=255)
        address = st.text_input("Address",max_chars=255)

        if(st.button("Update")):
            if not profile_created:
                cursor.execute(
                    'INSERT INTO user_db (username, First_name, Last_name, Email, Phone_Number, Date_of_Birth,Gender,Date_of_Joining,Address) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)',
                    (username, first_name,last_name,email,phone_number,dob,gender,date_of_joining,address))
                db.commit()
                st.success("You have successfully created a valid Account")
                profile_created = True
            else:
                cursor.execute(
                    'UPDATE user_db SET First_name = %s, Last_name = %s, Email = %s, Phone_Number = %s, Date_of_Birth = %s, Gender = %s, Date_of_Joining = %s, Address = %s WHERE Username = %s',
                    (first_name,last_name,email,phone_number,dob,gender,date_of_joining,address))
                db.commit()
                st.success("You have successfully updated your account")

    if (query == "View Profile"):
        st.subheader(query)
        cursor.execute("SELECT * FROM user_db WHERE username= %s", (username,))
        profile = cursor.fetchall()
        st.text("User ID: {}".format(profile[0][0]))
        st.text("First Name: {}".format(profile[0][1]))
        st.text("Last Name: {}".format(profile[0][2]))
        st.text("Email: {}".format(profile[0][3]))
        st.text("Phone Number: {}".format(profile[0][4]))
        st.text("Date of Birth: {}".format(profile[0][5]))
        st.text("Gender: {}".format(profile[0][6]))
        st.text("Date of Joining: {}".format(profile[0][7]))
        st.text("Address: {}".format(profile[0][8]))

    def check_venue_availability(start_datetime, end_datetime, venue_id):
        query_input = (venue_id, start_datetime, start_datetime, end_datetime, end_datetime, start_datetime, end_datetime,)
        cursor.execute(
            "SELECT COUNT(*) FROM (SELECT * FROM venuebooking_db WHERE Venue_ID = %s AND ( (%s >= Start_DateTime AND %s <= End_DateTime) OR (%s >= Start_DateTime AND %s <= End_DateTime) OR (%s <= Start_DateTime AND %s >= End_DateTime))) as A;",
            query_input)
        l = cursor.fetchall()
        cnt = l[0][0]
        if (cnt == 0):
            return True
        else:
            return False

    if(query == "Add An Event"):
        start_datetime = st.text_input("Start Datetime - format(YYYY-MM-DD 'space' HH:MM:SS)",max_chars=255)
        end_datetime = st.text_input("End Datetime - format(YYYY-MM-DD 'space' HH:MM:SS)",max_chars=255)

        event_name = st.text_input("Event Name", max_chars=255)
        participant_limit = st.text_input("Participation Limit", max_chars=255)


        # show all venue available.
        cursor.execute("SELECT Venue_ID,Venue_Name,Sport_ID from venue_db")
        temp = cursor.fetchall()
        temp = pd.DataFrame(temp,columns=["Venue_ID","Venue_Name","Sport_ID"])
        st.dataframe(temp)
        venue_id = st.multiselect("Select rows: ",temp.Venue_ID)

        if(st.button("NEXT1")):
            venue_id = str(venue_id[0])
            if(not check_venue_availability(start_datetime,end_datetime,venue_id)):
               st.success("Sorry Venue not available in the given time slot")
            else:
                with st.spinner("TAKING DATA"):
                    cursor.execute("SELECT Sport_ID FROM venue_db WHERE Venue_ID = %s", (venue_id,))
                    sports_id = cursor.fetchall()[0][0]

                    cursor.execute("SElECT user_id FROM user_db WHERE username = %s;",(username,))
                    temp = cursor.fetchall()
                    user_id = temp[0][0]

                    query_booking = "INSERT INTO events_db (Event_Name,Start_Datetime,End_Datetime,Participant_Limit,Organizer_ID,Venue_ID,Sport_ID) VALUES (%s,%s,%s,%s,%s,%s,%s);"
                    query_data = (event_name, start_datetime, end_datetime, participant_limit, user_id, venue_id, sports_id,)
                    cursor.execute(query_booking, query_data)
                    db.commit()
                    cursor.execute("INSERT INTO participation_db VALUES (%s, %s);", (user_id,cursor.lastrowid))
                    db.commit()
                    cursor.execute("INSERT INTO venuebooking_db VALUES (%s, %s, %s);", (venue_id, start_datetime, end_datetime))
                    db.commit()
                    st.success("VENUE BOOKED SUCCESSFULLY")

    def check_college_equipment_availability(college_equipment_id, issue_datetime, return_datetime):
        query_input = (
        college_equipment_id, issue_datetime, issue_datetime, return_datetime, return_datetime, issue_datetime,
        return_datetime)
        cursor.execute(
            "SELECT COUNT(*) FROM (SELECT * FROM issueequip_db WHERE Equipment_ID = %s AND ( (%s >= Issue_Date_Time AND %s <= Return_Date_Time) OR (%s >= Issue_Date_Time AND %s <= Return_Date_Time) OR (%s <= Issue_Date_Time AND %s >= Return_Date_Time))) as A;",
            query_input)
        l = cursor.fetchall()
        cnt = l[0][0]
        if (cnt == 0):
            return True
        else:
            return False

    if(query == 'Take College Inventory'):
        issue_datetime = st.text_input("Issue Datetime - format(YYYY-MM-DD 'space' HH:MM:SS)",max_chars=255)
        return_datetime = st.text_input("Datetime Datetime - format(YYYY-MM-DD 'space' HH:MM:SS)",max_chars=255)

        cursor.execute("SELECT Equipment_ID,Name FROM collegeequip_db")
        temp = cursor.fetchall()
        temp = pd.DataFrame(temp,columns=['Equipment_ID','Name'])
        st.dataframe(temp)
        college_equipment_id = st.multiselect("Select rows: ",temp.Equipment_ID)

        if(st.button('NEXT')):
            college_equipment_id = str(college_equipment_id[0])
            equipment_available = check_college_equipment_availability(college_equipment_id, issue_datetime,
                                                                       return_datetime)
            if(not equipment_available):
                st.success("Sorry Equipment not available in the given time slot")
            else:

                cursor.execute("SElECT user_id FROM user_db WHERE username = %s;", (username,))
                temp = cursor.fetchall()
                user_id = temp[0][0]

                issue_query = "INSERT INTO issueequip_db VALUES (%s, %s, %s, %s);"
                query_data = (user_id, college_equipment_id, issue_datetime, return_datetime)
                cursor.execute(issue_query, query_data)
                db.commit()
                st.success("EQUIPMENT ISSUED SUCCESFULLY")

    def check_user_equipment_availability(user_equipment_id, issue_datetime, return_datetime):
        query_input = (
        user_equipment_id, issue_datetime, issue_datetime, return_datetime, return_datetime, issue_datetime,
        return_datetime)
        cursor.execute(
            "SELECT COUNT(*) FROM (SELECT * FROM borrow_db WHERE Equipment_ID = %s AND ( (%s >= Issue_Date_Time AND %s <= Return_Date_Time) OR (%s >= Issue_Date_Time AND %s <= Return_Date_Time) OR (%s <= Issue_Date_Time AND %s >= Return_Date_Time))) as A;",
            query_input)
        l = cursor.fetchall()
        cnt = l[0][0]
        if (cnt == 0):
            return True
        else:
            return False

    if(query == 'Borrow From Peers'):
        issue_datetime = st.text_input("Issue Datetime - format(YYYY-MM-DD 'space' HH:MM:SS)", max_chars=255)
        return_datetime = st.text_input("Datetime Datetime - format(YYYY-MM-DD 'space' HH:MM:SS)", max_chars=255)
        pickup_address = st.text_input('Pickup Address',max_chars=255)

        cursor.execute("SELECT Equipment_ID,Name FROM userequip_db")
        temp = cursor.fetchall()
        temp = pd.DataFrame(temp, columns=['Equipment_ID', 'Name'])
        st.dataframe(temp)
        user_equipment_id = st.multiselect("Select rows: ", temp.Equipment_ID)


        if(st.button('NEXT')):
            user_equipment_id = str(user_equipment_id[0])
            equipment_available = check_user_equipment_availability(user_equipment_id, issue_datetime, return_datetime)
            if(not equipment_available):
                st.success("EQUIPMENT NOT available in the entered time slot")
            else:
                cursor.execute("SElECT user_id FROM user_db WHERE username = %s;", (username,))
                temp = cursor.fetchall()
                user_id = temp[0][0]

                borrow_query = "INSERT INTO borrow_db VALUES (%s, %s, %s, %s, %s);"
                query_data = (user_id, user_equipment_id, issue_datetime, return_datetime, pickup_address)
                cursor.execute(borrow_query, query_data)
                db.commit()
                st.success("EQUIPMENT BORROWED SUCCESFULLY")

    if(query == 'Hire Coach'):
        start_date = st.text_input("Start Date - format(YYYY-MM-DD)",max_chars=255)

        cursor.execute('SELECT Coach_ID,First_name,Last_name,Gender From coach_db')
        temp = cursor.fetchall()
        temp = pd.DataFrame(temp,columns=['Coach_ID','First_name','Last_name','Gender'])
        st.dataframe(temp)

        coach_id = st.multiselect('Select Row - ',temp.Coach_ID)

        if(st.button("NEXT")):
            coach_id = str(coach_id[0])

            cursor.execute("SElECT user_id FROM user_db WHERE username = %s;", (username,))
            temp = cursor.fetchall()
            user_id = temp[0][0]

            hire_query = "INSERT INTO trains_db VALUES (%s, %s, %s);"
            query_data = (coach_id, user_id,start_date)
            cursor.execute(hire_query, query_data)
            db.commit()
            st.success("COACH HIRED SUCCESSFULLY")

def main():
	st.markdown(title_temp.format("Sportify"),unsafe_allow_html=True)

	menu = ["Home","Login","SignUp"]
	types = ["User", "Administration", "Referee", "Coach", "Vendor"]
	tables = {"User": "user_db", "Vendor": "vendor_db"}
	choice = st.sidebar.selectbox("Menu",menu)

	if choice == "Home":
		st.subheader("Home")

	elif choice == "Login":
		st.subheader("Home")

		username = st.sidebar.text_input("User Name")
		password = st.sidebar.text_input("Password",type='password')
		user_type = st.sidebar.selectbox("Login as", types)
		if st.sidebar.checkbox("Login"):
			create_usertable()
			hashed_pswd = make_hashes(password)

			result = login_user(username,check_hashes(password,hashed_pswd), user_type)
			if result:
				st.success("Logged In as {}".format(username))

				if user_type == "User":
					st.info("Not made yet")
				elif user_type == "Administration":
					st.info("Not made yet")
				elif user_type == "Referee":
					st.info("Not made yet")
				elif user_type == "Coach":
					# st.info("Not made yet")
					Coach_Queries(username)
				elif user_type == "Vendor":
					VenderQueries(username)

			else:
				st.warning("Incorrect Username/Password")

	elif choice == "SignUp":
		st.subheader("Create New Account")
		new_user = st.text_input("Username", max_chars = 50)
		new_password = st.text_input("Password",type='password', max_chars = 50)
		new_type = st.selectbox("User Type", types)

		if st.button("Signup"):
			create_usertable()
			add_userdata(new_user,make_hashes(new_password), new_type)
			st.success("You have successfully created a valid Account")
			st.info("Go to Login Menu to login")


title_temp = """
<link href="//maxcdn.bootstrapcdn.com/bootstrap/4.0.0/css/bootstrap.min.css" rel="stylesheet" id="bootstrap-css">
<script src="//maxcdn.bootstrapcdn.com/bootstrap/4.0.0/js/bootstrap.min.js"></script>
<script src="//cdnjs.cloudflare.com/ajax/libs/jquery/3.2.1/jquery.min.js"></script>

<div class="border-top my-3"></div>
<div class="row featurette">
	<div class="col-md-7 order-md-2">
		<h2 class="featurette-heading">Sport<span class="text-muted">Ify.</span></h2>
		<p class="lead">Let's Play</p>
	</div>
	<div class="col-md-5 order-md-1">
		<img src="https://drive.google.com/thumbnail?id=1G935akOWbGejQFjNX-wiqpszuCLfhz_q" class="img-fluid logo" alt="logo">
	</div>
</div>
<div class="border-top my-3"></div>
"""

if __name__ == '__main__':
	main()
