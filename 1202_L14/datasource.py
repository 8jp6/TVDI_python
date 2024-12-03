import psycopg2
from dotenv import load_dotenv
import os
load_dotenv()

#環境變數
Postgres_HOST=os.getenv('Postgres_HOST')
Postgres_DB=os.getenv('Postgres_DB')
Postgres_Password=os.getenv('Postgres_Password')
Postgres_User=os.getenv('Postgres_User')
a='a'


def get_cities()->list[dict]:
    conn = psycopg2.connect(database = Postgres_DB, user = Postgres_User, host = Postgres_HOST, password =Postgres_Password)
    with conn as c:
        cursor = conn.cursor()
        with cursor as cu:
            cursor.execute('SELECT * FROM city')
            data:list[tuple] = cursor.fetchall()

    #list comprehension
    transfer_data:list[dict] = [{'_id':i[0],
                                'citys.db':i[1],
                                'continent':i[2],
                                'country':i[3],
                                'image':i[4]
                                } for i in data]
    return transfer_data