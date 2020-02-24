from mysql.connector import MySQLConnection, Error



def get_data(query, args=''):
    conn = MySQLConnection(**dbconfig)
    cursor = conn.cursor(buffered=True)
    cursor.execute(query, args)
    answer = cursor.fetchone()
    conn.close()
    cursor.close()
    return answer


def get_all_data(query, args=''):
    conn = MySQLConnection(**dbconfig)
    cursor = conn.cursor(buffered=True)
    cursor.execute(query, args)
    answer = cursor.fetchall()
    conn.close()
    cursor.close()
    return answer


def insert_data(query, args=''):
    try:
        conn = MySQLConnection(**dbconfig)
        cursor = conn.cursor()
        cursor.execute(query, args)
        conn.commit()
        conn.close()
        cursor.close()
        if cursor.lastrowid:
            return cursor.lastrowid
        else:
            return 0
    except Error as e:
        return 'Can\'t insert Data to DataBase:\n' + str(e)
