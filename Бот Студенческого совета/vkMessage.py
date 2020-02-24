import vkapi

class vkMessage:


   def __init__(self, message, attachment = '', user_id = '', peer_id = '' , lat = '', long = '', keyboard = ''):
       self.message = message
       self.attachment = attachment
       self.user_id = user_id
       self.peer_id = peer_id
       self.coord = {'lat': lat, 'long':long}
       self.keyboard = keyboard


   def not_empty(self):
       return self.message or self.attachment


   def send(self):
       if self.not_empty():
           if int(self.peer_id) < 2000000000:
               return vkapi.send_private(self)
           else:
               return vkapi.send_conversation(self)
       else:
           return 0


   # def show(self):
   #      print('message = ' + str(self.message))
   #      print('\n')
   #      print('attachment = ' + str(self.attachment))
   #      print('\n')
   #      print(self.coord)
   #      print('\n')
