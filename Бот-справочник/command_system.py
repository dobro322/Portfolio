command_list = []

class Command:
   def __init__(self):
       self.__keys = ''
       self.description = ''
       command_list.append(self)

   @property
   def keys(self):
       return self.__keys

   @keys.setter
   def keys(self, mas):
       for k in mas:
           self.__keys += k.lower()

   def process(self):
       pass

   def deephelp(self):
       return 'This is just a simple func'
