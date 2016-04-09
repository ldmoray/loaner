# Sqlite library
import sqlite3
# Argument parsing library
import argparse
# Pretty table library
from prettytable import PrettyTable

# Sqlite file name
sqlite_file = 'data.sqlite'
# SQL setup file name
sql_file = 'setup.sql'

# Connection instance
conn = sqlite3.connect(sqlite_file)
# Connection cursor
cur = conn.cursor()

# SQL as array from file
sqls = open(sql_file).read().split('--')
# Loop through each query
for sql in sqls:
    # Execute each query
    cur.execute(sql)

# Print a list of items as a pretty table
def print_items (items):
    table = PrettyTable(['ID', 'Item Name', 'Item Location', 'Lent', 'Person Name', 'Person Info'])
    for item in items:
        table.add_row(item)
    print table

# Print a list of logs as a pretty table
def print_logs (logs):
    table = PrettyTable(['Type', 'Item Name', 'Item Location', 'Person Name', 'Person Info', 'Time Stamp'])
    for log in logs:
        table.add_row(log[1:])
    print table

# Find item sub command
def _find (args):
    if args.id == '%':
        qry = "SELECT * FROM item WHERE UPPER(item_name) LIKE UPPER('%{}%') AND UPPER(item_loc) LIKE UPPER('%{}%')"
        items = cur.execute(qry.format(args.name, args.location))
    else:
        qry = "SELECT * FROM item WHERE item_id = '{}' AND UPPER(item_name) LIKE UPPER('%{}%') AND UPPER(item_loc) LIKE UPPER('%{}%')"
        items = cur.execute(qry.format(args.id, args.name, args.location))
    print_items(items)

# Add item sub command
def _add (args):
    qry = "INSERT INTO item (item_name, item_loc) VALUES ('{}', '{}')"
    cur.execute(qry.format(args.name, args.location))
    conn.commit()
    qry = "SELECT * FROM item WHERE item_id = '{}'"
    items = cur.execute(qry.format(cur.lastrowid))
    print 'Item has been added'
    print_items(items)

# Remove item sub command
def _remove (args):
    qry = "SELECT * FROM item WHERE item_id = '{}'"
    items = cur.execute(qry.format(args.id))
    item = cur.fetchone()
    if item == None:
        print 'Item with id of ' + args.id + ' does not exist'
        return
    if item[3] == 'Yes':
        print 'You cannot remove an item that is currently lent out'
        return
    qry = "DELETE FROM item WHERE item_id = '{}'"
    cur.execute(qry.format(args.id))
    conn.commit()
    print 'Item has been removed'
    print_items([item])

# Update item sub command
def _update (args):
    qry = "SELECT * FROM item WHERE item_id = '{}'"
    cur.execute(qry.format(args.id))
    item = cur.fetchone()
    if item == None:
        print 'Item with id of ' + args.id + ' does not exist'
        return
    if item[3] == 'Yes':
        print 'You cannot update an item that is currently lent out'
        return
    if args.name != '' and args.location != '':
        qry = "UPDATE item SET item_name = '{}', item_loc = '{}' WHERE item_id = '{}'"
        cur.execute(qry.format(args.name, args.location, args.id))
        conn.commit()
    elif args.name != '':
        qry = "UPDATE item SET item_name = '{}' WHERE item_id = '{}'"
        cur.execute(qry.format(args.name, args.id))
        conn.commit()
    elif args.location != '':
        qry = "UPDATE item SET item_loc = '{}' WHERE item_id = '{}'"
        cur.execute(qry.format(args.location, args.id))
        conn.commit()
    qry = "SELECT * FROM item WHERE item_id = '{}'"
    items = cur.execute(qry.format(args.id))
    print 'Item has been updated'
    print_items(items)

# Lend item sub command
def _lend (args):
    qry = "SELECT * FROM item WHERE item_id = '{}'"
    items = cur.execute(qry.format(args.id))
    item = cur.fetchone()
    if item == None:
        print 'Item with id of ' + args.id + ' does not exist'
        return
    if item[3] == 'Yes':
        print 'You cannot lend an item that is currently lent out'
        return
    qry = "UPDATE item SET item_lent = '{}', person_name = '{}', person_info = '{}' WHERE item_id = '{}'"
    cur.execute(qry.format('Yes', args.name, args.info, args.id))
    conn.commit()
    qry = "INSERT INTO log (type, item_name, item_loc, person_name, person_info) VALUES ('{}', '{}', '{}', '{}', '{}')"
    cur.execute(qry.format('Lend', item[1], item[2], args.name, args.info))
    conn.commit()
    qry = "SELECT * FROM item WHERE item_id = '{}'"
    items = cur.execute(qry.format(args.id))
    print 'Item has been lent'
    print_items(items)

# Return item sub command
def _return (args):
    qry = "SELECT * FROM item WHERE item_id = '{}'"
    items = cur.execute(qry.format(args.id))
    item = cur.fetchone()
    if item == None:
        print 'Item with id of ' + args.id + ' does not exist'
        return
    if item[3] == 'No':
        print 'You cannot return an item that is not currently lent out'
        return
    qry = "UPDATE item SET item_lent = '{}', person_name = '{}', person_info = '{}' WHERE item_id = '{}'"
    cur.execute(qry.format('No', '', '', args.id))
    conn.commit()
    qry = "INSERT INTO log (type, item_name, item_loc, person_name, person_info) VALUES ('{}', '{}', '{}', '{}', '{}')"
    cur.execute(qry.format('Return', item[1], item[2], item[4], item[5]))
    conn.commit()
    qry = "SELECT * FROM item WHERE item_id = '{}'"
    items = cur.execute(qry.format(args.id))
    print 'Item has been returned'
    print_items(items)

# Search logs sub command
def _log (args):
    qry = "SELECT * FROM log WHERE UPPER(type) LIKE UPPER('%{}%') AND UPPER(item_name) LIKE UPPER('%{}%') AND UPPER(item_loc) LIKE UPPER('%{}%') AND UPPER(person_name) LIKE UPPER('%{}%') AND UPPER(person_info) LIKE UPPER('%{}%')"
    logs = cur.execute(qry.format(args.type, args.item_name, args.item_location, args.person_name, args.person_info))
    print_logs(logs)

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
if args.action is 'find':
    _find(args)
elif args.action is 'add':
    _add(args)
elif args.action is 'remove':
    _remove(args)
elif args.action is 'update':
    _update(args)
elif args.action is 'lend':
    _lend(args)
elif args.action is 'return':
    _return(args)
elif args.action is 'log':
    _log(args)
