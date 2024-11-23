# import sys
# import sqlite3
# from PyQt6 import QtCore, QtGui, QtWidgets
# from PyQt5 import QtWidgets, QtCore
# import sys
# import sqlite3
# from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QPushButton, QLabel, QLineEdit, QMessageBox
# from PyQt6.QtCore import QCoreApplication
# import sys
# import sqlite3
#
#
# class Ui_MainWindow(object):
#     def __init__(self, ):
#         super().__init__()
#
#     def setupUi(self, MainWindow):
#         MainWindow.setObjectName("MainWindow")
#         MainWindow.resize(800, 600)
#         self.centralwidget = QtWidgets.QWidget(parent=MainWindow)
#         self.centralwidget.setObjectName("centralwidget")
#         self.verticalLayoutWidget = QtWidgets.QWidget(parent=self.centralwidget)
#         self.verticalLayoutWidget.setGeometry(QtCore.QRect(290, 160, 211, 181))
#         self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
#         self.verticalLayout = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
#         self.verticalLayout.setContentsMargins(0, 0, 0, 0)
#         self.verticalLayout.setObjectName("verticalLayout")
#         self.verticalLayout_2 = QtWidgets.QVBoxLayout()
#         self.verticalLayout_2.setObjectName("verticalLayout_2")
#         self.loginParent = QtWidgets.QLineEdit(parent=self.verticalLayoutWidget)
#         self.loginParent.setObjectName("loginParent")
#         self.verticalLayout_2.addWidget(self.loginParent)
#         self.passwordParent = QtWidgets.QLineEdit(parent=self.verticalLayoutWidget)
#         self.passwordParent.setObjectName("passwordParent")
#         self.passwordParent.setEchoMode(QtWidgets.QLineEdit.EchoMode.Password)  # Скрыть ввод пароля
#         self.verticalLayout_2.addWidget(self.passwordParent)
#         self.lineEdit_3 = QtWidgets.QLineEdit(parent=self.verticalLayoutWidget)
#         self.lineEdit_3.setObjectName("lineEdit_3")
#         self.lineEdit_3.setEchoMode(QtWidgets.QLineEdit.EchoMode.Password)  # Скрыть ввод подтверждения пароля
#         self.verticalLayout_2.addWidget(self.lineEdit_3)
#         self.verticalLayout_3 = QtWidgets.QVBoxLayout()
#         self.verticalLayout_3.setObjectName("verticalLayout_3")
#         self.registrParent = QtWidgets.QPushButton(parent=self.verticalLayoutWidget)
#         self.registrParent.setObjectName("registrParent")
#         self.registrParent.clicked.connect(self.add_user)  # Подключаем обработчик
#         self.verticalLayout_3.addWidget(self.registrParent)
#         self.vhodParent = QtWidgets.QPushButton(parent=self.verticalLayoutWidget)
#         self.vhodParent.setObjectName("vhodParent")
#         self.vhodParent.clicked.connect(self.open_login_window)  # Подключаем обработчик для кнопки "вход"
#         self.verticalLayout_3.addWidget(self.vhodParent)
#         self.verticalLayout_2.addLayout(self.verticalLayout_3)
#         self.verticalLayout.addLayout(self.verticalLayout_2)
#         MainWindow.setCentralWidget(self.centralwidget)
#         self.menubar = QtWidgets.QMenuBar(parent=MainWindow)
#         self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 26))
#         self.menubar.setObjectName("menubar")
#         MainWindow.setMenuBar(self.menubar)
#         self.statusbar = QtWidgets.QStatusBar(parent=MainWindow)
#         self.statusbar.setObjectName("statusbar")
#         MainWindow.setStatusBar(self.statusbar)
#         self.retranslateUi(MainWindow)
#         QtCore.QMetaObject.connectSlotsByName(MainWindow)
#         # Подключение к базе данных
#         self.connection = sqlite3.connect('users.db')
#         self.cursor = self.connection.cursor()
#         self.cursor.execute('''
#         CREATE TABLE IF NOT EXISTS users (
#             id INTEGER PRIMARY KEY AUTOINCREMENT,
#             login TEXT NOT NULL UNIQUE,
#             password TEXT NOT NULL
#         )
#         ''')
#         self.connection.commit()
#
#     def retranslateUi(self, MainWindow):
#         _translate = QtCore.QCoreApplication.translate
#         MainWindow.setWindowTitle(_translate("MainWindow", "Регистрация"))
#         self.loginParent.setPlaceholderText(_translate("MainWindow", "логин"))
#         self.passwordParent.setPlaceholderText(_translate("MainWindow", "пароль"))
#         self.lineEdit_3.setPlaceholderText(_translate("MainWindow", "подтвердите пароль"))
#         self.registrParent.setText(_translate("MainWindow", "регистрация"))
#         self.vhodParent.setText(_translate("MainWindow", "вход"))
#
#     def add_user(self):
#         login = self.loginParent.text()
#         password = self.passwordParent.text()
#         confirm_password = self.lineEdit_3.text()
#         if login and password and password == confirm_password:
#             # Проверка на существование пользователя
#             self.cursor.execute('SELECT * FROM users WHERE login=?', (login,))
#             if self.cursor.fetchone():  # Если пользователь найден
#                 QtWidgets.QMessageBox.warning(None, 'Ошибка', 'Логин уже зарегистрирован!')
#                 return
#             # Добавление нового пользователя
#             self.cursor.execute('INSERT INTO users (login, password) VALUES (?, ?)', (login, password))
#             self.connection.commit()
#             QtWidgets.QMessageBox.information(None, 'Успех', 'Пользователь успешно зарегистрирован!')
#         else:
#             QtWidgets.QMessageBox.warning(None, 'Ошибка', 'Пожалуйста, проверьте ввод данных!')
#
#     def open_login_window(self):
#         self.login_dialog = LoginDialog(self.connection)
#         self.login_dialog.exec()
#
#     def closeEvent(self, event):
#         self.connection.close()  # Закрыть соединение с базой данных при закрытии окна
#
#
# class LoginDialog(QtWidgets.QDialog):
#     def __init__(self, connection):
#         super().__init__()
#
#         self.connection = connection
#         self.setWindowTitle("Вход")
#         self.setGeometry(300, 300, 300, 150)
#         self.layout = QtWidgets.QVBoxLayout()
#         self.loginInput = QtWidgets.QLineEdit(self)
#         self.loginInput.setPlaceholderText("Логин")
#         self.layout.addWidget(self.loginInput)
#         self.passwordInput = QtWidgets.QLineEdit(self)
#         self.passwordInput.setPlaceholderText("Пароль")
#         self.passwordInput.setEchoMode(QtWidgets.QLineEdit.EchoMode.Password)
#         self.layout.addWidget(self.passwordInput)
#         self.loginButton = QtWidgets.QPushButton("Войти", self)
#         self.loginButton.clicked.connect(self.check_login)
#         self.layout.addWidget(self.loginButton)
#         self.setLayout(self.layout)
#
#     def check_login(self):
#         login = self.loginInput.text()
#         password = self.passwordInput.text()
#         cursor = self.connection.cursor()
#         cursor.execute('SELECT * FROM users WHERE login=? AND password=?', (login, password))
#         user = cursor.fetchone()
#         if user:
#             print(login)
#             # QtWidgets.QMessageBox.information(self, 'Успех', 'Вход выполнен успешно!')
#             # self.accept()  # Закрывает диалоговое окно
#             self.window = TaskListApp(login)
#             self.window.show()
#
#
#         else:
#             QtWidgets.QMessageBox.warning(self, 'Ошибка', 'Неверный логин или пароль!')
#
#
# import sys
# import sqlite3
# from PyQt6 import QtCore, QtWidgets
#
#
# class Task:
#     def __init__(self, name, urgency, reward, deadline):
#         self.name = name
#         self.urgency = urgency
#         self.reward = reward
#         self.deadline = deadline
#
#
# class TaskInputDialog(QtWidgets.QDialog):
#     def __init__(self):
#         super().__init__()
#         self.setWindowTitle("Добавить задачу")
#         self.setGeometry(100, 100, 300, 250)
#         self.layout = QtWidgets.QVBoxLayout(self)
#         # Ввод названия задачи
#         self.taskNameInput = QtWidgets.QLineEdit(self)
#         self.taskNameInput.setPlaceholderText("Название дела")
#         self.layout.addWidget(self.taskNameInput)
#         # Выбор срочности
#         self.urgencyComboBox = QtWidgets.QComboBox(self)
#         self.urgencyComboBox.addItems(["Срочно", "Желательно", "Не обязательно"])
#         self.layout.addWidget(self.urgencyComboBox)
#         # Ввод награды
#         self.rewardInput = QtWidgets.QLineEdit(self)
#         self.rewardInput.setPlaceholderText("Награда за выполнение задачи")
#         self.layout.addWidget(self.rewardInput)
#         # Ввод дедлайна
#         self.deadlineInput = QtWidgets.QLineEdit(self)
#         self.deadlineInput.setPlaceholderText("Дедлайн (например, 2023-10-31)")
#         self.layout.addWidget(self.deadlineInput)
#         # Кнопка добавления задачи
#         self.addButton = QtWidgets.QPushButton("Добавить задачу", self)
#         self.addButton.clicked.connect(self.accept)
#         self.layout.addWidget(self.addButton)
#
#     def get_task_data(self):
#         return (self.taskNameInput.text(),
#                 self.urgencyComboBox.currentText(),
#                 self.rewardInput.text(),
#                 self.deadlineInput.text())
#
#
# class TaskListApp(QtWidgets.QWidget):
#     def __init__(self, user_login):
#         super().__init__()
#         self.user_login = user_login  # Уникальный логин пользователя
#         self.setWindowTitle("Список задач")
#         self.setGeometry(100, 100, 400, 400)
#         self.layout = QtWidgets.QVBoxLayout(self)
#         # Кнопка для добавления новой задачи
#         self.addTaskButton = QtWidgets.QPushButton("Добавить задачу", self)
#         self.addTaskButton.clicked.connect(self.open_task_input_dialog)
#         self.layout.addWidget(self.addTaskButton)
#         # Список задач
#         self.taskListWidget = QtWidgets.QListWidget(self)
#         self.layout.addWidget(self.taskListWidget)
#         # Подключение к базе данных
#         self.connection = sqlite3.connect('tasks.db')
#         self.cursor = self.connection.cursor()
#         self.cursor.execute('''
#         CREATE TABLE IF NOT EXISTS tasks (
#             id INTEGER PRIMARY KEY AUTOINCREMENT,
#             user_login TEXT NOT NULL,
#             task_name TEXT NOT NULL,
#             urgency TEXT NOT NULL,
#             reward TEXT NOT NULL,
#             deadline TEXT NOT NULL
#         )
#         ''')
#         self.connection.commit()
#         self.load_tasks()
#
#     def load_tasks(self):
#         self.cursor.execute('SELECT task_name, urgency, reward, deadline FROM tasks WHERE user_login=?',
#                             (self.user_login,))
#         tasks = self.cursor.fetchall()
#         for task in tasks: self.display_task(Task(*task))
#
#     def open_task_input_dialog(self):
#         dialog = TaskInputDialog()
#         if dialog.exec() == QtWidgets.QDialog.DialogCode.Accepted:
#             task_data = dialog.get_task_data()
#             self.add_task(*task_data)
#
#     def add_task(self, name, urgency, reward, deadline):
#         if name:  # Проверка, что название задачи не пустое
#             task = Task(name, urgency, reward, deadline)
#             self.display_task(task)
#             self.save_task_to_db(task)
#
#     def display_task(self, task):
#         item = QtWidgets.QListWidgetItem()
#         item.setText(f"{task.name} - Награда: {task.reward} - Дедлайн: {task.deadline}")
#         # Установка цвета в зависимости от срочности
#         color_square = QtWidgets.QWidget()
#         color_square.setFixedSize(15, 15)
#         if task.urgency == "Срочно":
#             color_square.setStyleSheet("background-color: red;")
#         elif task.urgency == "Желательно":
#             color_square.setStyleSheet("background-color: yellow;")
#         else:
#             color_square.setStyleSheet("background-color: green;")
#         # Компоновка для ячейки
#         item_layout = QtWidgets.QHBoxLayout()
#         item_layout.addWidget(color_square)
#         item_layout.addWidget(QtWidgets.QLabel(f"{task.name} - Награда: {task.reward} - Дедлайн: {task.deadline}"))
#         # Установка виджета в элемент списка
#         item.setSizeHint(item_layout.sizeHint())
#         self.taskListWidget.addItem(item)
#         self.taskListWidget.setItemWidget(item, color_square)
#         # Добавляем текст задачи в ячейку
#         text_label = QtWidgets.QLabel(f"{task.name} - Награда: {task.reward} - Дедлайн: {task.deadline}")
#         item_layout.addWidget(text_label)
#         item_layout.addWidget(color_square)
#         item.setSizeHint(item_layout.sizeHint())
#         self.taskListWidget.addItem(item)
#
#     def save_task_to_db(self, task):
#         self.cursor.execute(
#             'INSERT INTO tasks (user_login, task_name, urgency, reward, deadline) VALUES (?, ?, ?, ?, ?)',
#             (self.user_login, task.name, task.urgency, task.reward, task.deadline))
#         self.connection.commit()
#
#     def closeEvent(self, event):
#         self.connection.close()
#
#
# class UserSelectionWindow(object):
#     def setupUi(self, MainWindow):
#         MainWindow.setObjectName("UserSelectionWindow")
#         MainWindow.resize(400, 300)
#
#         self.centralwidget = QWidget(MainWindow)
#         self.centralwidget.setObjectName("centralwidget")
#
#         self.layout = QVBoxLayout(self.centralwidget)
#
#         # Кнопка "Ребенок"
#         self.childButton = QPushButton("Ребенок", self.centralwidget)
#         self.childButton.setObjectName("childButton")
#         self.childButton.clicked.connect(self.open_login_window)  # Подключение к функции
#         self.layout.addWidget(self.childButton)
#
#         # Кнопка "Родитель"
#         self.parentButton = QPushButton("Родитель", self.centralwidget)
#         self.parentButton.setObjectName("parentButton")
#         self.layout.addWidget(self.parentButton)
#
#         MainWindow.setCentralWidget(self.centralwidget)
#
#         self.retranslateUi(MainWindow)
#         QtCore.QMetaObject.connectSlotsByName(MainWindow)
#
#     def retranslateUi(self, MainWindow):
#         _translate = QtCore.QCoreApplication.translate
#         MainWindow.setWindowTitle(_translate("UserSelectionWindow", "Выбор пользователя"))
#
#     def open_login_window(self):
#         self.login_window = LoginWindow()
#         self.login_window.show()
#
#
# class LoginWindow(QWidget):
#     def __init__(self):
#         super().__init__()
#         self.setupUi()
#
#     def setupUi(self):
#         self.setWindowTitle("Вход ребенка")
#         self.setGeometry(100, 100, 300, 200)
#
#         self.layout = QVBoxLayout(self)
#
#         # Поле ввода логина родителя
#         self.parent_login_label = QLabel("Логин родителя:")
#         self.layout.addWidget(self.parent_login_label)
#         self.parent_login_entry = QLineEdit(self)
#         self.layout.addWidget(self.parent_login_entry)
#
#         # Поле ввода логина ребенка
#         self.child_login_label = QLabel("Логин ребенка:")
#         self.layout.addWidget(self.child_login_label)
#         self.child_login_entry = QLineEdit(self)
#         self.layout.addWidget(self.child_login_entry)
#
#         # Поле ввода пароля ребенка
#         self.child_password_label = QLabel("Пароль ребенка:")
#         self.layout.addWidget(self.child_password_label)
#         self.child_password_entry = QLineEdit(self)
#         self.child_password_entry.setEchoMode(QLineEdit.EchoMode.Password)
#         self.layout.addWidget(self.child_password_entry)
#
#         # Кнопка входа
#         self.login_button = QPushButton("Войти", self)
#         self.login_button.clicked.connect(self.login_child)
#         self.layout.addWidget(self.login_button)
#
#     def login_child(self):
#         parent_login = self.parent_login_entry.text().strip()
#         child_login = self.child_login_entry.text().strip()
#         child_password = self.child_password_entry.text().strip()
#
#         # Проверка на заполнение полей
#         if not parent_login or not child_login or not child_password:
#             QMessageBox.warning(self, "Внимание", "Пожалуйста, заполните все поля.")
#             return
#
#         try:
#             # Подключение к базе данных
#             conn = sqlite3.connect('users.db')
#             cursor = conn.cursor()
#
#             # Проверка, существует ли родитель с таким логином
#             cursor.execute("SELECT * FROM users WHERE login=? AND parent_login IS NULL", (parent_login,))
#             parent = cursor.fetchone()
#             if parent is None:
#                 QMessageBox.warning(self, "Ошибка", "Родитель с таким логином не найден.")
#                 conn.close()
#                 return
#
#             # Проверка, существует ли ребенок с таким логином и паролем
#             cursor.execute("SELECT * FROM users WHERE login=? AND password=? AND parent_login=?",
#                            (child_login, child_password, parent_login))
#             child = cursor.fetchone()
#
#             if child is None:
#                 QMessageBox.warning(self, "Ошибка", "Неверный логин или пароль ребенка.")
#                 conn.close()
#                 return
#
#             QMessageBox.information(self, "Успех", "Вход выполнен успешно!")
#             self.close()  # Закрываем окно входа
#
#             # Здесь можно открыть окно ребенка или родителя в зависимости от входа
#             # Например, открытие основного окна ребенка:
#             # child_main_window = ChildMainWindow()
#             # child_main_window.show()
#
#         except sqlite3.Error as e:
#             QMessageBox.critical(self, "Ошибка базы данных", f"Произошла ошибка: {e}")
#
#
# # Основной код для запуска приложения
# if __name__ == "__main__":
#     # Создание базы данных и таблицы, если еще не существует
#     conn = sqlite3.connect('users.db')
#     cursor = conn.cursor()
#     cursor.execute("""
#     CREATE TABLE IF NOT EXISTS users (
#         id INTEGER PRIMARY KEY AUTOINCREMENT,
#         login TEXT UNIQUE NOT NULL,
#         password TEXT NOT NULL,
#         parent_login TEXT,
#         FOREIGN KEY (parent_login) REFERENCES users (login)
#     );
#     """)
#     conn.commit()
#     conn.close()
#
#     app = QApplication(sys.argv)
#     MainWindow = QMainWindow()
#     ui = UserSelectionWindow()
#     ui.setupUi(MainWindow)
#     MainWindow.show()
#     sys.exit(app.exec())