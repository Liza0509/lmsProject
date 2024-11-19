import sys

from PyQt6.QtWidgets import QApplication, QWidget, QPushButton
from PyQt6.QtWidgets import QMainWindow, QLabel
from PyQt6 import uic  # Импортируем uic

class FirstForm(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('войти_как.ui', self)  # Загружаем дизайн
        self.mainChild.clicked.connect(self.openChildRegistr)
        self.mainParent.clicked.connect(self.openParentRegistr)

    def openChildRegistr(self):
        self.ChildRegistr = ChildRegistr()
        self.ChildRegistr.show()
        self.close()

    def openParentRegistr(self):
        self.ParentRegistr = ParentRegistr()
        self.ParentRegistr.show()
        self.close()


class ChildRegistr(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('вход_дети.ui', self)  # Загружаем дизайн

class ParentRegistr(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('регистрация_родитель.ui', self)  # Загружаем дизайн

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = FirstForm()
    ex.show()
    sys.exit(app.exec())
