import Vk
from mysql.connector import MySQLConnection, Error

def get_data(query, args=''):
    conn = MySQLConnection(**dbconfig)
    cursor = conn.cursor(buffered=True)
    cursor.execute(query, args)
    answer = cursor.fetchone()
    conn.close()
    cursor.close()
    return answer


def get_all_data(query, args=''):
    conn = MySQLConnection(**dbconfig)
    cursor = conn.cursor(buffered=True)
    cursor.execute(query, args)
    answer = cursor.fetchall()
    conn.close()
    cursor.close()
    return answer


def insert_data(query, args=''):
    try:
        conn = MySQLConnection(**dbconfig)
        cursor = conn.cursor()
        cursor.execute(query, args)
        conn.commit()
        conn.close()
        cursor.close()
        if cursor.lastrowid:
            return cursor.lastrowid
        else:
            return 0
    except Error as e:
        return 'Can\'t insert Data to DataBase:\n' + str(e)


class Users():
    def __init__(self, sub_id):
        self.sub_id = sub_id
        self.initialize()

    def initialize(self):
        query = """
        SELECT *
        FROM User_sub
        WHERE Sub_id = %s
        """
        args = (self.sub_id, )
        res = get_all_data(query, args)
        self._users = res

    def get(self):
        return self._users


class User():
    def __init__(self, id):
        self.id = id

    def initialize(self):
        user = Vk.get_user(self.id)
        self.name = "{} {}".format(user["first_name"], user["last_name"])
        self.id = user["id"]

    def add(self):
        self.initialize()
        query = """
        INSERT INTO User(Id, Name)
        VALUES(%s, %s)
        """
        args = (self.id, self.name.strip())
        return insert_data(query, args)


class Message():
    def add(self, text, attachment, payload, author_id):
        self.text = text
        self.attachment = attachment
        self.payload = payload
        self.author_id = author_id
        query = """
        INSERT INTO Message(Text, Attach, Payload, Author_id)
        VALUES(%s, %s, %s, %s)
        """
        args = (self.text, self.attachment, self.payload, self.author_id)
        return insert_data(query, args)


class Subscriptions():
    def __init__(self, group_id):
        self.group_id = group_id
        self.initialize()

    def initialize(self):
        query = """
        SELECT x.Sub_id, x.Name, x.Keyword, x.Text, x.Gr_id, COUNT(y.User_id) as followers
        FROM Sub_type as x
        LEFT JOIN User_sub as y
        on x.Sub_id = y.Sub_id
        WHERE x.Gr_id = %s
        GROUP BY x.Sub_id
        """
        args = (self.group_id,)
        res = get_all_data(query, args)
        self._subs = res

    def get(self):
        return self._subs


class Subscription():
    def add(self, name, keyword, text, group_id):
        self.name = name
        self.keyword = keyword
        self.text = text
        self.group_id = group_id
        query = """
        INSERT INTO Sub_type(Name, Keyword, Text, Gr_id)
        VALUES(%s, %s, %s, %s)
        """
        args = (self.name.strip(), self.keyword.lower().strip(), self.text.strip(),  self.group_id)
        return insert_data(query, args)

    def change(self, name, keyword, text, id):
        self.name = name
        self.keyword = keyword
        self.text = text
        self.id = id
        query = """
        UPDATE Sub_type
        SET Name = %s,
        Keyword = %s,
        Text = %s
        WHERE Sub_id = %s
        """
        args = (self.name, self.keyword.lower(), self.text, self.id)
        return insert_data(query, args)

    def remove(self, id):
        self.id = id
        query = """
        DELETE FROM Sub_type
        WHERE Sub_id = %s
        """
        args = (self.id,)
        return insert_data(query, args)


class Community():
    def _initialize(self):
        community = Vk.get_community(self._token)
        self.name = community["name"]
        self.id = community["id"]
        self.pic = community["photo_100"]

    def add(self, token, conf_token):
        self._token = token
        self._conf_token = conf_token
        self._initialize()
        query = """
        INSERT INTO Community(Gr_id, Gr_name, Gr_token, Conf_token, Gr_pic)
        VALUES(%s, %s, %s, %s, %s)
        """
        args = (self.id, self.name, self._token, self._conf_token, self.pic)
        insert_data(query, args)
        return self.get()

    def get(self, id=None):
        if id:
            query = """
            SELECT *
            FROM Community
            WHERE Gr_id = %s
            """
            args = (id,)
            res = get_data(query, args)
            self.id = res[0]
            self.name = res[1]
            self._token = res[2]
            self._conf_token = res[3]
            self.pic = res[4]
        return {
            "name": self.name,
            "id": self.id,
            "pic": self.pic,
            "token": self._token,
            "conf_token": self._conf_token
        }


class Mail():
    def add(self, recipient_id, sub_id, text, attachment, author_id, status):
        self.recip_id = recipient_id
        self.sub_id = sub_id
        self.text = text
        self.attachment = attachment
        self.author_id = author_id
        self.status = status
        query = """
        INSERT INTO Mail(User_id, Sub_id, Text, Attach, Author_id, Status)
        VALUES(%s, %s, %s, %s, %s, %s)
        """
        args = (
            self.recip_id,
            self.sub_id,
            self.text,
            self.attachment,
            self.author_id,
            self.status
        )
        return insert_data(query, args)


class User_subscription():
    def add(self, user_id, sub_id):
        self.user_id = user_id
        self.sub_id = sub_id
        query = """
        INSERT INTO User_sub(User_id, Sub_id)
        VALUES(%s, %s)
        """
        args = (self.user_id, self.sub_id)
        return insert_data(query, args)

    def remove(self, sub_id, user_id):
        self.sub_id = sub_id
        self.user_id = user_id
        query = """
        DELETE FROM User_sub
        WHERE Sub_id = %s
        AND User_id = %s
        """
        args = (self.sub_id, self.user_id)
        return insert_data(query, args)

    def get(self, user_id, group_id):
        self.user_id = user_id
        self.group_id = group_id
        query = """
        SELECT *
        FROM Sub_type x
        LEFT JOIN User_sub y
        on x.Sub_id = y.Sub_id
        AND y.User_id = %s
        WHERE x.Gr_id = %s
        """
        args = (user_id, group_id)
        return get_all_data(query, args)


class Admin():
    def __init__(self, login, password=None, group_id=None):
        self.login = login
        self._password = password
        self.group_id = group_id

    def add(self):
        query = """
        INSERT INTO Admin(Login, Password)
        VALUES(%s, %s)
        """
        args = (self.login, self._password)
        return insert_data(query, args)

    def get(self):
        query = """
        SELECT *
        FROM Admin
        WHERE Login = %s
        AND Password = %s
        """
        args = (self.login, self._password)
        res = get_data(query, args)
        return {
            "login": res[0],
            "group_id": res[1]
        }

    def set_gr(self, token, conf_token):
        community = Community().add(token, conf_token)
        self.group_id = community["id"]
        query = """
        UPDATE Admin
        SET Gr_id = %s
        WHERE Login = %s
        """
        args = (self.group_id, self.login)
        insert_data(query, args)
        query = """
        SELECT Login, Gr_id
        FROM Admin
        WHERE Login = %s
        """
        args = (self.login,)
        res = get_data(query, args)
        return {
            "login": res[0],
            "group_id": res[1]
        }
