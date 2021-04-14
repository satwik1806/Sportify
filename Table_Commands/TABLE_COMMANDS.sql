CREATE TABLE user_db(
   User_ID         INTEGER  NOT NULL PRIMARY KEY auto_increment
  ,First_name      VARCHAR(11) NOT NULL
  ,Last_name       VARCHAR(16) NOT NULL
  ,Email           VARCHAR(34) NOT NULL unique
  ,Phone_Number    VARCHAR(12) NOT NULL unique
  ,Date_of_Birth   DATE  NOT NULL
  ,Gender          VARCHAR(6) NOT NULL
  ,check (Gender in ('Male', 'Female', 'Others'))
  ,Date_of_Joining DATE  NOT NULL
  ,check (Date_of_Joining>Date_of_Birth)
  ,Address         VARCHAR(27) NOT NULL
);

CREATE TABLE vendor_db(
   Vendor_ID                INTEGER  NOT NULL PRIMARY KEY auto_increment
  ,Shop_name                VARCHAR(10) NOT NULL
  ,Email                    VARCHAR(29) NOT NULL unique
  ,Phone_number             VARCHAR(12) NOT NULL unique
  ,no_of_equipment_repaired INTEGER  NOT NULL
  ,Address_Location         VARCHAR(25) NOT NULL
);

CREATE TABLE sports_db(
   Sport_ID    INTEGER  NOT NULL PRIMARY KEY auto_increment
  ,Name        VARCHAR(12) NOT NULL
  ,Max_Players INTEGER  NOT NULL
);


CREATE TABLE friend_db(
   User_ID        INTEGER  NOT NULL 
  ,Friend_ID      INTEGER  NOT NULL
  ,check (User_ID != Friend_ID)
  ,Date_of_Adding DATETIME default current_timestamp
  ,PRIMARY KEY(User_ID, Friend_ID)
  ,foreign key (User_ID) references user_db(User_ID)
  ,foreign key (Friend_ID) references user_db(User_ID)
);

CREATE TABLE venue_db(
   Venue_ID     INTEGER  NOT NULL PRIMARY KEY 
  ,Venue_Name   VARCHAR(18) NOT NULL
  ,Venue_Type   VARCHAR(7) NOT NULL
  ,check (Venue_Type in ('Outdoor', 'Indoor'))
  ,Opening_Time time NOT NULL
  ,Closing_Time time NOT NULL
  ,check (Closing_Time>Opening_Time)
  ,Location     VARCHAR(27) NOT NULL
  ,Sport_ID     INTEGER  NOT NULL
  ,foreign key (Sport_ID) references sports_db(Sport_ID)
);

CREATE TABLE venuebooking_db(
   Venue_ID       INTEGER  NOT NULL
  ,Start_DateTime datetime NOT NULL
  ,End_DateTime   datetime NOT NULL
  ,primary key (Venue_ID, Start_DateTime)
  ,check (End_DateTime>Start_DateTime)
  ,foreign key (Venue_ID) references venue_db(Venue_ID)
);

CREATE TABLE referee_db(
   Referee_ID              INTEGER  NOT NULL PRIMARY KEY 
  ,First_name              VARCHAR(11) NOT NULL
  ,Last_name               VARCHAR(13) NOT NULL
  ,Gender                  VARCHAR(6) NOT NULL
  ,check (Gender in ('Male', 'Female', 'Others'))
  ,Email                   VARCHAR(31) NOT NULL unique
  ,Phone_number            VARCHAR(12) NOT NULL unique
  ,Date_of_Birth           DATE  NOT NULL
  ,Availability_Status     varchar(20)  NOT NULL
  ,check(Availability_Status in ('Available', 'Not Available'))
  ,Games_refereed          INTEGER  NOT NULL
  ,Specialization_Sport_ID INTEGER  NOT NULL
  ,foreign key (Specialization_Sport_ID) references sports_db(Sport_ID)
);

CREATE TABLE coach_db(
   Coach_ID                INTEGER  NOT NULL PRIMARY KEY auto_increment
  ,First_name              VARCHAR(9) NOT NULL
  ,Last_name               VARCHAR(13) NOT NULL
  ,Gender                  VARCHAR(6) NOT NULL
  ,check (Gender in ('Male', 'Female', 'Others'))
  ,Email                   VARCHAR(27) NOT NULL unique
  ,Phone_number            VARCHAR(12) NOT NULL unique
  ,Date_of_Birth           DATE  NOT NULL
  ,Availability_Status     varchar(20)  NOT NULL
  ,check(Availability_Status in ('Available', 'Not Available'))
  ,Specialization_Sport_ID INTEGER  NOT NULL
  ,foreign key (Specialization_Sport_ID) references sports_db(Sport_ID)
);

CREATE TABLE trains_db(
   Coach_ID   INTEGER  NOT NULL 
  ,User_ID    INTEGER  NOT NULL
  ,Start_Date DATE  NOT NULL
  ,primary key(Coach_ID, User_ID)
  ,foreign key (Coach_ID) references coach_db(Coach_ID)
  ,foreign key (User_ID) references user_db(User_ID)
);

CREATE TABLE favorite_db(
   User_ID  INTEGER  NOT NULL 
  ,Sport_ID INTEGER  NOT NULL
  ,primary key(User_ID, Sport_ID)
  ,foreign key (User_ID) references user_db(User_ID)
  ,foreign key (Sport_ID) references sports_db(Sport_ID)
);

CREATE TABLE events_db(
   Event_ID          INTEGER  NOT NULL PRIMARY KEY auto_increment
  ,Event_Name        VARCHAR(21) NOT NULL
  ,Start_DateTime        DATETIME NOT NULL
  ,End_DateTime          DATETIME NOT NULL
  ,Duration          TIME as ( timediff(End_DateTime,Start_DateTime) )
  ,Participant_Limit INTEGER  NOT NULL
  ,Organizer_ID      INTEGER  NOT NULL
  ,DateTime_of_Booking DATETIME default current_timestamp
  ,Venue_ID          INTEGER  NOT NULL
  ,Sport_ID          INTEGER  NOT NULL
  ,foreign key (Organizer_ID) references user_db(User_ID)
  ,foreign key (Venue_ID) references venue_db(Venue_ID)
  ,foreign key (Sport_ID) references sports_db(Sport_ID)
);

CREATE TABLE judges_db(
   Event_ID   INTEGER  NOT NULL 
  ,Referee_ID INTEGER  NOT NULL
  ,primary key(Event_ID, Referee_ID)
  ,foreign key (Event_ID) references events_db(Event_ID)
  ,foreign key (Referee_ID) references referee_db(Referee_ID)
);

CREATE TABLE participation_db(
   User_ID  INTEGER  NOT NULL 
  ,Event_ID INTEGER  NOT NULL
  ,primary key(User_ID, Event_ID)
  ,foreign key (User_ID) references user_db(User_ID)
  ,foreign key (Event_ID) references events_db(Event_ID)
);


CREATE TABLE administrator_db(
   Admin_ID          INTEGER  NOT NULL PRIMARY KEY auto_increment
  ,First_name        VARCHAR(11) NOT NULL
  ,Last_name         VARCHAR(10) NOT NULL
  ,Email             VARCHAR(28) NOT NULL unique
  ,Phone_number      VARCHAR(12) NOT NULL unique
  ,Office_Location   VARCHAR(23) NOT NULL
  ,Managing_Sport_ID INTEGER  NOT NULL
  ,foreign key (Managing_Sport_ID) references sports_db(Sport_ID)
);

CREATE TABLE userequip_db(
   Equipment_ID  INTEGER  NOT NULL PRIMARY KEY auto_increment 
  ,Name          VARCHAR(22) NOT NULL
  ,Repair_Status BIT  NOT NULL
  ,Equip_Condition VARCHAR(7) NOT NULL
  ,check (Equip_Condition in ('Poor', 'Average', 'Good'))
  ,Sport_ID      INTEGER  NOT NULL
  ,User_ID  INTEGER  NOT NULL
  ,foreign key (Sport_ID) references sports_db(Sport_ID)
  ,foreign key (User_ID) references user_db(User_ID)
);

CREATE TABLE collegeequip_db(
   Equipment_ID        INTEGER  NOT NULL PRIMARY KEY auto_increment
  ,Name                VARCHAR(19) NOT NULL
  ,Repair_Status BIT  NOT NULL
  ,Equip_Condition VARCHAR(7) NOT NULL
  ,check (Equip_Condition in ('Poor', 'Average', 'Good'))
  ,Manufacturer        VARCHAR(10) NOT NULL
  ,Sport_ID      INTEGER  NOT NULL
  ,Owner_Admin_ID      INTEGER  NOT NULL
  ,foreign key (Sport_ID) references sports_db(Sport_ID)
  ,foreign key (Owner_Admin_ID) references administrator_db(Admin_ID)
);

CREATE TABLE borrow_db(
   Borrower_ID               INTEGER  NOT NULL
  ,Equipment_ID              INTEGER  NOT NULL
  ,Issue_Date_Time           DATETIME NOT NULL
  ,Return_Date_Time DATETIME NOT NULL
  ,check(Return_Date_Time > Issue_Date_Time)
  ,Pickup_Address            VARCHAR(26) NOT NULL
  ,PRIMARY KEY(Borrower_ID, Equipment_ID, Issue_Date_Time)
  ,foreign key (Borrower_ID) references user_db(User_ID)
  ,foreign key (Equipment_ID) references userequip_db(Equipment_ID)
);

CREATE TABLE issueequip_db(
   Borrower_ID               INTEGER  NOT NULL
  ,Equipment_ID              INTEGER  NOT NULL
  ,Issue_Date_Time           DATETIME NOT NULL
  ,Return_Date_Time      DATETIME NOT NULL
  ,check(Return_Date_Time > Issue_Date_Time)
  ,PRIMARY KEY(Borrower_ID, Equipment_ID, Issue_Date_Time)
  ,foreign key (Borrower_ID) references user_db(User_ID)
  ,foreign key (Equipment_ID) references collegeequip_db(Equipment_ID)
);
  

CREATE TABLE collegeorders_db(
     Order_ID INTEGER NOT NULL primary key auto_increment
    ,Type varchar(6) NOT NULL
    ,check (Type in ('Buy', 'Repair'))
    ,Order_Status varchar(10)
    ,check (Order_Status in ('Pending', 'Complete'))
    ,Equipment_ID INTEGER NOT NULL
    ,Vendor_ID INTEGER NOT NULL
    ,foreign key (Equipment_ID) references collegeequip_db(Equipment_ID)
    ,foreign key (Vendor_ID) references vendor_db(Vendor_ID)
);


CREATE TABLE userorders_db(
     Order_ID INTEGER NOT NULL primary key auto_increment
    ,Type varchar(6) NOT NULL
    ,check (Type in ('Buy', 'Repair'))
    ,Order_Status varchar(10)
    ,check (Order_Status in ('Pending', 'Complete'))
    ,User_ID INTEGER NOT NULL
    ,Equipment_ID INTEGER NOT NULL
    ,Vendor_ID INTEGER NOT NULL
    ,foreign key (User_ID) references user_db(User_ID)
    ,foreign key (Equipment_ID) references userequip_db(Equipment_ID)
    ,foreign key (Vendor_ID) references vendor_db(Vendor_ID)
);


CREATE TABLE coachfeedback_db(
     User_ID    INTEGER NOT NULL
    ,Coach_ID   INTEGER NOT NULL
    ,Feedback_Text  varchar(150)
    ,PRIMARY KEY (User_ID, Coach_ID)
    ,foreign key (User_ID) references user_db(User_ID)
    ,foreign key (Coach_ID) references coach_db(Coach_ID)
);


-- username adding to tables, creating table for usernames : 

CREATE TABLE IF NOT EXISTS accounts_db (
  Username varchar(50) Primary Key,
  Account_Password TEXT, 
  User_Type TEXT,
    check (User_Type in ('User', 'College Administrator', 'Vendor', 'Referee', 'Coach')) 
);


ALTER TABLE user_db
ADD username varchar(50) NOT NULL;

ALTER TABLE vendor_db
ADD username varchar(50) NOT NULL;

ALTER TABLE referee_db
ADD username varchar(50) NOT NULL;

ALTER TABLE coach_db
ADD username varchar(50) NOT NULL;

ALTER TABLE administrator_db
ADD username varchar(50) NOT NULL;


ALTER TABLE vendor_db
ADD FOREIGN KEY (username) REFERENCES accounts_db(Username);

ALTER TABLE user_db
ADD FOREIGN KEY (username) REFERENCES accounts_db(Username);

ALTER TABLE referee_db
ADD FOREIGN KEY (username) REFERENCES accounts_db(Username);

ALTER TABLE coach_db
ADD FOREIGN KEY (username) REFERENCES accounts_db(Username);

ALTER TABLE administrator_db
ADD FOREIGN KEY (username) REFERENCES accounts_db(Username);

-- ADDING CHECKS IN EVENTS_DB :
alter table events_db
add CHECK (Start_DateTime < End_DateTime);
alter table events_db
add CHECK (DateTime_of_Booking < Start_DateTime);


-- BIT VALUE , data too long some data type compatibility issue,,  changing it to INT NOT NULL

alter table userequip_db
modify Repair_Status INT NOT NULL;
alter table collegeequip_db
modify Repair_Status INT NOT NULL;
