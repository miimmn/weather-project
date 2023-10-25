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

    def dbConnect(self) :
        con = psycopg2.connect(**dataSource)
        return con

    
    


    



