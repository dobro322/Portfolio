import zipfile
import DataBase as DB
import os
from vkMessage import vkMessage
import vkapi
import requests
from flask import Flask, request, json

def get_report(id):
    return DB.get_last_report(id)

def get_user(id):
    return DB.get_person(id)

def get_request(url):
    try:
        with open(os.getcwd() + '\Docs\\Zhaloba.docx', 'rb') as f:
            return requests.post(url['upload_url'], files={'file': f})
    except:
        with open(os.getcwd() + '/VKBot/Docs/Zhaloba.docx', 'rb') as f:
            return requests.post(url['upload_url'], files={'file': f})

def get_answer(req, User):
    return vkapi.save(req, 'Жалоба от ' + get_fio_initials(User['FIO']) + '.docx')


def set_message(answer, User, Report, peer_id):
    message = vkMessage('')
    message.attachment = 'doc' + str(answer[0]['owner_id']) + '_' + str(answer[0]['id'])
    message.message =  'Жалоба от @id' + str(User['VK']) + '(' + User['FIO'] + ')\nНа тему ' + Report['Header']
    message.user_id = message.peer_id = int(peer_id)
    return message



def send_sluzhebka(peer_id, id):
    Report = dict(zip(DB.Reports_table, get_report(id)))
    User = dict(zip(DB.Persons_table, get_user(id)))
    url = vkapi.get_messages_upload_server(peer_id)
    request = get_request(url)
    req = request.text.split('":"')[1][0:-2]
    answer = get_answer(req, User)
    message = set_message(answer, User, Report, peer_id)
    return message.send()


def docx_open(old_file, new_file):
    zin = zipfile.ZipFile (old_file, 'r')
    zout = zipfile.ZipFile (new_file, 'w')
    return zin, zout


def docx_replace(rep, old_file = 'file.docx',new_file = 'new_file.docx'):
    zin, zout = docx_open(old_file, new_file)
    for item in zin.infolist():
        buffer = zin.read(item.filename)
        if (item.filename == 'word/document.xml'):
            res = buffer.decode("utf-8")
            for r in rep:
                res = res.replace(r,rep[r])
            buffer = res.encode("utf-8")
        if (item.filename == 'word/footer1.xml'):
            res = buffer.decode("utf-8")
            for r in rep:
                res = res.replace(r,rep[r])
            buffer = res.encode("utf-8")
        zout.writestr(item, buffer)
    zout.close()
    zin.close()

def get_faculty(faculty):
    query = """
    SELECT Faculty_short_name
    FROM Faculties
    WHERE Faculty_id = %s
    """
    args = (faculty,)
    faculty = DB.get_data(query, args)[0]
    return faculty

def get_group(group):
    return group

def get_address(address):
    address = DB.hostel_address(address)
    if address:
        return address
    else:
        return ''

def get_fio_initials(FIO):
    FIO = FIO.split(' ')
    Name = FIO[0] + ' ' + FIO[1][:1] + '.'
    try:
        Name += FIO[2][:1] + '.'
    except:
        print('Net otchestva')
    return Name

def get_report_header(header):
    return header

def get_full_fio(fio):
    return fio

def get_report_body(body):
    return body

def get_report_Orders(orders):
    return orders

def get_report_date(date):
    date = str(date)
    date = date.split('-')
    date = date[::-1]
    date = '.'.join(date)
    return str(date)

def get_phone(phone):
    return phone

def get_chairman_id(faculty_id):
    query = """
    SELECT Faculty_chairman_id
    FROM Faculties
    WHERE Faculty_id = %s
    """
    args = (faculty_id,)
    return DB.get_data(query,args)[0]

def prepare_doc(id):
    Report = dict(zip(DB.Reports_table, get_report(id)))
    User = dict(zip(DB.Persons_table, get_user(id)))
    array = {
        'Faculty': get_faculty(User['Faculty_id']),
        'GroupId': get_group(User['GroupId']),
        'Address': get_address(User['Hostel_id']),
        'INIT': get_fio_initials(User['FIO']),
        'Header': get_report_header(Report['Header']),
        'FIO': get_full_fio(User['FIO']),
        'Body': get_report_body(Report['Body']),
        'Orders': get_report_Orders(Report['Orders']),
        'Date': get_report_date(Report['Date']),
        'Autor': get_fio_initials(User['FIO']),
        'Phone': get_phone(User['Phone'])
    }
    try:
        docx_replace(array, os.getcwd() + '/Docs/Zhalobaa.docx', os.getcwd() + '/Docs/Zhaloba.docx')
    except:
        docx_replace(array, os.getcwd() + '/VKBot/Docs/Zhalobaa.docx', os.getcwd() + '/VKBot/Docs/Zhaloba.docx')

    peer_id = ['21766756','34854271']
    chairman = get_chairman_id(User['Faculty_id'])
    if chairman and not chairman in '-':
        peer_id.append(str(chairman))
    for guy in peer_id:
        send_sluzhebka(guy, id)
