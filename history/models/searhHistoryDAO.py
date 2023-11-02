from database import dbConfig as db


class searchHistoryDAO:

    def __init__(self) :
        self.db = db()


    # 날씨 검색 시 검색 기록 넣기
    def insertSearchHistory(self, data) :
        
        qry =  '''
            INSERT INTO 
                weather_search_history(user_email, history_si, history_gu, history_dong, history_date) 
            VALUES 
                ( %(user_email)s, %(si)s, %(gu)s, %(dong)s, %(history_date)s)
        '''
         
        self.db.exeute(qry, data)


    # 검색 기록 가져오기
    def getSearchHistory(self, data) :

        qry = '''
            SELECT 
                history_id, user_email, history_si, history_gu, history_dong, TO_CHAR(history_date, 'YYYY-MM-DD   HH:MM:SS') 
            FROM 
                weather_search_history 
            WHERE 
                user_email = %(user_email)s
        '''
        return self.db.read(qry, data)
    

    def deleteSearchHistory(self, data) :
        qry = '''
            DELETE
            FROM 
                weather_search_history 
            WHERE 
                history_id = %(history_id)s
        '''
        return self.db.exeute(qry, data)