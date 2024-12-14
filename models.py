from sqlalchemy import Column, Integer, String, Float
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    username = Column(String, nullable=False, unique=True)
    email = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    weight = Column(Float, nullable=True)
    height = Column(Float, nullable=True)
    gender = Column(String, nullable=True)
    balance = Column(Float, default=0)
    lives = Column(Integer, default=0)
    programs = Column(String, nullable=True)

    @staticmethod
    def create_default_user(session):
        """Создание первоначальной записи пользователя."""
        default_user = User(
            username='admin',
            email='admin@mail.ru',
            password='123456',  
            weight=70,
            height=175,
            gender='M',
            balance=100,
            lives=5,
            programs='default_program'
        )
        session.add(default_user)
        session.commit()
