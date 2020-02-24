import codecs
import os
import configparser
from mysql.connector import MySQLConnection, Error
import re
import datetime

Persons_table = [
'VK',
'FIO',
'Faculty_id',
'GroupId',
'Hostel_id',
'Phone',
'Status',
]

Reports_table = [
'ID',
'Person_id',
'Header',
'Date',
'Body',
'Orders',
'Is_solved'
]

def get_data(query, args = ''):
        conn = MySQLConnection(**dbconfig)
        cursor = conn.cursor(buffered=True)
        cursor.execute(query, args)
        answer = cursor.fetchone()
        conn.close()
        cursor.close()
        return answer

def get_all_data(query, args = ''):
        conn = MySQLConnection(**dbconfig)
        cursor = conn.cursor(buffered=True)
        cursor.execute(query, args)
        answer = cursor.fetchall()
        conn.close()
        cursor.close()
        return answer

def insert_data(query, args = ''):
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

def get_user(vk):
    query = """SELECT VK, Faculty_id, GroupId, FIO, Phone FROM Persons WHERE VK = %s"""
    args = (vk,)
    return get_data(query, args)

def get_umka(vk):
    query = """SELECT FIO, VK, Faculty_id, GroupId, Phone FROM Persons WHERE VK = %s"""
    args = (vk,)
    return get_data(query, args)

def get_msha_user(vk):
    query = """SELECT FIO, Faculty_id, GroupId, Phone FROM Persons WHERE VK = %s"""
    args = (vk,)
    return get_data(query,args)


def get_person(id):
    query = """
    SELECT *
    FROM Persons
    WHERE VK = %s
    """
    args = (id,)
    return get_data(query, args)

def get_faculty(id):
    query = """
    SELECT Faculty_id
    FROM Persons
    WHERE VK = %s
    """
    args = (id,)
    return get_data(query,args)[0]

def get_report(id):
    query = """
    SELECT *
    FROM Reports
    WHERE ID = %s
    """
    args = (id,)
    return get_data(query, args)

def get_last_report(id):
    query = """
    SELECT *
    FROM Reports
    WHERE PersonId = %s
    ORDER BY ID
    DESC LIMIT 1
    """
    args = (id,)
    return get_data(query, args)

def get_current_state(id):
    query = """
    SELECT Status
    FROM Persons
    WHERE VK = %s
    """
    args = (id, )
    return get_data(query, args)[0]

def hostel_address(id):
    query = """
    SELECT Hostel_Address
    FROM Hostels
    WHERE Hostel_Id = %s
    """
    args = (id,)
    return get_data(query, args)[0]


def get_state_help(code):
    query = """
    SELECT Help
    FROM States
    WHERE Code = %s
    """
    args = (code,)
    return get_data(query, args)[0]

def full_state_info(code):
    query = """
    SELECT *
    FROM States
    WHERE Code = %s
    """
    args = (code,)
    return get_data(query, args)

def delete_report(report_id):
    query = """
    DELETE FROM Reports
    WHERE ID = %s
    """
    args = (report_id,)
    return insert_data(query, args)

def delete_person(id):
    query = """
    DELETE FROM Persons
    WHERE VK = %s
    """
    args = (id,)
    return insert_data(query, args)


def set_state(id, code):
    query = """
    UPDATE Persons
    SET Status = %s
    WHERE VK = %s
    """
    args = (code,id)
    return insert_data(query, args)

def get_events():
    query = """
    SELECT *
    FROM Events
    """
    return get_all_data(query)

def get_event_column_value(table, column, id):
    query = """
    SELECT `%s`
    FROM %s
    WHERE `0` = %s
    """
    args = (column, table, id)

    return get_data(query % args)



def set_after_reg(id, After_reg):
    query = """
    UPDATE Persons
    SET After_reg = %s
    WHERE VK = %s
    """
    args = (After_reg, id)
    return insert_data(query, args)

def get_after_reg(id):
    query = """
    SELECT After_reg
    FROM Persons
    WHERE VK = %s
    """
    args = (id,)
    return get_data(query, args)[0]

def new_event_participant(table, id):
    query = """
    INSERT INTO %s(Date, `0`)
    VALUES(CURRENT_TIME(), %s)
    """
    args = (table, id)
    return insert_data(query % args)

def update_event_participant(table, column, arg, id, date = ''):
    query = """
    UPDATE %s
    SET `%s` = '%s'
    WHERE `0` = '%s'
    """
    args = (table, column, arg, id)
    if date:
        query += " AND Date = '%s'"
        args += (date,)
    return insert_data(query % args)

def get_event_submenu(event, key):
    query = """
    SELECT * FROM States
    WHERE Code LIKE %s
    AND Key_word = %s
    """
    args = (event + "%", key)
    return get_data(query, args)

def get_event_help(event):
    query = """
    SELECT Help
    FROM Events
    WHERE ID = %s
    """
    args = (event,)
    return get_data(query, args)[0]

def get_submenu_count(event):
    query = """
    SELECT Count(0)
    FROM States
    WHERE Code Like %s
    """
    args = (event + "%",)
    return get_data(query, args)[0]

def get_last_event_record_date(event, id):
    query = "SELECT Date FROM %s WHERE `0` = %s ORDER BY Date DESC LIMIT 1"
    args = (event, id)
    return get_data(query % args)[0]

def get_event_participant(vk, event):
    query = """SELECT * FROM %s WHERE `0` = %s AND Date = '%s'"""
    date = get_last_event_record_date(event, vk)
    args = (event, vk, date)
    return get_data(query % args)


def get_event(code):
    query = """
    SELECT *
    FROM Events
    WHERE ID = %s
    """
    args = (code,)
    return get_data(query, args)[0]

def remove_participant(table, id):
    query = """
    DELETE FROM %s
    WHERE `0` = '%s'
    AND Date = '%s'
    """
    date = get_last_event_record_date(table, id)
    args = (table, id, date)
    return insert_data(query % args)

def is_registrated(table, column, id):
    query = """
    SELECT `%s`
    FROM %s
    WHERE `0` = %s
    AND `%s` is not null
    """
    args = (column, table, id, column)
    return bool(get_data(query % args))

def rewrite():
    query = """SELECT `0`
    FROM  Events_2_1
    WHERE `8` is not null
    ORDER BY `Date` """
    answer = get_all_data(query)
    return answer


def participant_count(event,column = ''):
    query = """
    SELECT COUNT(0)
    FROM %s
    """
    args = (event,)
    if column:
        query += "WHERE `%s` <> '' "
        args += (column,)
    return get_data(query % args)[0]

def select_firs_course():
    query = """ SELECT VK FROM Persons WHERE `GroupId` LIKE "%-8%" AND `GroupId` NOT LIKE "%М" """
    return get_all_data(query)

def select_all():
    query = """ SELECT VK FROM Persons WHERE Status > 5 or Status like 'Events%'"""
    return [x[0] for x in get_all_data(query)]


def msha():
    query = """ SELECT VK, Status FROM Persons WHERE Status LIKE 'Events_2_1%' """
    return [[x[0],x[1]] for x in get_all_data(query)]

def registered_in_msha():
    query = """SELECT `0` FROM Events_2_1 e WHERE e.8 is not null"""
    return [x[0] for x in get_all_data(query)]


def in_removed_event():
    query = """ SELECT VK FROM `Persons` WHERE Status LIKE "Events_2%" """
    return [x[0] for x in get_all_data(query)]

def ivo_msha():
    query = """ SELECT VK FROM Events_2_1 e LEFT JOIN Persons p ON e.0 = p.VK WHERE p.Faculty_id = 4 and e.8 is not null """
    return [x[0] for x in get_all_data(query)]


def failed_msha():
    query = """ SELECT `0` FROM `Events_2_1` WHERE `8` is null """
    return [x[0] for x in get_all_data(query)]

def get_event_participants(event):
    query = """ SELECT `0` FROM %s"""
    args = (event,)
    return [x[0] for x in get_all_data(query % args)]
