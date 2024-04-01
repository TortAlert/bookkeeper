from pony.orm import *
from bookkeeper.models.entities import Budget, Category, Expense
import datetime

@db_session
def add_budget(monthly, weekly, daily):
    try:
        Budget(monthly=monthly, weekly=weekly, daily=daily)
    except Exception as e:
        print(e)  # TODO: This should be sent to GUI in a user-friendly manner


@db_session
def get_budget():
    try:
        q = select(b for b in Budget).order_by(lambda: desc(b.id)).limit(1)
        budget = q.to_list()[0]
        return tuple([budget.monthly, budget.weekly, budget.daily])  # TODO: return the object itself for GUI?
    except Exception as e:
        print(e)  # TODO: This should be sent to GUI in a user-friendly manner

@db_session
def add_category(name):
    try:
        q = select((c) for c in Category if c.name == name)
        if len(q) == 0:
            Category(name=name)
        else:
            print("You can't add same categories")
    except Exception as e:
        print(e)


@db_session
def get_category():
    try:
        q = select((c.name) for c in Category)
        cats = list(q)
        print('Cats in get_cat:', cats)
        return cats
        #return tuple("".join(cat) for cat in cats)
    except Exception as e:
        print(e)

@db_session
def add_expense(amount, category, expense_date=datetime.date.today(), added_date=datetime.date.today(), comment=''):
    try:
        q = select((c.id) for c in Category if c.name == category)
        print("Q is: ", list(q), "len(Q) = ", len(q))
        Expense(amount=amount, expense_date=expense_date, added_date=added_date, category=list(q)[0], comment=comment)
    except Exception as e:
        print(e)

@db_session
def get_expense():
    try:
        q = select((ex.category.name, ex.amount, ex.expense_date, ex.added_date, ex.comment) for ex in Expense)
        exs = list(q)
        print(exs[0][0])
        return exs
        #return tuple(" > ".join(expense) for expense in exs)
    except Exception as e:
        print(e)
