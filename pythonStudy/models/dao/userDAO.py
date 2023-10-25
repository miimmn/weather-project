import database as db
from database import dbConfig as db


class userDAO():

    def __init__(self) :
        self.db = db()


    def insertUser(self, data):
        con = self.db.dbConnect()
        cursor = con.cursor()

        cursor.execute(
            'INSERT INTO weather_user(user_email, user_pwd, user_name) VALUES (%s, %s, %s)', data)
        con.commit()

        cursor.close()
        con.close()


    def selectUserByEmail(self, email) : 
        con = self.db.dbConnect()
        cursor = con.cursor()

        cursor.execute('SELECT user_email, user_pwd, user_name FROM weather_user WHERE user_email = %s', [email])
        userInfo = cursor.fetchone()

        cursor.close()
        con.close()

        return userInfo
    

