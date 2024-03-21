from datetime import date
from pony.orm import *


db = Database()


class Expense(db.Entity):
    id = PrimaryKey(int, auto=True)
    amount = Required(float)
    expense_date = Required(date)
    added_date = Required(date)
    comment = Optional(str)
    category = Required('Category')


class Category(db.Entity):
    id = PrimaryKey(int, auto=True)
    expenses = Set(Expense)
    name = Required(str)
    #parent = Optional('Category', reverse='parent')


class Budget(db.Entity):
    id = PrimaryKey(int, auto=True)
    monthly = Required(float, default=50000)
    weekly = Required(float, default=10000)
    daily = Required(float, default=1200)

