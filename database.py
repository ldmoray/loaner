import datetime
import sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy import Column, Integer, String, Boolean, DateTime
from sqlalchemy.ext.declarative import declarative_base

# Class base
Base = declarative_base()

class Item (Base):
    # Item table
    __tablename__ = 'item'
    # ID of the item. Required
    id = Column (Integer, primary_key=True)
    # Name of the item. Required
    name = Column(String, nullable=False)
    # Location of the item. Required
    location = Column(String, nullable=False)
    # Is the item lent? Default: False
    lent = Column(Boolean, nullable=False, default=False)
    # Name of the person
    person_name = Column(String)
    # Contact information of the person
    person_information = Column(String)

    # Self representation string
    def __repr__ (self):
        # Return self representation
        return "<Item(name='%s', location='%s', lent='%s', person_name='%s', person_information='%s')>" % (self.name, self.location, self.lent, self.person_name, self.person_information)

class Transaction (Base):
    # Transaction table
    __tablename__ = 'transaction'
    # ID of the transaction
    id = Column (Integer, primary_key=True)
    # Type of transaction. Required
    type = Column(String, nullable=False)
    # Name of the item in the transaction. Required.
    item_name = Column(String, nullable=False)
    # Location of the item in the transaction. Required.
    item_location = Column(String, nullable=False)
    # Name of the person in the transaction. Required.
    person_name = Column(String, nullable=False)
    # Contact information of the person in the transaction. Required.
    person_information = Column(String, nullable=False)
    # Time stamp of this transaction. Default: Current Timestamp
    timestamp = Column(DateTime, nullable=False, default=datetime.datetime.utcnow)

    # Self representation string
    def __repr__ (self):
        # Return self representation
        return "<Transaction(type='%s, item_name='%s', item_location='%s', person_name='%s', person_information='%s', timestamp='%s')>" % (self.type, self.item_name, self.item_location, self.person_name, self.person_information, self.timestamp)

engine = create_engine('sqlite:///test.db')
Base.metadata.create_all(engine)
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()

item = Item(name='Windows 10 x86_64', location='Tower 1/1')
session.add(item)
session.commit()

transaction = Transaction(type='Lend', item_name='CentOS', item_location='Tower 1/2', person_name='Zachariah T. Dzielinski', person_information='(240) 818-4962')
session.add(transaction)
session.commit()

items = session.query(Item).all()
for i in items:
    print i

transactions = session.query(Transaction).all()
for t in transactions:
    print t
