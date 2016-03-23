# Configuration:

from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine

# Type of class to be inherited
Base = declarative_base()


# Class + Table + Mappers
class Restaurant(Base):

    __tablename__ = 'restaurant'

    id = Column(Integer, primary_key=True)
    name = Column(String(80), nullable=False)

    @property
    def serialize(self):
        return {
            'name': self.name,
            'id': self.id,
        }


# Class + Table + Mappers
class MenuItem(Base):

    __tablename__= 'menu_item'

    id = Column(Integer, primary_key=True)
    name = Column(String(80), nullable=False)
    course = Column(String(250))
    description = Column(String(250))
    price = Column(String(8))
    restaurant_id = Column(Integer, ForeignKey('restaurant.id'))
    restaurant = relationship(Restaurant)

    @property
    def serialize(self):
        # Returns object data in easily serializeable format
        return {
            'name': self.name,
            'price': self.price,
            'course': self.course,
            'description': self.description,
            'id': self.id,
        }


# Configuration:
engine = create_engine('sqlite:///restaurantmenu.db')
Base.metadata.create_all(engine)