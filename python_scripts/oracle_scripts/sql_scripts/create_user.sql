create user :user_name identified by :password;
grant connect to :user_name;
grant create session to :user_name with admin option;
grant unlimited tablespace to :user_name;
grant resource to :user_name;



