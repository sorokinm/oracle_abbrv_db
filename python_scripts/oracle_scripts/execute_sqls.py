import cx_Oracle
import os
import re
os.environ["NLS_LANG"] = ".AL32UTF8"


def get_data_from_file(file_name):
    sql_query_file = open(file_name, encoding="utf-8")
    return ''.join(sql_query_file.readlines())


def execute_queries(query_with_semicolon, cursor):
    query_list = [query.strip(";") for query in query_with_semicolon.split(";\n")]
    for query in query_list:
        query = query.strip()
        if len(query) != 0:
            try:
                cursor.execute(query)
            except Exception as inst:
                print("Error:")
                print(type(inst))  # the exception instance
                print(query)



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


def army_fill_db(connection):
    fill_db_with_default_tag("../../csvs/army.csv", 'Армия', connection)


def informatics_fill_db(connection):
    fill_db_with_default_tag("../../csvs/informatics.csv", 'Информатика', connection)


def science_miscel_fill_db(conn):
    fill_db_with_default_tag("../../csvs/science_miscellaneous.csv", "Наука.Разное", conn)


def fill_db_with_default_tag(file_path, default_tag, connection):
    cursor = connection.cursor()
    raw_data = get_data_from_file(file_path)
    data_to_save = [csv_line.strip().split(",") for csv_line in raw_data.split(",\n")]
    for csv_line_data in data_to_save:
        if len(csv_line_data) == 2:
            save_to_db_with_tag(csv_line_data, default_tag, cursor)
        elif len(csv_line_data) >= 3:
            save_to_db_csv_line(csv_line_data, cursor)
        else:
            print("Can't save line " + str(csv_line_data))


def chemi_fill_db(connection):
    fill_db_with_default_tag("../../csvs/chemotherapy.csv", 'None', connection)


def math_fill_db(connection):
    fill_db_with_default_tag("../../csvs/math.csv", 'None', connection)


def historical_places_fill_db(connection):
    fill_db_with_default_tag("../../csvs/historical_places.csv", 'None', connection)


def save_to_db_csv_line(csv_line_data, cursor):
    if len(csv_line_data) < 3:
        print("Too short csv line!!!")
        return
    abbrv = csv_line_data[0]
    tag = csv_line_data[len(csv_line_data) - 1]
    meaning = (','.join(csv_line_data[1:-1]))
    sql_to_execute = get_row_insert_sql(abbrv, meaning, tag)
    execute_queries(sql_to_execute, cursor)


def save_to_db_with_tag(csv_line_data, tag, cursor):
    if len(csv_line_data) < 2:
        print("Can't save line" + str(csv_line_data))
        return
    abbrv = csv_line_data[0]
    meaning = csv_line_data[1]
    sql_to_execute = get_row_insert_sql(abbrv, meaning, tag)
    execute_queries(sql_to_execute, cursor)


def sorkr_fill_db(conn):
    fill_db_with_default_tag("../../csvs/full_sorkr.csv", 'None', conn)

#create_db_user('sma', 'sma')
#execute_queries(sql_to_execute, cursor)

connection = get_oracle_connection('sma', 'sma')
#create_tables(connection)
#chemi_fill_db(connection)
#historical_places_fill_db(connection)

#informatics_fill_db(connection)
#math_fill_db(connection)

#science_miscel_fill_db(connection)

sorkr_fill_db(connection)

#execute_queries(sql, cursor)

#create_db_user("sma", "sma")

