from sqlalchemy import create_engine

class dbConnectionEngine:
    def __init__(self, database_url=None):
        self.database_url = database_url or 'sqlite:///test.db'  

    def get_engine(self):
        return create_engine(self.database_url)
