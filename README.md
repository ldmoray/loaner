## Synopsis

This is a small project that handles item management, item lending, and transaction logging. It is meant to be used as a quick and painless alternative to a CD tower / software setup, so as to remove the stress of hardware and software failures that I have certainly run into before.

## Code Example

Show what the library does as concisely as possible, developers should be able to figure out **how** your project solves their problem by looking at the code example. Make sure the API you are showing off is obvious, and that your code is short and concise.

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
+----+-------------------+---------------+------+-------------+-------------+
| ID |     Item Name     | Item Location | Lent | Person Name | Person Info |
+----+-------------------+---------------+------+-------------+-------------+
| 8  | Windows 10 x86_64 |   Tower 1/1   |  No  |             |             |
+----+-------------------+---------------+------+-------------+-------------+
```

```
# python loaner.py find

+----+-------------------+---------------+------+----------------+--------------------+
| ID |     Item Name     | Item Location | Lent |  Person Name   |    Person Info     |
+----+-------------------+---------------+------+----------------+--------------------+
| 1  | Windows 10 x86_64 |   Tower 1/1   |  No  |                |                    |
| 2  |      Mac OSx      |   Tower 1/2   |  No  |                |                    |
| 3  |       CentOS      |   Tower 1/3   | Yes  | Gordon Freeman |    123-456-7890    |
| 4  |      FreeBSD      |   Tower 1/4   |  No  |                |                    |
| 5  |      Solaris      |   Tower 1/5   |  No  |                |                    |
| 6  |       Ubuntu      |   Tower 1/6   |  No  |                |                    |
| 7  |   A Bag of Chips  |   Tower 1/7   | Yes  |   Bill Gates   | bill@microsoft.com |
+----+-------------------+---------------+------+----------------+--------------------+
```

```
# python loaner.py log

+--------+-------------------+---------------+-------------------------+--------------------+---------------------+
|  Type  |     Item Name     | Item Location |       Person Name       |    Person Info     |      Time Stamp     |
+--------+-------------------+---------------+-------------------------+--------------------+---------------------+
|  Lend  | Windows 10 x86_64 |   Tower 1/1   | Zachariah T. Dzielinski |   (240) 818-4962   | 2016-04-09 01:36:15 |
| Return | Windows 10 x86_64 |   Tower 1/1   | Zachariah T. Dzielinski |   (240) 818-4962   | 2016-04-09 01:37:05 |
|  Lend  |       CentOS      |   Tower 1/3   |      Gordon Freeman     |    123-456-7890    | 2016-04-09 02:21:09 |
|  Lend  |   A Bag of Chips  |   Tower 1/7   |        Bill Gates       | bill@microsoft.com | 2016-04-09 02:22:16 |
|  Lend  |      Solaris      |   Tower 1/5   |     Hopefully Nobody    |    999-888-777     | 2016-04-09 02:22:48 |
|  Lend  |       Ubuntu      |   Tower 1/6   |       Matt Murdock      |    135-234-6342    | 2016-04-09 02:26:14 |
| Return |       Ubuntu      |   Tower 1/6   |       Matt Murdock      |    135-234-6342    | 2016-04-09 02:26:19 |
+--------+-------------------+---------------+-------------------------+--------------------+---------------------+
```



## Motivation

I was tasked with finding or developing an item management and lending system where I work, and eventually gave up on finding an existing project as none showed up and started developing my own. I am developing this in my free time as it doesn't entirely suit the purposes for what my work requires, but it does appeal to myself and hopefully other system administrators like myself.

## Installation

This project requires these python dependencies

* pysqlite
* prettytable

You can install them yourself, or you can install them using pip and my requirements.txt file

`pip install -r requirements.txt`

## Contributors

[Zachariah T. Dzielinski](https://github.com/UnmercifulTurtle)

## License

The MIT License (MIT)
