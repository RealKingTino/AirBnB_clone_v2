#!/usr/bin/python3
""" State Module for HBNB project """
from os import environ
from sqlalchemy import Column, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from models.base_model import BaseModel, Base

class State(BaseModel, Base):
    """ State class """
    storage_type = environ.get('HBNB_TYPE_STORAGE', 'file')

    __tablename__ = "states"
    name = Column(String(128), nullable=False)

    cities = relationship('City', backref='state', cascade='all, delete')
    if storage_type == 'db':
        from models.city import City
    else:
        name = ""

    # For FileStorage
    if storage_type != 'db':
        @property
        def cities(self):
            """Getter attribute cities that returns the list of City instances
               with state_id equals to the current State.id
            """
            from models import storage, City
            city_objs = []
            for city in storage.all(City).values():
                if city.state_id == self.id:
                    city_objs.append(city)
            return city_objs
