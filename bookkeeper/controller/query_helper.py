from pony.orm import *
from bookkeeper.models.entities import Budget, Category, Expense
import datetime

@db_session
def add_budget(monthly, weekly, daily):
    try:
        Budget(monthly=monthly, weekly=weekly, daily=daily)
    except Exception as e:
        print(e)

@db_session
def get_budget():
    try:
        q = select(b for b in Budget).order_by(lambda: desc(b.id)).limit(1)
        budget = q.to_list()[0]
        return tuple([budget.monthly, budget.weekly, budget.daily])
    except Exception as e:
        print(e)

@db_session
def add_category(name):
    try:
        q = select((c) for c in Category if c.name == name)
        if len(q) == 0:
            Category(name=name)
        else:
            return Exception
    except Exception as e:
        print(e)

@db_session
def get_category():
    try:
        q = select((c.name) for c in Category)
        i = select((c.id) for c in Category)
        cats = list(q)
        id = list(i)
        return [cats, id]
    except Exception as e:
        print(e)

@db_session
def upd_category(id, name):
    try:
        cat = Category[id]
        q = select((c) for c in Category if c.name == name)
        if (len(q) == 0) or (cat.name == name):
            cat.name = name
        else:
            return Exception
    except Exception as e:
        print(e)

@db_session
def del_category(id):
    try:
        delete(e for e in Expense if e.category.id == id)
        Category[id].delete()
    except Exception as e:
        print(e)

@db_session
def add_expense(amount, category, expense_date=datetime.date.today(), added_date=datetime.date.today(), comment=''):
    try:
        q = select((c.id) for c in Category if c.name == category)
        Expense(amount=amount, expense_date=expense_date, added_date=added_date, category=list(q)[0], comment=comment)
    except Exception as e:
        print(e)

@db_session
def get_expense():
    try:
        q = select((ex.id, ex.category.name, ex.amount, ex.expense_date, ex.added_date, ex.comment) for ex in Expense)
        exs = list(q)
        day_summ = sum(ex.amount for ex in Expense if ex.added_date == datetime.date.today())
        month_summ = sum(ex.amount for ex in Expense if (ex.added_date.month == datetime.date.today().month and ex.added_date.year == datetime.date.today().year))
        week_summ = 0
        for e in exs:
            if e[4].isocalendar()[1] == datetime.date.today().isocalendar()[1]:
                week_summ = week_summ + e[2]
        return exs, day_summ, week_summ, month_summ
    except Exception as e:
        print(e)

@db_session
def upd_expense(id, added_date, amount, category, comment):
    try:
        ex = Expense[id]
        ex.amount = float(amount)
        date = added_date.split('-')
        ex.added_date = datetime.date(int(date[0]), int(date[1]), int(date[2]))
        q = select((c.id) for c in Category if c.name == category)
        ex.category = int(list(q)[0])
        ex.comment = comment
    except Exception as e:
        print(e)

@db_session
def del_expense(id):
    try:
        Expense[id].delete()
    except Exception as e:
        print(e)
