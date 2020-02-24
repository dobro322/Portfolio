import command_system
import random
from vkMessage import vkMessage

def styopa(str, peer_id):
    message = vkMessage('')
    for i in styopa_command.keys:
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
            fam += 'с'
            fam += sogl(fam)
            if fam == 'сз' or fam == 'сж':
                fam = 'ж'
            fam += gl(fam)
            fam += 'п'
            fam += 'a'
            fam += sogl(fam)
            fam += gl(fam)
            fam += sogl(fam)
            if fam[-1] == 'к':
                fam = fam[0:-1]
            fam += 'ков'
            message.message = fam.capitalize()
            return message
    return message

styopa_command = command_system.Command()

styopa_command.keys = ['напомни фамилию гриши']
styopa_command.description = ''
styopa_command.process = styopa
