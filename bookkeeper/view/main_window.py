from PySide6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QLabel, QPushButton,
                               QLineEdit, QComboBox, QTableWidget, QTableWidgetItem)

from PySide6 import QtCore

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.controller = None
        self.setWindowTitle("Программа для ведения бюджета")
        self.setFixedSize(800, 600)

        self.layout = QVBoxLayout()

        self.budget = QLabel('Бюджет:')
        self.layout.addWidget(self.budget)
        self.table = QTableWidget()
        self.table.setRowCount(3)
        self.table.setColumnCount(2)
        self.table.setHorizontalHeaderLabels(['Потрачено', 'Бюджет'])
        self.table.setVerticalHeaderLabels(['День', 'Неделя', 'Месяц'])
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
        self.layout.addWidget(self.table)


        self.budget_button = QPushButton('Задать бюджет')
        self.layout.addWidget(self.budget_button)
        self.budget_button.clicked.connect(self.on_budget_button_click)

        self.category = QComboBox(self)
        self.layout.addWidget(QLabel('Выберите категорию расхода:'))
        self.layout.addWidget(self.category)

        self.widget = QWidget()
        self.widget.setLayout(self.layout)

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
        self.category.addItems(cats)
