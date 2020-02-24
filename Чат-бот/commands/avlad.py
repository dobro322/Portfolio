import command_system
import random
from vkMessage import vkMessage

def vlad(str, peer_id):
    message = vkMessage('')
    for i in vlad_command.keys:
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
            fam += 'К'
            fam += gl(fam)
            fam += 'чк'
            fam += gl(fam)
            fam += ' '
            fam += sogl(fam)
            fam += gl(fam)
            fam += 'к'
            message.message = fam.capitalize()
            return message
    return message

vlad_command = command_system.Command()

vlad_command.keys = ['напомни фамилию Влада']
vlad_command.description = ''
vlad_command.process = vlad
