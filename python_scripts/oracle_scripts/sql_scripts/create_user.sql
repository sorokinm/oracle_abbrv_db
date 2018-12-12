create user :user_name identified by :password;

grant connect to :user_name;
--grant create session grant any privilege to :user_name;

--grant unlimited tablespace to :user_name;



