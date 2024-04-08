from controller.crud_controller import CrudController
from view.main_window import MainWindow
from PySide6.QtWidgets import QApplication

class App(QApplication):
    def __init__(self):
        super().__init__()
        self.view = MainWindow()
        self.controller = CrudController()
        self.view.set_controller(self.controller)
        if (self.controller.read('Budget') == None):
            self.controller.create('Budget', {'monthly': 10000, 'weekly': 1000, 'daily': 100})
        self.controller.read('Expense')
        self.view.refresh_budgets()
        self.view.refresh_categories()
        self.view.refresh_expenses()
        self.view.show()


if __name__ == "__main__":
    app = App()
    app.exec()