## Synopsis

This is a small project that handles item management, item lending, and transaction logging. It is meant to be used as a quick and painless alternative to a CD tower / software setup, so as to remove the stress of hardware and software failures that I have certainly run into before.

## Code Example

```
# python loaner.py -h

usage: loaner.py [-h] {find,add,remove,update,lend,return,log} ...

positional arguments:
  {find,add,remove,update,lend,return,log}
    find                find an item
    add                 add a new item
    remove              remove an item, item must not be currently lent out
    update              update an item, item must not be currently lent out
    lend                lend an item, item must not be currently lent out
    return              return an item, item must be currently lent out
    log                 find a transaction log

optional arguments:
  -h, --help            show this help message and exit
```

```
# python loaner.py add "Windows 10 x86_64" "Tower 1/1"

Item has been added
+----+-------------------+---------------+-------+-------------+-------------+
| ID |     Item Name     | Item Location |  Lent | Person Name | Person Info |
+----+-------------------+---------------+-------+-------------+-------------+
| 2  | Windows 10 x86_64 |   Tower 1/1   | False |             |             |
+----+-------------------+---------------+-------+-------------+-------------+
```

```
# python loaner.py find

+----+-------------------+---------------+-------+----------------+--------------+
| ID |     Item Name     | Item Location |  Lent |  Person Name   | Person Info  |
+----+-------------------+---------------+-------+----------------+--------------+
| 1  | Windows 10 x86_64 |   Tower 1/1   | False |                |              |
| 2  |      Mac OSx      |   Tower 1/2   | False |                |              |
| 3  |       CentOS      |   Tower 1/3   |  True | Gordon Freeman | 123-456-7890 |
| 4  |       Fedora      |   Tower 1/4   | False |                |              |
| 5  |      Solaris      |   Tower 1/5   | False |                |              |
| 6  |       Ubuntu      |   Tower 1/6   | False |                |              |
| 7  |   A Bag of Chips  |   Tower 1/7   |  True |   My Stomach   | 123-456-7890 |
+----+-------------------+---------------+-------+----------------+--------------+
```

```
# python loaner.py log

+--------+----------------+---------------+------------------+--------------+----------------------------+
|  Type  |   Item Name    | Item Location |   Person Name    | Person Info  |         Time Stamp         |
+--------+----------------+---------------+------------------+--------------+----------------------------+
|  Lend  |     CentOS     |   Tower 1/3   |  Gordon Freeman  | 123-456-7890 | 2016-04-14 01:04:20.864000 |
|  Lend  |    Solaris     |   Tower 1/5   | Hopefully Nobody | 123-456-7890 | 2016-04-14 01:04:59.455000 |
| Return |    Solaris     |   Tower 1/5   | Hopefully Nobody | 123-456-7890 | 2016-04-14 01:05:04.812000 |
|  Lend  | A Bag of Chips |   Tower 1/7   |    My Stomach    | 123-456-7890 | 2016-04-14 01:05:34.063000 |
+--------+----------------+---------------+------------------+--------------+----------------------------+
```



## Motivation

I was tasked with finding or developing an item management and lending system where I work, and eventually gave up on finding an existing project as none showed up and started developing my own. I am developing this in my free time as it doesn't entirely suit the purposes for what my work requires, but it does appeal to myself and hopefully other system administrators like myself.

## Installation

This project requires these python dependencies

* sqlalchemy
* pysqlite
* prettytable

You can install them yourself, or you can install them using pip and my requirements.txt file

`pip install -r requirements.txt`

## Contributors

[Zachariah T. Dzielinski](https://github.com/UnmercifulTurtle)
[Lenny Morayniss](https://github.com/ldmoray)

## License

The MIT License (MIT)
