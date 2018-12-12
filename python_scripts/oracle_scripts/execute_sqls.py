import cx_Oracle


def get_sql_query_from_file(file_name):
    sql_query_file = open(file_name, encoding="utf-8")
    return ''.join(sql_query_file.readlines())


def create_db_user(name, pas, conn):
    sql = get_sql_query_from_file('sql_scripts/create_user.sql')
    sql = sql.replace(":user_name", name)
    sql = sql.replace(":password", pas)
    conn.cursor().execute(sql)



def get_oracle_connection(usrname='system', passw='oracle'):
    try:
        return cx_Oracle.connect(usrname, passw, "192.168.1.149:1521/orcl" )
    except cx_Oracle.DatabaseError as exc:
        err, = exc.args
        print("Oracle-Error-Code:", err.code)
        print("Oracle-Error-Message:", err.message)


connection = get_oracle_connection('system', 'oracle')
sql = get_sql_query_from_file('sql_scripts/create_user.sql')
cursor = connection.cursor()
create_db_user("sma", "sma", connection)