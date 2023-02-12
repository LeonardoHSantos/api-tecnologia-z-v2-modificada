import mysql.connector
import config_db

def connetion_db():
    conn = mysql.connector.connect(
        host=config_db.HOST,
        user=config_db.USER,
        password=config_db.PASSWORD,
        database=config_db.NAME,
    )
    return conn