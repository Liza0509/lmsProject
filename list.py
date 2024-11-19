import sys
import sqlite3
from PyQt6 import QtCore, QtWidgets
class Task:
    def __init__(self, name, urgency, reward, deadline):
        self.name = name
        self.urgency = urgency
        self.reward = reward
        self.deadline = deadline
class TaskInputDialog(QtWidgets.QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Добавить задачу")
        self.setGeometry(100, 100, 300, 250)
        self.layout = QtWidgets.QVBoxLayout(self)
        # Ввод названия задачи
        self.taskNameInput = QtWidgets.QLineEdit(self)
        self.taskNameInput.setPlaceholderText("Название дела")
        self.layout.addWidget(self.taskNameInput)
        # Выбор срочности
        self.urgencyComboBox = QtWidgets.QComboBox(self)
        self.urgencyComboBox.addItems(["Срочно", "Желательно", "Не обязательно"])
        self.layout.addWidget(self.urgencyComboBox)
        # Ввод награды
        self.rewardInput = QtWidgets.QLineEdit(self)
        self.rewardInput.setPlaceholderText("Награда за выполнение задачи")
        self.layout.addWidget(self.rewardInput)
        # Ввод дедлайна
        self.deadlineInput = QtWidgets.QLineEdit(self)
        self.deadlineInput.setPlaceholderText("Дедлайн (например, 2023-10-31)")
        self.layout.addWidget(self.deadlineInput)
        # Кнопка добавления задачи
        self.addButton = QtWidgets.QPushButton("Добавить задачу", self)
        self.addButton.clicked.connect(self.accept)
        self.layout.addWidget(self.addButton)
    def get_task_data(self):
        return (self.taskNameInput.text(),
                self.urgencyComboBox.currentText(),
                self.rewardInput.text(),
                self.deadlineInput.text())
class TaskListApp(QtWidgets.QWidget):
    def __init__(self, user_login):
        super().__init__()
        self.user_login = user_login  # Уникальный логин пользователя
        self.setWindowTitle("Список задач")
        self.setGeometry(100, 100, 400, 400)
        self.layout = QtWidgets.QVBoxLayout(self)
        # Кнопка для добавления новой задачи
        self.addTaskButton = QtWidgets.QPushButton("Добавить задачу", self)
        self.addTaskButton.clicked.connect(self.open_task_input_dialog)
        self.layout.addWidget(self.addTaskButton)
        # Список задач
        self.taskListWidget = QtWidgets.QListWidget(self)
        self.layout.addWidget(self.taskListWidget)
        # Подключение к базе данных
        self.connection = sqlite3.connect('tasks.db')
        self.cursor = self.connection.cursor()
        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_login TEXT NOT NULL,
            task_name TEXT NOT NULL,
            urgency TEXT NOT NULL,
            reward TEXT NOT NULL,
            deadline TEXT NOT NULL
        )
        ''')
        self.connection.commit()
        self.load_tasks()
    def load_tasks(self):
        self.cursor.execute('SELECT task_name, urgency, reward, deadline FROM tasks WHERE user_login=?',
                            (self.user_login,))
        tasks = self.cursor.fetchall()
        for task in tasks: self.display_task(Task(*task))
    def open_task_input_dialog(self):
        dialog = TaskInputDialog()
        if dialog.exec() == QtWidgets.QDialog.DialogCode.Accepted:
            task_data = dialog.get_task_data()
            self.add_task(*task_data)
    def add_task(self, name, urgency, reward, deadline):
        if name:  # Проверка, что название задачи не пустое
            task = Task(name, urgency, reward, deadline)
            self.display_task(task)
            self.save_task_to_db(task)
    def display_task(self, task):
        item = QtWidgets.QListWidgetItem()
        item.setText(f"{task.name} - Награда: {task.reward} - Дедлайн: {task.deadline}")
        # Установка цвета в зависимости от срочности
        color_square = QtWidgets.QWidget()
        color_square.setFixedSize(15, 15)
        if task.urgency == "Срочно": color_square.setStyleSheet("background-color: red;")
        elif task.urgency == "Желательно": color_square.setStyleSheet("background-color: yellow;")
        else: color_square.setStyleSheet("background-color: green;")
        # Компоновка для ячейки
        item_layout = QtWidgets.QHBoxLayout()
        item_layout.addWidget(color_square)
        item_layout.addWidget(QtWidgets.QLabel(f"{task.name} - Награда: {task.reward} - Дедлайн: {task.deadline}"))
        # Установка виджета в элемент списка
        item.setSizeHint(item_layout.sizeHint())
        self.taskListWidget.addItem(item)
        self.taskListWidget.setItemWidget(item, color_square)
        # Добавляем текст задачи в ячейку
        text_label = QtWidgets.QLabel(f"{task.name} - Награда: {task.reward} - Дедлайн: {task.deadline}")
        item_layout.addWidget(text_label)
        item_layout.addWidget(color_square)
        item.setSizeHint(item_layout.sizeHint())
        self.taskListWidget.addItem(item)
    def save_task_to_db(self, task):
        self.cursor.execute(
            'INSERT INTO tasks (user_login, task_name, urgency, reward, deadline) VALUES (?, ?, ?, ?, ?)',
            (self.user_login, task.name, task.urgency, task.reward, task.deadline))
        self.connection.commit()
    def closeEvent(self, event): self.connection.close()

# if __name__ == "__main__":
#     app = QtWidgets.QApplication(sys.argv)
#     # Пример: логин пользователя (в реальном приложении логин может быть получен из предыдущего окна)
#     #user_login = "example_user"  # Здесь следует заменить на логин текущего пользователя
#     window = TaskListApp(user_login)
#     window.show()
#     sys.exit(app.exec())