import sys
import sqlite3
from PyQt6 import QtCore, QtGui, QtWidgets
from list import TaskListApp

class Ui_MainWindow(object):
    def __init__(self, ):
        super().__init__()

    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 600)
        self.centralwidget = QtWidgets.QWidget(parent=MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayoutWidget = QtWidgets.QWidget(parent=self.centralwidget)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(290, 160, 211, 181))
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.loginParent = QtWidgets.QLineEdit(parent=self.verticalLayoutWidget)
        self.loginParent.setObjectName("loginParent")
        self.verticalLayout_2.addWidget(self.loginParent)
        self.passwordParent = QtWidgets.QLineEdit(parent=self.verticalLayoutWidget)
        self.passwordParent.setObjectName("passwordParent")
        self.passwordParent.setEchoMode(QtWidgets.QLineEdit.EchoMode.Password)  # Скрыть ввод пароля
        self.verticalLayout_2.addWidget(self.passwordParent)
        self.lineEdit_3 = QtWidgets.QLineEdit(parent=self.verticalLayoutWidget)
        self.lineEdit_3.setObjectName("lineEdit_3")
        self.lineEdit_3.setEchoMode(QtWidgets.QLineEdit.EchoMode.Password)  # Скрыть ввод подтверждения пароля
        self.verticalLayout_2.addWidget(self.lineEdit_3)
        self.verticalLayout_3 = QtWidgets.QVBoxLayout()
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.registrParent = QtWidgets.QPushButton(parent=self.verticalLayoutWidget)
        self.registrParent.setObjectName("registrParent")
        self.registrParent.clicked.connect(self.add_user)  # Подключаем обработчик
        self.verticalLayout_3.addWidget(self.registrParent)
        self.vhodParent = QtWidgets.QPushButton(parent=self.verticalLayoutWidget)
        self.vhodParent.setObjectName("vhodParent")
        self.vhodParent.clicked.connect(self.open_login_window)  # Подключаем обработчик для кнопки "вход"
        self.verticalLayout_3.addWidget(self.vhodParent)
        self.verticalLayout_2.addLayout(self.verticalLayout_3)
        self.verticalLayout.addLayout(self.verticalLayout_2)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(parent=MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 26))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(parent=MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)
        # Подключение к базе данных
        self.connection = sqlite3.connect('users.db')
        self.cursor = self.connection.cursor()
        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            login TEXT NOT NULL UNIQUE,
            password TEXT NOT NULL
        )
        ''')
        self.connection.commit()

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Регистрация"))
        self.loginParent.setPlaceholderText(_translate("MainWindow", "логин"))
        self.passwordParent.setPlaceholderText(_translate("MainWindow", "пароль"))
        self.lineEdit_3.setPlaceholderText(_translate("MainWindow", "подтвердите пароль"))
        self.registrParent.setText(_translate("MainWindow", "регистрация"))
        self.vhodParent.setText(_translate("MainWindow", "вход"))

    def add_user(self):
        login = self.loginParent.text()
        password = self.passwordParent.text()
        confirm_password = self.lineEdit_3.text()
        if login and password and password == confirm_password:
            # Проверка на существование пользователя
            self.cursor.execute('SELECT * FROM users WHERE login=?', (login,))
            if self.cursor.fetchone():  # Если пользователь найден
                QtWidgets.QMessageBox.warning(None, 'Ошибка', 'Логин уже зарегистрирован!')
                return
            # Добавление нового пользователя
            self.cursor.execute('INSERT INTO users (login, password) VALUES (?, ?)', (login, password))
            self.connection.commit()
            QtWidgets.QMessageBox.information(None, 'Успех', 'Пользователь успешно зарегистрирован!')
        else:
            QtWidgets.QMessageBox.warning(None, 'Ошибка', 'Пожалуйста, проверьте ввод данных!')

    def open_login_window(self):
        self.login_dialog = LoginDialog(self.connection)
        self.login_dialog.exec()

    def closeEvent(self, event):
        self.connection.close()  # Закрыть соединение с базой данных при закрытии окна


class LoginDialog(QtWidgets.QDialog):
    def __init__(self, connection):
        super().__init__()

        self.connection = connection
        self.setWindowTitle("Вход")
        self.setGeometry(300, 300, 300, 150)
        self.layout = QtWidgets.QVBoxLayout()
        self.loginInput = QtWidgets.QLineEdit(self)
        self.loginInput.setPlaceholderText("Логин")
        self.layout.addWidget(self.loginInput)
        self.passwordInput = QtWidgets.QLineEdit(self)
        self.passwordInput.setPlaceholderText("Пароль")
        self.passwordInput.setEchoMode(QtWidgets.QLineEdit.EchoMode.Password)
        self.layout.addWidget(self.passwordInput)
        self.loginButton = QtWidgets.QPushButton("Войти", self)
        self.loginButton.clicked.connect(self.check_login)
        self.layout.addWidget(self.loginButton)
        self.setLayout(self.layout)

    def check_login(self):
        login = self.loginInput.text()
        password = self.passwordInput.text()
        cursor = self.connection.cursor()
        cursor.execute('SELECT * FROM users WHERE login=? AND password=?', (login, password))
        user = cursor.fetchone()
        if user:
            print(login)
            #QtWidgets.QMessageBox.information(self, 'Успех', 'Вход выполнен успешно!')
            #self.accept()  # Закрывает диалоговое окно
            self.window = TaskListApp(login)
            self.window.show()


        else:
            QtWidgets.QMessageBox.warning(self, 'Ошибка', 'Неверный логин или пароль!')


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec())
