import cx_Oracle
import os
os.environ["NLS_LANG"] = ".AL32UTF8"


def get_data_from_file(file_name):
    sql_query_file = open(file_name, encoding="utf-8")
    return ''.join(sql_query_file.readlines())


def execute_queries(query_with_semicolon, cursor):
    query_list = [query.strip(";") for query in query_with_semicolon.split(";\n")]
    for query in query_list:
        query = query.strip()
        if len(query) != 0:
            cursor.execute(query)


def create_db_user(name, pas):
    conn = get_oracle_connection('system', 'oracle')
    sql = get_data_from_file('sql_scripts/create_user.sql').strip()
    sql = sql.replace(":user_name", name)
    sql = sql.replace(":password", pas)
    execute_queries(sql, conn.cursor())


def get_oracle_connection(usrname='system', passw='oracle'):
    try:
        return cx_Oracle.connect(usrname, passw, "192.168.1.149:1521/orcl" )
    except cx_Oracle.DatabaseError as exc:
        err, = exc.args
        print("Oracle-Error-Code:", err.code)
        print("Oracle-Error-Message:", err.message)


def create_tables(conn):
    sql = get_data_from_file('sql_scripts/create_tables.sql')
    cursor = conn.cursor()
    execute_queries(sql, cursor)

def get_row_insert_sql(abbrv_name, abbrv_meaning, abbrv_tag):
    sql = get_data_from_file('sql_scripts/insert_abbrv_row.sql')
    sql = sql.replace(":abbrv_name", "'{}'".format(abbrv_name))
    sql = sql.replace(":tag_name", "'{}'".format(abbrv_tag))
    sql = sql.replace(":abbrv_meaning", "'{}'".format(abbrv_meaning))
    return sql


def army_fill_db():
    connection = get_oracle_connection('sma', 'sma')
    cursor = connection.cursor()
    army_csv = get_data_from_file("../../csvs/army.csv")
    data_to_save = [csv_line.strip().split(",") for csv_line in army_csv.split(",\n")]
    for csv_line_data in data_to_save:
        if len(csv_line_data) == 2:
            sql_to_execute = get_row_insert_sql(csv_line_data[0], csv_line_data[1], 'Армия')
            execute_queries(sql_to_execute, cursor)


connection = get_oracle_connection('sma', 'sma')
cursor = connection.cursor()


#sql_to_execute = get_row_insert_sql('WTF', 'What the fuck', 'slang')
#execute_queries(sql_to_execute, cursor)

connection = get_oracle_connection('sma', 'sma')
cursor = connection.cursor()
chem_csv = get_data_from_file("../../csvs/chemotherapy.csv")
data_to_save = [csv_line.strip().split(",") for csv_line in chem_csv.split(",\n")]
for csv_line_data in data_to_save:
    if len(csv_line_data) >= 3:
        abbrv = csv_line_data[0]
        tag = csv_line_data[len(csv_line_data) - 1]
        meaning = (','.join(csv_line_data[1:-1]))[0:130]
        sql_to_execute = get_row_insert_sql(abbrv, meaning, tag)
        execute_queries(sql_to_execute, cursor)


#execute_queries(sql, cursor)

#create_db_user("sma", "sma")

