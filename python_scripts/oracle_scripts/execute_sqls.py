import cx_Oracle


def get_sql_query_from_file(file_name):
    sql_query_file = open(file_name, encoding="utf-8")
    return ''.join(sql_query_file.readlines())


def get_oracle_connection(username='SMA', password='SMA'):
    try:
        return cx_Oracle.connect(username, password, "oracle@192.168.1.149/orcl")
    except cx_Oracle.DatabaseError as exc:
        err, = exc.args
        print("Oracle-Error-Code:", err.code)
        print("Oracle-Error-Message:", err.message)


connection = get_oracle_connection('SYSTEM', 'oracle')
#sql = get_sql_query_from_file('sql_scripts/create_tables.sql')
#cursor = connection.cursor()
#cursor.execute(sql)