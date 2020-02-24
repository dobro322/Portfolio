#coding: utf-8

import re
import codecs
from vkMessage import vkMessage
import os
from keyboard import KeyBoard

def getTxt(file):
    try:
        contents = codecs.open(os.getcwd() + "\Data\\"+file,encoding='utf-8')
    except:
        contents = codecs.open(os.getcwd() + "/VKBot/Data/"+file,encoding='utf-8')
    return contents

def getLinesFromFile(command, data):
    list = []
    for line in data:
        if re.match(command, line):
            list.append(line)
        else:
            break
    return list

def getCommands(data):
    list = getLinesFromFile(r'!.+', data)
    return [x[1:] for x in list]

def getAttachments(data):
    list = re.findall (r'\w+?-?\d+_\d+|doc-?\d+_\d+', data)
    print(list)
    if list:
        return re.sub(r'документы\n(.+\n)+','',data), ','.join(list)
    else:
        return data, ''

def help(file, body = 'Какие команды есть в этом разделе:\n', payload = ''):
    KB = KeyBoard()
    text = getTxt(file)
    contents = getCommands(text)
    for line in contents:
        label = re.match(r'.+', line).group(0)
        body += '\n - ' + label
        KB.addButton(label,'white','{\\"text\\":\\"' + payload + '\\"}')
    return body, KB.getWithMenuButton()

def callCommand(command, text):
    isCommandShowed = False
    finalText = ''
    for line in text:
        if isCommandShowed:
            if not re.match('@|\n' + command, line):
                finalText += line

        if re.match('@' + command, line):
            isCommandShowed = True

        if line in '\n' and isCommandShowed:
            isCommandShowed = False
    return finalText


def prepeareTheAnswer(command, file, message = vkMessage('')):
    txt = getTxt(file)
    message.message = callCommand(command, txt)
    try:
        txt.close()
    except:
        pass
    message.message, message.attachment = getAttachments(message.message)
    print(message.attachment)
    return message
