import sqlite3
import random
import pandas as pd

def transliterate(name):
    slovar = {'а':'a','б':'b','в':'v','г':'g','д':'d','е':'e','ё':'e',
              'ж':'zh','з':'z','и':'i','й':'i','к':'k','л':'l','м':'m','н':'n',
              'о':'o','п':'p','р':'r','с':'s','т':'t','у':'u','ф':'f','х':'h',
              'ц':'c','ч':'cz','ш':'sh','щ':'scz','ъ':'','ы':'y','ь':'','э':'e',
              'ю':'u','я':'ja', 'А':'A','Б':'B','В':'V','Г':'G','Д':'D','Е':'E','Ё':'E',
              'Ж':'ZH','З':'Z','И':'I','Й':'I','К':'K','Л':'L','М':'M','Н':'N',
              'О':'O','П':'P','Р':'R','С':'S','Т':'T','У':'U','Ф':'F','Х':'H',
              'Ц':'C','Ч':'CZ','Ш':'SH','Щ':'SCH','Ъ':'','Ы':'y','Ь':'','Э':'E',
              'Ю':'U','Я':'YA',',':'','?':'',' ':'_','~':'','!':'','@':'','#':'',
              '$':'','%':'','^':'','&':'','*':'','(':'',')':'','-':'','=':'','+':'',
              ':':'',';':'','<':'','>':'','\'':'','"':'','\\':'','/':'','№':'',
              '[':'',']':'','{':'','}':'','ґ':'','ї':'', 'є':'','Ґ':'g','Ї':'i',
              'Є':'e', '—':''}

    for key in slovar:
        name = name.replace(key, slovar[key])
    return name

def password_generation():
    password = ''
    for i in range(10):
        password += str(random.randint(0, 9))
    return password

def login_generation(fam, nam, ot):
    return transliterate(fam.lower()) + '_' + transliterate(nam.lower()[0]) + transliterate(ot.lower()[0])


class Rules:
    def connect_to_db(self):
        self.connect = sqlite3.connect("vr_course.db")
        self.cursor = self.connect.cursor()

    def close(self):
        self.connect.close()

    def check_role(self, _id=0):
        self.connect_to_db()
        request = "SELECT description FROM rules WHERE id = ?"
        result = self.cursor.execute(request, (_id,)).fetchall()
        self.close()
        return result[0][0]


class Students:
    def connect_to_db(self):
        self.connect = sqlite3.connect("vr_course.db")
        self.cursor = self.connect.cursor()

    def close(self):
        self.connect.close()

    def add_group(self, group_id, teacher_id, group_name, description):
        self.connect_to_db()
        request = "INSERT INTO groups(group_id, teacher_id, group_name, description) VALUES(?, ?, ?, ?)"
        self.cursor.execute(request, (group_id, teacher_id, group_name, description))
        self.connect.commit()
        self.close()

    def add_group(self):
        self.connect_to_db()
        request = "SELECT group_id FROM groups "
        result = self.cursor.execute(request).fetchall()
        self.close()
        return [i[0] for i in result]

    def add_user(self, group_id, teacher_id, first_name, surname, last_name):
        self.connect_to_db()
        login = login_generation(last_name, first_name, surname)
        password = password_generation()
        request = "INSERT INTO users(login, group_id, teacher_id, password, first_name, surname, last_name) VALUES(?, ?, ?, ?, ?, ?, ?)"
        self.cursor.execute(request, (login, group_id, teacher_id, password, first_name, surname, last_name))
        self.connect.commit()
        self.close()

    def get_pass(self, login):
        self.connect_to_db()
        try:
            request = "SELECT password FROM users WHERE login = ?"
            result = self.cursor.execute(request, (login,)).fetchall()
            self.close()
            return result[0][0]
        except:
            self.close()
            return 0



    def add_log(self, _id, name, login, group_id, teacher_id, test_id, score, mark, datetime):
        self.connect_to_db()
        request = "INSERT INTO log(id, name, login, group_id, teacher_id, test_id, score, mark, datetime) VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?)"
        self.cursor.execute(request, (_id, name, login, group_id, teacher_id, test_id, score, mark, datetime))
        self.connect.commit()
        self.close()

    def sql_to_df(self, _list=True, table='users'):
        self.connect_to_db()
        data_frame = pd.read_sql_query(f'SELECT * FROM {table}', self.connect)
        self.close()
        if _list:
            return data_frame.values.tolist()
        return data_frame
