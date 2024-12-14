from sqlalchemy import create_engine
import os


class dbConnectionEngine:
   def get_engine(self):
        url = os.getenv('DATABASE_URL')  # или другой способ получения строки подключения
        if not url:
         raise ValueError("DATABASE_URL is not set or is invalid")
        engine = create_engine("postgresql://postgres:0180@localhost:5432/FitnessAppDB", pool_size=50, echo=False)
        return engine
