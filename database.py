# DB 연결
import psycopg2

dataSource = {
    "dbname" : "weather_project",
    "user" : "postgres",
    "password" : "1234",
    "host" : "192.168.56.10",
    "port" : "5432"
}


class dbConfig() :
    
    def __init__(self) -> None:
        pass


    def db_connect(self) :
        con = psycopg2.connect(**dataSource)
        return con
    

    # INSERT, UPDATE, DELETE
    def exeute(self, qry, args) :
        conn = self.db_connect()
        cursor = conn.cursor()
        cursor.execute(qry, args)
        conn.commit()
        conn.close()


    # SELECT (한 개)
    def readOne(self, qry, args) :
        conn = self.db_connect()
        cursor = conn.cursor()
        cursor.execute(qry, args)
        result = cursor.fetchone() 
        conn.close()

        return result


    # SELECT (여러 개)
    def read(self, qry, args) :
        conn = self.db_connect()
        cursor = conn.cursor()
        cursor.execute(qry, args)
        result = cursor.fetchall()
        conn.close()

        return result


    



