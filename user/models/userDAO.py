from database import dbConfig as db


class userDAO():

    def __init__(self) :
        self.db = db()
        

    # 회원가입
    def insertUser(self, data):
        qry =  '''
            INSERT INTO 
                weather_user(user_email, user_pwd, user_name) 
            VALUES 
                ( %(email)s, md5(%(password)s), %(name)s )
        '''
        self.db.exeute(qry, data)


    # 이메일로 사용자 찾기
    def selectUserByEmail(self, data) : 
        qry = '''
            SELECT 
                user_email, user_pwd, user_name 
            FROM 
                weather_user 
            WHERE 
                user_email = %(email)s
        '''
        return self.db.readOne(qry, data)

