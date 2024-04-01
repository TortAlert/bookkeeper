from PySide6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QLabel, QPushButton, QDialog,
                               QLineEdit, QComboBox, QTableWidget, QTableWidgetItem, QHBoxLayout, QHeaderView)

from PySide6 import QtCore

class CatWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.setFixedSize(400, 200)
        self.controller = None
        self.cat_box = None
        self.layout = QVBoxLayout()
        self.t_layout = QVBoxLayout()
        self.table_name = QLabel('Список категорий')
        self.t_layout.addWidget(self.table_name)

        self.cat_table = QTableWidget()
        self.cat_table.setRowCount(0)
        self.cat_table.setColumnCount(1)
        self.cat_table.setHorizontalHeaderLabels(['Название'])
        self.H_header = self.cat_table.horizontalHeader()
        self.H_header.setSectionResizeMode(0, QHeaderView.ResizeMode.Stretch)
        self.cat_table.resize(self.cat_table.sizeHint())
        self.t_layout.addWidget(self.cat_table)


        self.l_layout = QHBoxLayout()
        self.line_name = QLabel('Новая категория:')
        self.l_layout.addWidget(self.line_name)
        self.new_cat = QLineEdit()
        self.l_layout.addWidget(self.new_cat)
        self.new_button = QPushButton('Создать категорию')
        self.new_button.clicked.connect(self.on_new_button_click)
        self.l_layout.addWidget(self.new_button)

        self.layout.addLayout(self.t_layout)
        self.layout.addLayout(self.l_layout)
        self.setLayout(self.layout)

    def refresh_categories(self):
        cats = self.controller.read('Category')
        self.cat_table.setRowCount(len(cats))
        for (i, c) in enumerate(cats):
            item = QTableWidgetItem(str(c))
            self.cat_table.setItem(i, 0, item)


    def on_new_button_click(self):
        self.controller.create('Category', {'name': str(self.new_cat.text())})
        self.refresh_categories()

    def set_controller(self, controller):
        self.controller = controller

    def give_cat_box(self, cat_box):
        self.cat_box = cat_box

    def closeEvent(self, event):
        cats = self.controller.read('Category')
        self.cat_box.clear()
        self.cat_box.addItems(cats)
        event.accept()

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.dialog = None
        self.controller = None
        self.setWindowTitle("Программа для ведения бюджета")
        self.setFixedSize(800, 600)

        self.layout1 = QVBoxLayout()
        self.db_name = QLabel('Траты:')
        self.layout1.addWidget(self.db_name)
        self.db_table = QTableWidget()
        self.db_table.setColumnCount(4)
        self.db_table.setHorizontalHeaderLabels(['Дата', 'Сумма', 'Категория', 'Комментарий'])
        self.dbH_header = self.db_table.horizontalHeader()
        self.dbH_header.setSectionResizeMode(0, QHeaderView.ResizeMode.ResizeToContents)
        self.dbH_header.setSectionResizeMode(1, QHeaderView.ResizeMode.ResizeToContents)
        self.dbH_header.setSectionResizeMode(2, QHeaderView.ResizeMode.ResizeToContents)
        self.dbH_header.setSectionResizeMode(3, QHeaderView.ResizeMode.Stretch)
        self.db_table.setRowCount(0)
        self.db_table.resize(self.db_table.sizeHint())
        self.layout1.addWidget(self.db_table)

        self.layout2 = QVBoxLayout()
        self.budget = QLabel('Бюджет:')
        self.layout2.addWidget(self.budget)
        self.table = QTableWidget()
        self.table.setRowCount(3)
        self.table.setColumnCount(2)
        self.table.setHorizontalHeaderLabels(['Потрачено', 'Бюджет'])
        self.table.setVerticalHeaderLabels(['День', 'Неделя', 'Месяц'])
        self.H_header = self.table.horizontalHeader()
        self.H_header.setSectionResizeMode(0, QHeaderView.ResizeMode.Stretch)
        self.H_header.setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch)
        #self.V_header = self.table.verticalHeader()
        #self.V_header.setSectionResizeMode(0, QHeaderView.ResizeMode.ResizeToContents)
        #self.V_header.setSectionResizeMode(1, QHeaderView.ResizeMode.ResizeToContents)
        #self.V_header.setSectionResizeMode(2, QHeaderView.ResizeMode.ResizeToContents)
        self.daily_expensed = QTableWidgetItem()
        self.table.setItem(0, 0, self.daily_expensed)
        self.edit_budget_daily = QTableWidgetItem()
        self.table.setItem(0, 1, self.edit_budget_daily)
        self.weekly_expensed = QTableWidgetItem()
        self.table.setItem(1, 0, self.weekly_expensed)
        self.edit_budget_weekly = QTableWidgetItem()
        self.table.setItem(1, 1, self.edit_budget_weekly)
        self.monthly_expensed = QTableWidgetItem()
        self.table.setItem(2, 0, self.monthly_expensed)
        self.edit_budget_monthly = QTableWidgetItem()
        self.table.setItem(2, 1, self.edit_budget_monthly)
        self.table.resize(self.table.sizeHint())
        self.layout2.addWidget(self.table)

        self.layout3 = QVBoxLayout()
        self.budget_button = QPushButton('Задать бюджет')
        self.layout3.addWidget(self.budget_button)
        self.budget_button.clicked.connect(self.on_budget_button_click)

        self.layout4 = QHBoxLayout()
        self.layout4.addWidget(QLabel('Сумма:'))
        self.amount_line = QLineEdit()
        self.layout4.addWidget(self.amount_line)

        self.layout5 = QHBoxLayout()
        self.category = QComboBox(self)
        self.layout5.addWidget(QLabel('Категория:'))
        self.layout5.addWidget(self.category)
        self.category_button = QPushButton('Редактировать')
        self.layout5.addWidget(self.category_button)
        self.category_button.clicked.connect(self.on_category_button_click)

        self.layout6 = QVBoxLayout()
        self.add_exp_button = QPushButton('Добавить')
        self.layout6.addWidget(self.add_exp_button)
        self.add_exp_button.clicked.connect(self.add_exp_button_click)
        self.upd_exp_button = QPushButton('Внести изменения в траты')
        self.layout6.addWidget(self.upd_exp_button)
        self.upd_exp_button.clicked.connect(self.upd_exp_button_click)

        self.megalayout = QVBoxLayout()
        self.megalayout.addLayout(self.layout1)
        self.megalayout.addLayout(self.layout2)
        self.megalayout.addLayout(self.layout3)
        self.megalayout.addLayout(self.layout4)
        self.megalayout.addLayout(self.layout5)
        self.megalayout.addLayout(self.layout6)

        self.widget = QWidget()
        self.widget.setLayout(self.megalayout)

        self.setCentralWidget(self.widget)

    def set_controller(self, controller):
        self.controller = controller

    def refresh_budgets(self):
        bdgt = self.controller.read('Budget')
        self.edit_budget_daily = QTableWidgetItem(str(bdgt[2]))
        self.table.setItem(0, 1, self.edit_budget_daily)
        self.edit_budget_weekly = QTableWidgetItem(str(bdgt[1]))
        self.table.setItem(1, 1, self.edit_budget_weekly)
        self.edit_budget_monthly = QTableWidgetItem(str(bdgt[0]))
        self.table.setItem(2, 1, self.edit_budget_monthly)


    def on_budget_button_click(self):
        self.controller.update('Budget', {'monthly': float(self.edit_budget_monthly.text()),
                                          'weekly': float(self.edit_budget_weekly.text()),
                                          'daily': float(self.edit_budget_daily.text())})
        self.refresh_budgets()

    def refresh_categories(self):
        cats = self.controller.read('Category')
        self.category.clear()
        self.category.addItems(cats)

    def on_category_button_click(self):
        self.dialog = CatWindow()
        self.dialog.set_controller(self.controller)
        self.dialog.give_cat_box(self.category)
        self.dialog.refresh_categories()
        self.dialog.show()

    def refresh_expenses(self):
        exp = self.controller.read('Expense')
        self.db_table.setRowCount(len(exp))
        index = 0
        for i in exp:
            print('i= ', i)
            cat_it = QTableWidgetItem(str(i[0]))
            amount_it = QTableWidgetItem(str(i[1]))
            time_it = QTableWidgetItem(str(i[3]))
            com_it = QTableWidgetItem(str(i[4]))
            self.db_table.setItem(index, 0, time_it)
            self.db_table.setItem(index, 1, amount_it)
            self.db_table.setItem(index, 2, cat_it)
            self.db_table.setItem(index, 3, com_it)
            index = index + 1

    def add_exp_button_click(self):
        self.controller.create('Expense', {'amount': float(self.amount_line.text()),
                                           'category': self.category.currentText()})
        self.refresh_expenses()

    def upd_exp_button_click(self):
        #for i in range(self.db_table.rowCount()):

        print('aboba')