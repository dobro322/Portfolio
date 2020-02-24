import command_system
import random
from vkMessage import vkMessage

def lera(str, peer_id):
    message = vkMessage('')
    for i in lera_command.keys:
        if i in str:
            glasnye = 'аеиоуы'
            soglasnye = ['б','в','г','д','ж','з','к','л','м','н','п','р','с','т','х','ч','ш']

            lg=len(glasnye) - 1
            ls=len(soglasnye) - 1

            def sogl(word):
                a = soglasnye[random.randint(0,ls)]
                while a == word[-1]:
                    a = soglasnye[random.randint(0,ls)]
                return a

            def gl(word):
                a = glasnye[random.randint(0,lg)]
                while a == word[-1]:
                    a = glasnye[random.randint(0,lg)]
                return a

            fam = ''
            fam += 'П'
            fam += gl(fam)
            fam += 'бе'
            fam += sogl(fam)
            fam += gl(fam)
            fam += sogl(fam)
            if fam[-1] == "ч":
                fam += "к"
            fam += gl(fam)
            fam += 'ва'
            message.message = fam.capitalize()
            return message
    return message

lera_command = command_system.Command()

lera_command.keys = ['напомни фамилию леры']
lera_command.description = ''
lera_command.process = lera
