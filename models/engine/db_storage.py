#!/usr/bin/python3
"""Start link class to table in database"""
import os
from sqlalchemy import (create_engine)
from sqlalchemy.orm import sessionmaker, scoped_session
from models.base_model import Base


class DBStorage:
    """this is a class"""
    __engine = None
    __session = None

    def __init__(self):
        user = os.getenv("HBNB_MYSQL_USER")
        password = os.getenv("HBNB_MYSQL_PWD")
        host = os.getenv("HBNB_MYSQL_HOST")
        db = os.getenv("HBNB_MYSQL_DB")
        env = os.getenv("HBNB_ENV")
        self.__engine = create_engine(
            'mysql+mysqldb://{}:{}@{}/{}'.format(user, password, host, db),
            pool_pre_ping=True)
        Base.metadata.create_all(self.__engine)        
        if env == "test":
            for tbl in Base.metadata.sorted_tables:
                tbl.drop(engine)

    def all(self, cls=None):
        dict = {}
        print(cls)
        if cls:
            s = self.__session.query(cls).all()
            for val in s:
                dict = {"{}.{}".format(cls.__name__, val.id): val}
        else:
            for table in self.__engine.table_names():
                for val in table:
                    dict = {"{}.{}".format(cls.__name__, val.id): val}
        print(dict)
        return dict

    def new(self, obj):
        """new to database"""
        self.__session.add(obj)
        self.__session.commit()


    def save(self):
        """adding save"""
        self.__session.commit()

    def delete(self, obj=None):
        """delete"""
        self.__session.delete(obj)
        self.__session.commit()

    def reload(self):
        """reload"""
        Base.metadata.bind = self.__engine
        Base.metadata.create_all()
        session = sessionmaker(bind=self.__engine, expire_on_commit=False)
        S = scoped_session(session)
        self.__session = S()