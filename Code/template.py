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
sportify = {"database": "sportify_test"
			,"account": "Accounts_DB"
			,"admin": "Administrator_DB"
			,"borrow": "BorrowEquip_DB"
			,"coach": "Coach_DB"
			,"collegeEquip": "CollegeEquip_DB"
			,"collegeOrder": "CollegeOrders_DB"
			,"event": "Events_DB"
			,"favourite": "Favorite_DB"
			,"friend": "Friend_DB"
			,"issue": "IssueEquip_DB"
			,"judge": "Judges_DB"
			,"participate": "Participation_DB"
			,"referee": "Referee_DB"
			,"sports": "Sports_DB"
			,"trains": "Trains_DB"
			,"user": "User_DB"
			,"userEquip": "UserEquip_DB"
			,"userOrder": "UserOrders_DB"
			,"vendor": "Vendor_DB"
			,"venue": "Venue_DB"
			,"booking": "VenueBooking_DB"
			}

# DB Management
db = mysql.connect(
    host = "127.0.0.1",
    user = "root",
    passwd = os.environ.get("DB_PASSWORD"),
    database = sportify["database"],
    auth_plugin="mysql_native_password"
)
cursor = db.cursor()

# DB  Functions
def create_usertable():
	cursor.execute('CREATE TABLE IF NOT EXISTS Accounts_DB(Username TEXT, Password TEXT, User_Type TEXT);')


def add_userdata(username,password,user_type):
	cursor.execute('INSERT INTO Accounts_DB(Username, Password, User_Type) VALUES (%s,%s,%s);',(username,password,user_type))
	db.commit()

def login_user(username,password,user_type):
	cursor.execute("SELECT * FROM Accounts_DB WHERE username= %s AND password= %s AND User_type= %s;",(username,password,user_type))
	data = cursor.fetchall()
	return data

# All Queries

# Vendor
def VenderQueries(username):
	cursor.execute('CREATE TABLE IF NOT EXISTS Vendors_DB(Vendor_ID INT NOT NULL PRIMARY KEY AUTO_INCREMENT, Username TEXT, Shop_name VARCHAR(255) NOT NULL, Email VARCHAR(255) NOT NULL, Phone_number CHAR(15) NOT NULL, Equipments_repaired INT DEFAULT 0, Address VARCHAR(255) NOT NULL);')
	cursor.execute("SELECT * FROM Vendors_DB WHERE username= %s",(username,))
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
				cursor.execute('INSERT INTO Vendors_DB(Username, Shop_name, Email, Phone_number, Address) VALUES (%s,%s,%s,%s,%s)',(username,shop_name,email,phone,address))
				db.commit()
				st.success("You have successfully created a valid Account")
				profile_created = True
			else:
				cursor.execute('UPDATE Vendors_DB SET Shop_name = %s, Email = %s, Phone_number = %s, Address = %s WHERE Username = %s',(shop_name,email,phone,address,username))
				db.commit()
				st.success("You have successfully updated your account")
	
	elif query == "View Profile":
		cursor.execute("SELECT * FROM Vendors_DB WHERE username= %s",(username,))
		profile = cursor.fetchall()
		st.text("Username: {}".format(profile[0][1]))
		st.text("Shop Name: {}".format(profile[0][2]))
		st.text("Email: {}".format(profile[0][3]))
		st.text("Phone: {}".format(profile[0][4]))
		st.text("Address: {}".format(profile[0][6]))

	elif query == "Check College Orders":
		order_type = st.selectbox("Type of Order", ["Buy Order", "Repair Order"])
		if order_type == "Repair Order":
			cursor.execute("SELECT Vendor_ID FROM Vendors_DB WHERE username= %s",(username,))
			vendor_id = cursor.fetchall()[0][0]
			cursor.execute("SELECT * FROM CollegeOrders_DB WHERE Vendor_ID= {} AND Type= 'Repair'".format(vendor_id,))
			buy_order = cursor.fetchall()
			buy_order = pd.DataFrame(buy_order, columns=["Order_ID", "Type", "Order_Status", "Equipment_ID", "Vendor_ID"])
			st.dataframe(buy_order)
			selected_indices = st.multiselect('Select rows:', buy_order.Order_ID)

			if st.button("Update Status"):
				for index in selected_indices:
					cursor.execute('UPDATE CollegeOrders_DB SET Order_Status = "Complete" WHERE Equipment_ID = {}'.format(index))
					db.commit()
					cursor.execute('UPDATE CollegeEquip_DB SET Ongoing_Repair = 0, Cond = "Good" WHERE Equipment_ID = {}'.format(index))
					db.commit()
					st.success("Successfully updated the order status")
		
		elif order_type == "Buy Order":
			cursor.execute("SELECT Vendor_ID FROM Vendors_DB WHERE username= %s",(username,))
			vendor_id = cursor.fetchall()[0][0]
			cursor.execute("SELECT * FROM CollegeOrders_DB WHERE Vendor_ID= {} AND Type= 'Buy'".format(vendor_id,))
			buy_order = cursor.fetchall()
			buy_order = pd.DataFrame(buy_order, columns=["Order_ID", "Type", "Order_Status", "Equipment_ID", "Vendor_ID"])
			st.dataframe(buy_order)
			selected_indices = st.multiselect('Select rows:', buy_order.Order_ID)

			if st.button("Update Status"):
				for index in selected_indices:
					cursor.execute('UPDATE CollegeOrders_DB SET Order_Status = "Complete" WHERE Equipment_ID = {}'.format(index))
					db.commit()
					cursor.execute('UPDATE CollegeEquip_DB SET Ongoing_Repair = 0, Cond = "Good" WHERE Equipment_ID = {}'.format(index))
					db.commit()
					st.success("Successfully updated the order status")


	elif query == "Check User Orders":
		order_type = st.selectbox("Type of Order", ["Buy Order", "Repair Order"])
		if order_type == "Repair Order":
			cursor.execute("SELECT Vendor_ID FROM Vendors_DB WHERE username= %s",(username,))
			vendor_id = cursor.fetchall()[0][0]
			cursor.execute("SELECT * FROM UserOrders_DB WHERE Vendor_ID= {} AND Type= 'Repair'".format(vendor_id,))
			buy_order = cursor.fetchall()
			buy_order = pd.DataFrame(buy_order, columns=["Order_ID", "Type", "Order_Status", "User_ID", "Equipment_ID", "Vendor_ID"])
			st.dataframe(buy_order)
			selected_indices = st.multiselect('Select rows:', buy_order.Equipment_ID)

			if st.button("Update Status"):
				for index in selected_indices:
					cursor.execute('UPDATE UserOrders_DB SET Order_Status = "Complete" WHERE Equipment_ID = {}'.format(index))
					db.commit()
					cursor.execute('UPDATE UserEquip_DB SET Ongoing_Repair = 0, Cond = "Good" WHERE Equipment_ID = {}'.format(index))
					db.commit()
					st.success("Successfully updated the order status")
		
		elif order_type == "Buy Order":
			cursor.execute("SELECT Vendor_ID FROM Vendors_DB WHERE username= %s",(username,))
			vendor_id = cursor.fetchall()[0][0]
			cursor.execute("SELECT * FROM UserOrders_DB WHERE Vendor_ID= {} AND Type= 'Buy'".format(vendor_id,))
			buy_order = cursor.fetchall()
			buy_order = pd.DataFrame(buy_order, columns=["Order_ID", "Type", "Order_Status", "User_ID", "Equipment_ID", "Vendor_ID"])
			st.dataframe(buy_order)
			selected_indices = st.multiselect('Select rows:', buy_order.Equipment_ID)

			if st.button("Update Status"):
				for index in selected_indices:
					cursor.execute('UPDATE UserOrders_DB SET Order_Status = "Complete" WHERE Equipment_ID = {}'.format(index))
					db.commit()
					cursor.execute('UPDATE UserEquip_DB SET Ongoing_Repair = 0, Cond = "Good" WHERE Equipment_ID = {}'.format(index))
					db.commit()
					st.success("Successfully updated the order status")




def main():
	st.markdown(title_temp.format("Sportify"),unsafe_allow_html=True)

	menu = ["Home","Login","SignUp"]
	types = ["User", "Administration", "Referee", "Coach", "Vendor"]
	tables = {"User": "User_DB", "Vendor": "Vendor_DB"}
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
					st.info("Not made yet")
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
