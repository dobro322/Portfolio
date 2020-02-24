import vkapi

class vkMessage:
   def __init__(self, message, attachment = '', user_id = '', peer_id = '' , lat = '', long = ''):
       self.message = message
       self.attachment = attachment
       self.user_id = user_id
       self.peer_id = peer_id
       self.coord = {'lat': lat, 'long':long}

   def isEmpty(self):
       return self.message or self.attachment

   def send(self):
       if self.isEmpty():
           if int(self.peer_id) < 2000000000:
               vkapi.send_chat(self)
           else:
               vkapi.send_dialog(self)
       else:
           print('No message or attachment')


   # def show(self):
   #      print('message = ' + str(self.message))
   #      print('\n')
   #      print('attachment = ' + str(self.attachment))
   #      print('\n')
   #      print(self.coord)
   #      print('\n')
