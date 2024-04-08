from bookkeeper.controller.crud_controller import CrudController
import datetime
import pytest

@pytest.fixture
def controller():
    return CrudController()


def test_add_and_read_budget(controller):
    controller.create('Budget', {'monthly': 100_000,
                               'weekly': 25_000,
                               'daily': 4_000})
    budget = controller.read('Budget')
    assert budget == (100000.0, 25000.0, 4000.0)

def test_add_and_read_expense(controller):
    controller.create('Category', {'name': 'name'})
    controller.create('Expense', {'amount': 100, 'category': 'name'})
    exp = controller.read('Expense')[0]
    assert exp[0][1] == 'name'
    assert exp[0][2] == 100

def test_upd_expense(controller):
    controller.create('Category', {'name': 'name1'})
    controller.create('Category', {'name': 'name2'})
    controller.create('Expense', {'amount': 100, 'category': 'name1'})
    exp = controller.read('Expense')[0]
    controller.update('Extity', {'id': exp[0],
                                            'date': datetime.date(2022, 1, 1),
                                            'amount': 1000,
                                            'category': 'name2',
                                            'comment': 'Hello'})
    exp = controller.read('Expense')[0]
    assert exp[0][1] == 'name2'
    assert exp[0][2] == 1000
    assert exp[0][4] == datetime.date(2022, 1, 1)
    assert exp[0][5] == 'Hello'
