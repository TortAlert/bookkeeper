from PySide6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QLabel, QPushButton, QDialog,
                               QLineEdit, QComboBox, QTableWidget, QTableWidgetItem, QHBoxLayout,
                               QHeaderView, QDialogButtonBox)

#Диалоговое окно для предупреждения пользователя о правильном удалении из таблиц
class WrongRowDialog(QDialog):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Удар по рукам пользователя!")

        QBtn = QDialogButtonBox.StandardButton.Ok

        self.buttonBox = QDialogButtonBox(QBtn)
        self.buttonBox.accepted.connect(self.accept)

        self.layout = QVBoxLayout()
        message = QLabel("Введите номер строки, содержащейся в таблице!")
        self.layout.addWidget(message)
        self.layout.addWidget(self.buttonBox)
        self.setLayout(self.layout)

#Диалоговое окно с предупреждением пользователя о том, что у категорий должны быть разные имена
class WrongCatNameDialog(QDialog):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Удар по рукам пользователя!")

        QBtn = QDialogButtonBox.StandardButton.Ok

        self.buttonBox = QDialogButtonBox(QBtn)
        self.buttonBox.accepted.connect(self.accept)

        self.layout = QVBoxLayout()
        message = QLabel("Запрещено создавать одинаковые категории.")
        self.layout.addWidget(message)
        self.layout.addWidget(self.buttonBox)
        self.setLayout(self.layout)

#Дополнительное окно для работы с категориями
class CatWindow(QWidget):
    def __init__(self, db_table, ex_id_list, controller, category, db_cat_box, daily_expensed, weekly_expensed, monthly_expensed, budg_table):
        super().__init__()

        #Общая настройка и создание необюходимых объектов
        self.setFixedSize(600, 400)
        self.db_table = db_table
        self.ex_id_list = ex_id_list
        self.controller = controller
        self.category = category
        self.db_cat_box = db_cat_box
        self.layout = QVBoxLayout()
        self.daily_expensed = daily_expensed
        self.weekly_expensed = weekly_expensed
        self.monthly_expensed = monthly_expensed
        self.budg_table = budg_table

        #Слой с таблицей категорий
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
        self.upd_button = QPushButton('Внести изменения')
        self.upd_button.clicked.connect(self.on_upd_button_click)
        self.t_layout.addWidget(self.upd_button)

        #Слой с созданием новой категории
        self.l_layout = QHBoxLayout()
        self.new_cat_line = QLabel('Новая категория:')
        self.l_layout.addWidget(self.new_cat_line)
        self.new_cat = QLineEdit()
        self.l_layout.addWidget(self.new_cat)
        self.new_button = QPushButton('Создать категорию')
        self.new_button.clicked.connect(self.on_new_button_click)
        self.l_layout.addWidget(self.new_button)

        #Слой с удалением категории
        self.del_layout = QHBoxLayout()
        self.del_layout.addWidget(QLabel('Номер строки:'))
        self.del_line = QLineEdit()
        self.del_layout.addWidget(self.del_line)
        self.del_button = QPushButton('Удалить категорию')
        self.del_layout.addWidget(self.del_button)
        self.del_button.clicked.connect(self.del_button_click)

        #Соединение слоев
        self.layout.addLayout(self.t_layout)
        self.layout.addLayout(self.l_layout)
        self.layout.addLayout(self.del_layout)
        self.setLayout(self.layout)

    #Функционал кнопки удалоения категории
    def del_button_click(self):
        row_number = int(self.del_line.text())
        if (row_number-1 > self.cat_table.rowCount()):
            dlg = WrongRowDialog()
            dlg.exec()
        else:
            cats_id = self.controller.read('Category')[1]
            self.controller.delete('Category', {'id': cats_id[row_number - 1]})
            self.refresh_categories()

    #Обновление таблицы категорий
    def refresh_categories(self):
        cats = self.controller.read('Category')
        self.cat_table.setRowCount(len(cats[0]))
        for (i, c) in enumerate(cats[0]):
            item = QTableWidgetItem(str(c))
            self.cat_table.setItem(i, 0, item)

    #Функционал кнопки создания котегории
    def on_new_button_click(self):
        ex = self.controller.create('Category', {'name': str(self.new_cat.text())})
        if ex == Exception:
            dlg = WrongCatNameDialog()
            dlg.exec()
        self.refresh_categories()

    #Функционал кнопки обновления информации в таблице
    def on_upd_button_click(self):
        cats_id = self.controller.read('Category')[1]
        for i in range(self.cat_table.rowCount()):
            name_it = self.cat_table.takeItem(i, 0)
            name = name_it.text()
            ex = self.controller.update('Category', {'id': cats_id[i], 'name': name})
            if (ex == Exception):
                dlg = WrongCatNameDialog()
                dlg.exec()
                break
        self.refresh_categories()

    #Обновление таблиц из основного окна
    def refresh_expenses(self):
        exp = self.controller.read('Expense')[0]
        cats = self.controller.read('Category')

        day_summ = self.controller.read('Expense')[1]
        self.daily_expensed = QTableWidgetItem(str(day_summ))
        self.budg_table.setItem(0, 0, self.daily_expensed)
        week_summ = self.controller.read('Expense')[2]
        self.weekly_expensed = QTableWidgetItem(str(week_summ))
        self.budg_table.setItem(1, 0, self.weekly_expensed)
        month_summ = self.controller.read('Expense')[3]
        self.monthly_expensed = QTableWidgetItem(str(month_summ))
        self.budg_table.setItem(2, 0, self.monthly_expensed)

        self.db_cat_box.clear()
        self.db_table.setRowCount(len(exp))
        self.ex_id_list.clear()
        index = 0
        for i in exp:
            self.ex_id_list.append(i[0])
            amount_it = QTableWidgetItem(str(i[2]))
            time_it = QTableWidgetItem(str(i[4]))
            com_it = QTableWidgetItem(str(i[5]))
            self.db_table.setItem(index, 0, time_it)
            self.db_table.setItem(index, 1, amount_it)
            self.db_cat_box.append(QComboBox(self))
            self.db_cat_box[index].clear()
            self.db_cat_box[index].addItems(cats[0])
            self.db_cat_box[index].setCurrentText(str(i[1]))
            self.db_table.setCellWidget(index, 2, self.db_cat_box[index])
            self.db_table.setItem(index, 3, com_it)
            index = index + 1

    #Необходимые приготовления
    def closeEvent(self, event):
        cats = self.controller.read('Category')
        self.category.clear()
        self.category.addItems(cats[0])
        self.refresh_expenses()
        event.accept()

#Основное окно проекта
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        #Основные переменные
        self.dialog = None
        self.controller = None
        self.ex_id_list = []
        self.db_cat_box = []
        self.setWindowTitle("Программа для ведения бюджета")
        self.setFixedSize(800, 600)

        #Слой с таблицей трат
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

        #Слой с таблицей общего бюджета и кнопкой его подтверждения
        self.layout2 = QVBoxLayout()
        self.budget = QLabel('Бюджет:')
        self.layout2.addWidget(self.budget)
        self.budg_table = QTableWidget()
        self.budg_table.setRowCount(3)
        self.budg_table.setColumnCount(2)
        self.budg_table.setHorizontalHeaderLabels(['Потрачено', 'Бюджет'])
        self.budg_table.setVerticalHeaderLabels(['День', 'Неделя', 'Месяц'])
        self.H_header = self.budg_table.horizontalHeader()
        self.H_header.setSectionResizeMode(0, QHeaderView.ResizeMode.Stretch)
        self.H_header.setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch)
        self.daily_expensed = QTableWidgetItem()
        self.budg_table.setItem(0, 0, self.daily_expensed)
        self.edit_budget_daily = QTableWidgetItem()
        self.budg_table.setItem(0, 1, self.edit_budget_daily)
        self.weekly_expensed = QTableWidgetItem()
        self.budg_table.setItem(1, 0, self.weekly_expensed)
        self.edit_budget_weekly = QTableWidgetItem()
        self.budg_table.setItem(1, 1, self.edit_budget_weekly)
        self.monthly_expensed = QTableWidgetItem()
        self.budg_table.setItem(2, 0, self.monthly_expensed)
        self.edit_budget_monthly = QTableWidgetItem()
        self.budg_table.setItem(2, 1, self.edit_budget_monthly)
        self.layout2.addWidget(self.budg_table)
        self.budget_button = QPushButton('Задать бюджет')
        self.layout2.addWidget(self.budget_button)
        self.budget_button.clicked.connect(self.on_budget_button_click)

        #Слой с заданием суммы покупки
        self.layout3 = QHBoxLayout()
        self.layout3.addWidget(QLabel('Сумма:'))
        self.amount_line = QLineEdit()
        self.layout3.addWidget(self.amount_line)

        #Слой для работы с категориями
        self.layout4 = QHBoxLayout()
        self.category = QComboBox(self)
        self.layout4.addWidget(QLabel('Категория:'))
        self.layout4.addWidget(self.category)
        self.category_button = QPushButton('Редактировать')
        self.layout4.addWidget(self.category_button)
        self.category_button.clicked.connect(self.on_category_button_click)

        #Слой с кнопками создания категории и кнопкой подтверждения изменения в таблице трат
        self.layout5 = QVBoxLayout()
        self.add_exp_button = QPushButton('Добавить')
        self.layout5.addWidget(self.add_exp_button)
        self.add_exp_button.clicked.connect(self.add_exp_button_click)
        self.upd_exp_button = QPushButton('Внести изменения в траты')
        self.layout5.addWidget(self.upd_exp_button)
        self.upd_exp_button.clicked.connect(self.upd_exp_button_click)

        #Слой с удалением покупок
        self.layout6 = QHBoxLayout()
        self.layout6.addWidget(QLabel('Номер строки:'))
        self.row_num_line = QLineEdit()
        self.layout6.addWidget(self.row_num_line)
        self.del_exp_button = QPushButton('Удалить покупку')
        self.layout6.addWidget(self.del_exp_button)
        self.del_exp_button.clicked.connect(self.del_exp_button_click)

        #Соединение слоев
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

    #Установка контроллера
    def set_controller(self, controller):
        self.controller = controller

    #Обновление заданного бюджета
    def refresh_budgets(self):
        bdgt = self.controller.read('Budget')
        self.edit_budget_daily = QTableWidgetItem(str(bdgt[2]))
        self.budg_table.setItem(0, 1, self.edit_budget_daily)
        self.edit_budget_weekly = QTableWidgetItem(str(bdgt[1]))
        self.budg_table.setItem(1, 1, self.edit_budget_weekly)
        self.edit_budget_monthly = QTableWidgetItem(str(bdgt[0]))
        self.budg_table.setItem(2, 1, self.edit_budget_monthly)

    #Функционал кнопки подтверждения обновления бюджета
    def on_budget_button_click(self):
        self.controller.update('Budget', {'monthly': float(self.edit_budget_monthly.text()),
                                          'weekly': float(self.edit_budget_weekly.text()),
                                          'daily': float(self.edit_budget_daily.text())})
        self.refresh_budgets()

    #Обновление категорий
    def refresh_categories(self):
        cats = self.controller.read('Category')
        self.category.clear()
        self.category.addItems(cats[0])

    #Функционал кнопки редактирования категорий
    def on_category_button_click(self):
        self.dialog = CatWindow(self.db_table, self.ex_id_list, self.controller, self.category, self.db_cat_box,
                                self.daily_expensed, self.weekly_expensed, self.monthly_expensed, self.budg_table)
        self.dialog.refresh_categories()
        self.dialog.show()

    #Обновление таблицы трат и суммы трат в таблице бюджета
    def refresh_expenses(self):
        exp = self.controller.read('Expense')[0]
        day_summ = self.controller.read('Expense')[1]
        self.daily_expensed = QTableWidgetItem(str(day_summ))
        self.budg_table.setItem(0, 0, self.daily_expensed)
        week_summ = self.controller.read('Expense')[2]
        self.weekly_expensed = QTableWidgetItem(str(week_summ))
        self.budg_table.setItem(1, 0, self.weekly_expensed)
        month_summ = self.controller.read('Expense')[3]
        self.monthly_expensed = QTableWidgetItem(str(month_summ))
        self.budg_table.setItem(2, 0, self.monthly_expensed)
        cats = self.controller.read('Category')
        self.db_cat_box.clear()
        self.db_table.setRowCount(len(exp))
        self.ex_id_list.clear()
        index = 0
        for i in exp:
            self.ex_id_list.append(i[0])
            amount_it = QTableWidgetItem(str(i[2]))
            time_it = QTableWidgetItem(str(i[4]))
            com_it = QTableWidgetItem(str(i[5]))
            self.db_table.setItem(index, 0, time_it)
            self.db_table.setItem(index, 1, amount_it)
            self.db_cat_box.append(QComboBox(self))
            self.db_cat_box[index].clear()
            self.db_cat_box[index].addItems(cats[0])
            self.db_cat_box[index].setCurrentText(str(i[1]))
            self.db_table.setCellWidget(index, 2, self.db_cat_box[index])
            self.db_table.setItem(index, 3, com_it)
            index = index + 1

    #Функционал кнопки добавления покупки
    def add_exp_button_click(self):
        self.controller.create('Expense', {'amount': float(self.amount_line.text()),
                                           'category': self.category.currentText()})
        self.refresh_expenses()

    #Функционал кнопки подтверждения изменений в покупки
    def upd_exp_button_click(self):
        for i in range(self.db_table.rowCount()):
            time_it = self.db_table.takeItem(i, 0)
            time = time_it.text()
            amount_it = self.db_table.takeItem(i, 1)
            amount = float(amount_it.text())
            cat = self.db_cat_box[i].currentText()
            com_it = self.db_table.takeItem(i, 3)
            com = com_it.text()
            self.controller.update('Expense', {'id': self.ex_id_list[i],
                                               'date': time,
                                               'amount': float(amount),
                                               'category': cat,
                                               'comment': com})
        self.refresh_expenses()

    #Функционал кнопки удаления покупки
    def del_exp_button_click(self):
        row_number = int(self.row_num_line.text())
        if (row_number-1 >= self.db_table.rowCount()) or (row_number-1 < 0):
            dlg = WrongRowDialog()
            dlg.exec()
        else:
            self.controller.delete('Expense', {'id': self.ex_id_list[row_number-1]})
            self.refresh_expenses()