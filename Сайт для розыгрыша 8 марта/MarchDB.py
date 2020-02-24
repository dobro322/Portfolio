#coding: utf-8

from mysql.connector import MySQLConnection, Error

dbconfig = {'host':     '*',
            'database': '*',
            'user':     '*',
            'password': '*'
            }


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
            return None
    except Error as e:
        print('Can\'t insert Data to DataBase:\n' + str(e))
        return None


def insert_all_data(query, args):
    try:
        conn = MySQLConnection(**dbconfig)
        cursor = conn.cursor()
        for arg in args:
            cursor.execute(query, arg)
            conn.commit()
        conn.close()
        cursor.close()
        if cursor.lastrowid:
            return cursor.lastrowid
        else:
            return None
    except Error as e:
        print('Can\'t insert Data to DataBase:\n' + str(e))
        return None


def is_exist(id):
    query = """
    SELECT VK
    FROM Particapants
    WHERE VK = %s
    """
    args = (id,)
    return True if get_data(query, args) else None


def add_particapant(id):
    query = """
    INSERT INTO Particapants(VK)
    VALUES(%s)
    """
    args = (id,)
    return insert_data(query, args)


def get_ticket(id):
    query = """
    SELECT ID
    FROM Particapants
    WHERE VK = %s
    """
    args = (id,)
    return get_data(query, args)[0]


def is_used(key):
    query = """
    SELECT Used
    FROM TicketKeys
    WHERE TicketKey = %s
    """
    args = (str(key).upper(),)
    try:
        return True if get_data(query, args)[0] else False
    except:
        return True


def set_used(key):
    query = """
    UPDATE TicketKeys
    SET Used = 1
    WHERE TicketKey = %s
    """
    args = (str(key).upper(),)
    return insert_data(query, args)


def add_key(key):
    query = """
    INSERT INTO TicketKeys(TicketKey)
    VALUES(%s)
    """
    return insert_all_data(query, key)


def wish(number):
    query = """
    SELECT Wish_text
    FROM Wishes
    WHERE Wish_id = %s
    """
    args = (number,)
    return get_data(query, args)[0]


def wish_count():
    query = """
    SELECT Count(0)
    FROM Wishes
    """
    return get_data(query)[0]
