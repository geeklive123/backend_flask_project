import os

class Config:
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:2021@localhost:3307/sobramat_db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False