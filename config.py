import os

class Config:
    DATA_FOLDER = './backend/data'
    DATABASE_FILE = os.path.join(DATA_FOLDER, 'database.json')
    SQLITE_DB = os.path.join(DATA_FOLDER, 'users.db') # ./data/users.db