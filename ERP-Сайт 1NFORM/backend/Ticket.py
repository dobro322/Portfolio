from PIL import Image
import os
import barcode as BCLibrary
from barcode.writer import ImageWriter, ImageFont, ImageDraw
import requests
import io
import json
# import DataBase as DB


class Ticket:
    def __init__(self, path=os.getcwd() + r'\ticket.jpg'):
        try:
            self.image = Image.open(path).convert("RGBA")
        except Exception as e:
            print("Can't open ticket image: " + e)
        self.width, self.height = self.image.size

    def add_img(self, image, coords):
        self.image.paste(image, coords, image)
        return self.image

    def add_text(self, text, coord,
                 font_family="Arial",
                 font_size=50,
                 color=(0, 0, 0)):
        print(os.getcwd()+"/project/Fonts/{}.otf".format(font_family))
        font = ImageFont.truetype(
            os.getcwd()+"/Fonts/{}.otf".format(font_family), font_size
            )
        print('kek')
        draw = ImageDraw.Draw(self.image)
        text = str(text)
        if str(coord['x']) == "center":
            w, h = draw.textsize(text, font=font)
            coord['x'] = (self.width - w) / 2
        if str(coord['y']) == "center":
            w, h = draw.textsize(text, font=font)
            coord['y'] = (self.height - h) / 2

        draw.text(
            tuple(coord.values()),
            text,
            color,
            font=font
        )
        return self.image

    def save(self):
        self.image.save("ticket1.png")
        return self.image

    def __exit__(self):
        self.image.close()


class Barcode:
    def __init__(self, code, type='code128'):
        self.barcode = io.BytesIO()
        self.EAN = BCLibrary.generate(type,
                                      str(code),
                                      writer=ImageWriter(),
                                      output=self.barcode)
        self.barcode = Image.open(self.barcode).convert("RGBA")
        self.width, self.height = self.barcode.size

    def crop(self, crop_values):
        self.barcode = self.barcode.crop((
            crop_values[0],
            crop_values[1],
            self.width - crop_values[2],
            self.height - crop_values[3]
        ))
        return self.barcode

    def scale(self, percent_value):
        new_width = int(self.width + self.width * percent_value)
        new_height = int(new_width * self.height / self.width)
        self.barcode = self.barcode.resize((new_width, new_height),
                                           Image.ANTIALIAS)
        self.width, self.height = self.barcode.size
        return self.barcode

    def __exit__(self):
        self.barcode.close()


ticket_example = {
    "text": [
        {
            "size": 80,
            "font_family": "Gilroy-Bold",
            "color": (0, 0, 0),
            "text": "12345",
            "coord": {
                'x': 705,
                'y': 1720
            }
        },
        {
            "size": 50,
            "font_family": "Gilroy-Light",
            "color": (0, 0, 0),
            "text": "Ковальчук Владислав",
            "coord": {
                'x': "center",
                'y': 880
            }
        }
    ],
    "barcodes": [
        {
            "width": 100,
            "crop": (30, 40, 30, 240),  # left/upper/rigth/lower
            "scale": 0.5,
            "type": "code128",
            "code": "AIS12345",
            "coords": (40, 1720)
        }
    ],
    "picture": {
        "file": "ticket.jpg",
    }
}


def add_barcode(barcode, ticket):
    BC = Barcode(barcode['code'])
    BC.scale(barcode['scale'])
    BC.crop(barcode['crop'])
    ticket.add_img(BC.barcode, barcode['coords'])


def add_text(text, ticket):
    ticket.add_text(
        text['text'],
        text['coord'],
        text['font_family'],
        text['size'],
        text['color']
    )


def create_ticket(pic, barcodes=None, texts=None):
    ticket = Ticket(pic['file'])

    if barcodes:
        for bc in barcodes:
            add_barcode(bc, ticket)

    if texts:
        for text in texts:
            add_text(text, ticket)

    imgByteIo = io.BytesIO()
    ticket.image.save(imgByteIo, 'PNG')
    # ticket.image.show()
    ticket.save()
    imgByteIo.seek(0)
    return io.BufferedReader(imgByteIo)


# def vk_ticket(user_id):
#     ticket = create_ticket(pic=ticket_example['picture'],
#                            barcodes=ticket_example['barcodes'],
#                            texts=ticket_example['text'])
#     # url = vkapi.get_photos_upload_server(user_id)
#     # r = requests.post(url['upload_url'], files={
#     #     'photo': (
#     #         'example.png',
#     #         ticket,
#     #         'image/png'
#     #     )
#     # })
#     # req = json.loads(r.text)
#     # answer = vkapi.doc_save(req['server'], req['photo'], req['hash'])
#     # return 'photo%s_%s' % (answer[0]['owner_id'], answer[0]['id'])
#
#
#
# print(vk_ticket(21766756))
def ticket_template(code, barcode, fio, faculty):
    ticket_example = {
        "text": [
            {
                "size": 220,
                "font_family": "Museo900",
                "color": (255, 255, 255),
                "text": code,
                "coord": {
                    'x': 135,
                    'y': 2240
                }
            },
            {
                "size": 70,
                "font_family": "Museo900",
                "color": (255, 255, 255),
                "text": fio,
                "coord": {
                    'x': 620,
                    'y': 2300
                }
            },
            {
                "size": 80,
                "font_family": "Museo900",
                "color": (255, 255, 255),
                "text": faculty,
                "coord": {
                    'x': 990,
                    'y': 2428
                }
            }
        ],
        "barcodes": [
            {
                "width": 100,
                "crop": (30, 150, 30, 750),  # lfeft/upper/rigth/lower
                "scale": 3,
                "type": "code128",
                "code": barcode,
                "coords": (20, 2570)
            }
        ],
        "picture": {
            "file": "ticket.png",
        }
    }
    return ticket_example


# if __name__ == "__main__":
#     member = DB.get_abit_by_vk(59015208)
#     try:
#         member_ticket = DB.add_ticket({
#             'vk': int(member['vk']),
#             'name': member['full_name'],
#             'faculty': member['faculty'],
#             'pic': member['pic'],
#         })
#     except:
#         member_ticket = DB.inform_tickets.find_one({"vk": 59015208})
#     ticketid = member_ticket['id']
#     temp = ticket_template(
#         ticketid,
#         '1NFORM-' + '0000'[0: 4 - len(str(ticketid))] + str(ticketid),
#         """{}
# {}""".format(member_ticket['name'].split(' ')[1], member_ticket['name'].split(' ')[0]),
#         member_ticket['faculty']
#     )
#     ticket = create_ticket(
#         pic=temp['picture'],
#         barcodes=temp['barcodes'],
#         texts=temp['text']
#     )

#     id = 521
#     temp = ticket_template(
#         id,
#         '1NFORM-' + '0000'[0: 4 - len(str(id))] + str(id),
#         """Владислав
# Ковальчук""",
#         "ИСиТ"
#     )
#     ticket = create_ticket(
#         pic=temp['picture'],
#         barcodes=temp['barcodes'],
#         texts=temp['text']
#     )
