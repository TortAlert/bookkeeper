from bookkeeper.models.entities import db
import bookkeeper.controller.query_helper as qh


class CrudController:
    def __init__(self):
        try:
            db.bind(provider='sqlite', filename='../database.sqlite', create_db=True)  # TODO: Move DB file name to config / dotenv
            db.generate_mapping(create_tables=True)
        except Exception as e:
            print(e)

    def create(self, entity, params):
        if entity == 'Budget':
            qh.add_budget(monthly=params['monthly'], weekly=params['weekly'],
                          daily=params['daily'])
            return

        if entity == 'Category':
            ex = qh.add_category(name=params['name'])
            return ex

        if entity == 'Expense':
            qh.add_expense(amount=params['amount'], category=params['category'])
            return
        raise NotImplementedError(f'Добавление для сущности {entity} не реализовано!')

    def read(self, entity, params=None):
        if entity == 'Budget':
            return qh.get_budget()
        if entity == 'Category':
            return qh.get_category()
        if entity == 'Expense':
            return qh.get_expense()
        raise NotImplementedError(f'Чтение для сущности {entity} не реализовано!')

    def update(self, entity, params):
        if entity == 'Budget':  # For Budget, update is the same as create
            qh.add_budget(monthly=params['monthly'], weekly=params['weekly'],
                          daily=params['daily'])
            return
        if entity == 'Category':
            ex = qh.upd_category(id=params['id'], name=params['name'])
            return ex
        if entity == 'Expense':
            qh.upd_expense(id=params['id'], added_date=params['date'], amount=params['amount'], category=params['category'], comment=params['comment'])
            return
        raise NotImplementedError(f'Изменение для сущности {entity} не реализовано!')

    def delete(self, entity, params):
        if entity == 'Expense':
            qh.del_expense(id=params['id'])
            return
        if entity == 'Category':
            qh.del_category(id=params['id'])
            return
        raise NotImplementedError(f'Удаление для сущности {entity} не реализовано!')