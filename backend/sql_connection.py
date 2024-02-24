import mysql.connector
__cnx = None


def get_sql_connection():
    global __cnx
    if __cnx is None:
        __cnx  = mysql.connector.connect(
        host="127.0.0.1",
        user="root",
        password="password",
        database="groccery-store"
    )
    return __cnx
     




