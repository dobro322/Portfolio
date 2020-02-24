import json

class KeyBoard():
    def __init__(self, columns=1, one_time=True):
        self.columns = columns
        self.buttons_count = 0
        self.template = {
            "one_time": one_time,
            "buttons": []
        }

    def add(self, Button):
        if self.buttons_count % self.columns == 0:
            self.template["buttons"].append([])
        iteration = self.buttons_count // self.columns
        self.template["buttons"][iteration].append(Button.get())

        self.buttons_count += 1


    def get(self):
        return json.dumps(self.template)




class Button(KeyBoard):
    def __init__(self, text, payload, active, color=None):
        self.text = text
        self.payload = payload
        self.active = active
        if color:
            self.color(color)

    def get(self):
        return {
            "action": {
                "type": "text",
                "payload": '{\"sub_id\": \"%s\", \"active\" : \"%s\"}' % (self.payload, self.active)  ,
                "label": self.text
                },
                "color": self.color
        }

    def color(self, color="white"):
        """
        white, blue, red, green
        """
        a = {
            "white": "secondary",
            "blue": "primary",
            "red": "negative",
            "green": "positive"
        }
        self.color = a[color]
