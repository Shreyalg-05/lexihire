import mysql.connector
from config import DB_CONFIG

class Database:
    @staticmethod
    def get_connection():
        return mysql.connector.connect(**DB_CONFIG)
