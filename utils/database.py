
"""
Database utility functions for Resume Analyzer
"""

import pymysql
from pymysql.cursors import DictCursor
import json
from datetime import datetime
from config import Config
import hashlib

class DatabaseManager:
    def __init__(self):
        self.config = {
            'host': Config.DB_HOST,
            'user': Config.DB_USER,
            'password': Config.DB_PASSWORD,
            'database': Config.DB_NAME,
            'port': Config.DB_PORT,
            'charset': 'utf8mb4',
            'cursorclass': DictCursor
        }

    def get_connection(self):
        try:
            connection = pymysql.connect(**self.config)
            return connection
        except pymysql.Error as e:
            print(f"Error connecting to database: {e}")
            raise
