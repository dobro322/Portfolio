import barcode
from barcode.writer import ImageWriter
from PIL import Image
import os

class Barcode:
    def __init__(self, code, codeType = 'code128'):
        self.EAN = barcode.get_barcode_class(codeType)
        self.path = self.generateBarcode(code, 'barcode' + str(code))
        self.barcodeImage = Image.open(self.path).convert("RGBA")
        self.width, self.height = self.barcodeImage.size
        self.width = self.width + 150
        self.height = int( self.width * self.height / (self.width - 150) )
        self.barcodeImage =  self.barcodeImage.resize((self.width, self.height), Image.ANTIALIAS)
        self.barcodeImage = self.barcodeCrop((30, 40, self.width - 30, self.height - 250))


    def generateBarcode(self, code, name = 'barcode'):
        code = str(code)
        ean = self.EAN(code, writer=ImageWriter())
        try:
            return ean.save(os.getcwd() + '\Barcodes\\' + name)
        except:
            return ean.save(os.getcwd() + '/VKBot/Barcodes/' + name)

    def barcodeCrop(self, cropSize):
        return self.barcodeImage.crop(cropSize)



    def __exit__(self):
        self.barcodeImage.close()
