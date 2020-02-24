from PIL import Image
import os
from barcode.writer import ImageWriter, ImageFont, ImageDraw
from Barcodes import Barcode as bc
import DataBase as DB
import re, json
from vkMessage import vkMessage
import vkapi
import requests

class Ticket:


    def __init__(self, path = (os.getcwd() + '\\ticket.jpg')):
        try:
            self.ticketImage = Image.open(path).convert("RGBA")
        except Exception as e:
            print(e)
        self.width, self.height = self.ticketImage.size

    def pasteBarcode(self, number, x, y):
        barcode = bc(str(number)).barcodeImage
        self.ticketImage.paste(barcode, (x,y), barcode)


    def pasteText(self, number, x, y, font_family = "Museo Cyrl 900", font_size = 80, color = (29,28,31)):
        try:
            font = ImageFont.truetype(os.getcwd()+"\Fonts\\%s.otf" % (font_family), font_size)
        except:
            font = ImageFont.truetype(os.getcwd()+"/VKBot/Fonts/%s.otf" % (font_family), font_size)
        draw = ImageDraw.Draw(self.ticketImage)
        if str(x) == "center":
            w, h = draw.textsize(number, font = font)
            x = (self.width-w) / 2
        draw.text((x,y), number, color, font= font)

    def saveTicket(self, name = ''):
        try:
            self.ticketImage.save(os.getcwd() + r'/Tickets/Ticket' + name + '.png')
        except:
            self.ticketImage.save(os.getcwd() + r'/VKBot/Tickets/Ticket' + name + '.png')

    def __exit__(self):
        self.ticketImage.close()


def ais_ticket_generate(code, name, Tk):
    Tk.pasteBarcode(code, 50, Tk.height - 190)
    Tk.pasteText(name, "center", Tk.height/2 - 100, font_family = "Gilroy-Light", font_size = 50)
    Tk.pasteText(code[3:], Tk.width/2 + 165, Tk.height - 190, font_family = "Gilroy-Bold", font_size = 80)
    Tk.saveTicket(code)


def get_ticket_attachment(id, name, code):

    try:
        print('y')
        ticket = Ticket((os.getcwd() + '\\ticket.jpg'))
    except:
        print('n')
        ticket = Ticket((os.getcwd() + '/VKBot/ticket.jpg'))
    ais_ticket_generate(code, name, ticket)
    url = vkapi.get_doc_upload_server(id)
    try:
        with open(os.getcwd() + r'/Tickets/Ticket' + str(code) + '.png', 'rb') as f:
            r = requests.post(url['upload_url'], files = {'file': f})
    except:
        with open(os.getcwd() + r'/VKBot/Tickets/Ticket' + str(code) + '.png', 'rb') as f:
            r = requests.post(url['upload_url'], files = {'file': f})
    req = json.loads(r.text)
    answer = vkapi.doc_save(req['server'], req['photo'], req['hash'])
    return 'photo' + str(answer[0]['owner_id']) + '_' + str(answer[0]['id'])
