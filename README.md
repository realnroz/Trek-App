# Trek-App
Flask app for elective

1.Create database & configure database settings in main.py

   Table name : users

   Columns:
   
      -id               int,not null,auto_increment
      -first_name       varchar(200)
      -last_name        varchar(200)
      -address          varchar(200)
      -phone_number     varchar(200)
      -email            varchar(200)
      -password         varchar(200)
      
   Table name : trek_destinations

   Columns:
   
      -id               int,not null,auto_increment
      -title            varchar(200)
      -days             int
      -difficulty       varchar(200)
      -total_cost       int
      -upvotes          int
      -user_id          int
      
   Table name : iternaries
   
   Columns:
   
      -id                     int,not null,auto_increment
      -title                  varchar(200)
      -day                    int
      -start_place            varchar(200)
      -endplace               varchar(200)
      -description            text
      -duration               varchar(200)
      -cost                   int
      -trek_destination_id    int

2.Create Virtual Environment

3.Install required packages
      
      pip install -r requirements.txt
      
4.Run main.py
