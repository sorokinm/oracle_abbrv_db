import cx_Oracle


connection = cx_Oracle.connect("hr", "oracle", "192.168.1.149/orcl")
cursor = connection.cursor()