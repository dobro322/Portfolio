from string import Template
import string

Button = Template("""
    {
        "action": {
          "type": "text",
          "payload": "$payload",
          "label": "$label"
        },
        "color": "$color"
      }""")

colors = {'red':'negative',
          'green':'positive',
          'white':'default',
          'blue':'primary'}

class KeyBoard:
    def __init__(self, one_time = 'false', rows = 2):
        self.keyboard = """{"one_time":false,
                         "buttons":["""
        self.rows = rows
        self.one_time = one_time
        self.Buttons = []
        self.buttonCount = 0


    def addButton(self, label = 'button', color = 'red', payload = '{"button":"1"}'):
        self.Buttons.append({'label' : label,
                        'color' : color,
                        'payload' : payload})
        self.buttonCount += 1

    def getButton(self):
        for k, button in enumerate(self.Buttons, 1):
            if not (k - 1) % self.rows:
                self.keyboard += '['
            self.keyboard += Button.substitute(payload = button['payload'], label = button['label'], color = colors[button['color']]) + ','
            if (not k % self.rows) or k == len(self.Buttons):
                self.keyboard = self.keyboard[:-1] + '],'
        if self.Buttons:
            self.Buttons = []
            return self.keyboard[:-1]+']}'


    def getWithMenuButton(self):
        self.getButton()
        self.keyboard = self.keyboard[:-1] + ',['
        self.keyboard += Button.substitute(payload = '{\\"text\\":\\"''\\"}', label = 'Меню', color = colors['blue']) + ']]}'
        return self.keyboard
