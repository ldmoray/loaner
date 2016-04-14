import argparse
from prettytable import PrettyTable
import datetime
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
    person_name = Column(String, nullable=False, default='')
    # Contact information of the person
    person_information = Column(String, nullable=False, default='')

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

# Database connection setup
engine = create_engine('sqlite:///data.db')
Base.metadata.create_all(engine)
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()

def print_items (items):
    table = PrettyTable(['ID', 'Item Name', 'Item Location', 'Lent', 'Person Name', 'Person Info'])
    for item in items:
        table.add_row([item.id, item.name, item.location, item.lent, item.person_name, item.person_information])
    print table

def print_transactions (transactions):
    table = PrettyTable(['Type', 'Item Name', 'Item Location', 'Person Name', 'Person Info', 'Time Stamp'])
    for t in transactions:
        table.add_row([t.type, t.item_name, t.item_location, t.person_name, t.person_information, t.timestamp])
    print table

def _find (args):
    query = session.query(Item)
    query = query.filter(Item.id.like('%' + args.id + '%'))
    query = query.filter(Item.name.like('%' + args.name + '%'))
    query = query.filter(Item.location.like('%' + args.location + '%'))
    items = query.all()
    print_items(items)

def _add (args):
    item = Item(name=args.name, location=args.location)
    session.add(item)
    session.commit()
    print 'Item has been added'
    print_items([item])

def _remove (args):
    item = session.query(Item).get(args.id)
    if item is None:
        print 'Unable to find item with given id of ' + args.id
    elif item.lent:
        print 'You cannot remove an item that is currently lent out'
    else:
        session.delete(item)
        print 'Item has been removed'
        print_items([item])
        session.commit()

def _update (args):
    item = session.query(Item).get(args.id)
    if item is None:
        print 'Unable to find item with given id of ' + args.id
    elif item.lent:
        print 'You cannot update an item that is currently lent out'
    else:
        name = item.name if args.name == '' else args.name
        location = item.location if args.location == '' else args.location
        item.name = name
        item.location = location
        print 'Item has been updated'
        print_items([item])
        session.commit()

def _lend (args):
    item = session.query(Item).get(args.id)
    if item is None:
        print 'Unable to find item with given id of ' + args.id
    elif item.lent:
        print 'You cannot lend an item that is currently lent out'
    else:
        item.lent = True
        item.person_name = args.name
        item.person_information = args.info
        transaction = Transaction(type='Lend', item_name=item.name, item_location=item.location, person_name=args.name, person_information=args.info)
        session.add(transaction)
        print 'Item has been lent'
        print_items([item])
        session.commit()

def _return (args):
    item = session.query(Item).get(args.id)
    if item is None:
        print 'Unable to find item with given id of ' + args.id
    elif not item.lent:
        print 'You cannot return an item that is not currently lent out'
    else:
        transaction = Transaction(type='Return', item_name=item.name, item_location=item.location, person_name=item.person_name, person_information=item.person_information)
        item.lent = False
        item.person_name = ''
        item.person_information = ''
        session.add(transaction)
        print 'Item has been returned'
        print_items([item])
        session.commit()

def _log (args):
    query = session.query(Transaction)
    query = query.filter(Transaction.type.like('%' + args.type + '%'))
    query = query.filter(Transaction.item_name.like('%' + args.item_name + '%'))
    query = query.filter(Transaction.item_location.like('%' + args.item_location + '%'))
    query = query.filter(Transaction.person_name.like('%' + args.person_name + '%'))
    query = query.filter(Transaction.person_information.like('%' + args.person_info + '%'))
    items = query.all()
    print_transactions(items)

# Main argument parser
parser = argparse.ArgumentParser()
# Sub parsers for main argument parser
subparsers = parser.add_subparsers()

# Find item sub parser command
find_parser = subparsers.add_parser('find', help='find an item')
find_parser.add_argument('--id', '-i', help='id number of the item', nargs='?', default='%')
find_parser.add_argument('--name', '-n', help='full or partial name of the item', nargs='?', default='%')
find_parser.add_argument('--location', '-l', help='full or partial location of the item', nargs='?', default='%')
find_parser.set_defaults(action='find')

# Add item sub parser command
add_parser = subparsers.add_parser('add', help='add a new item')
add_parser.add_argument('name', help='name of the new item')
add_parser.add_argument('location', help='location of the new item')
add_parser.set_defaults(action='add')

# Remove item sub parser command
remove_parser = subparsers.add_parser('remove', help='remove an item, item must not be currently lent out')
remove_parser.add_argument('id', help='id of the item to remove')
remove_parser.set_defaults(action='remove')

# Update item sub parser command
update_parser = subparsers.add_parser('update', help='update an item, item must not be currently lent out')
update_parser.add_argument('id', help='id of the item to update')
update_parser.add_argument('--name', '-n', help='new name for the selected item', default='')
update_parser.add_argument('--location', '-l', help='new location for the selected item', default='')
update_parser.set_defaults(action='update')

# Lend item sub parser command
lend_parser = subparsers.add_parser('lend', help='lend an item, item must not be currently lent out')
lend_parser.add_argument('id', help='id of the item to lend')
lend_parser.add_argument('name', help='name of the person lending to')
lend_parser.add_argument('info', help='contact info of the person lending to')
lend_parser.set_defaults(action='lend')

# Return item sub parser command
return_parser = subparsers.add_parser('return', help='return an item, item must be currently lent out')
return_parser.add_argument('id', help='id of the item to return')
return_parser.set_defaults(action='return')

# Return item sub parser command
log_parser = subparsers.add_parser('log', help='find a transaction log')
log_parser.add_argument('--type', '-t', help='full or partial type of the transaction', nargs='?', default='%')
log_parser.add_argument('--item-name', '-n', help='full or partial name of the item', nargs='?', default='%')
log_parser.add_argument('--item-location', '-l', help='full or partial location of the item', nargs='?', default='%')
log_parser.add_argument('--person-name', '-p', help='full or partial name of the person', nargs='?', default='%')
log_parser.add_argument('--person-info', '-i', help='full or partial information of the person', nargs='?', default='%')
log_parser.set_defaults(action='log')

# Parse the arguments
args = parser.parse_args()

# Call sub parser function
if args.action == 'find':
    _find(args)
elif args.action == 'add':
    _add(args)
elif args.action == 'remove':
    _remove(args)
elif args.action == 'update':
    _update(args)
elif args.action == 'lend':
    _lend(args)
elif args.action == 'return':
    _return(args)
elif args.action == 'log':
    _log(args)
