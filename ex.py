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
        self.cursor.execute('SELECT id, task_name, urgency, reward, deadline FROM tasks WHERE user_login=?',
                            (self.user_login,))
        tasks = self.cursor.fetchall()
        for task in tasks:
            self.display_task(Task(*task))  # Обновленная функция

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
        if task.urgency == "Срочно":
            color_square.setStyleSheet("background-color: red;")
        elif task.urgency == "Желательно":
            color_square.setStyleSheet("background-color: yellow;")
        else:
            color_square.setStyleSheet("background-color: green;")

        # Компоновка для ячейки
        item_layout = QtWidgets.QHBoxLayout()
        item_layout.addWidget(color_square)
        item_layout.addWidget(QtWidgets.QLabel(f"{task.name} - Награда: {task.reward} - Дедлайн: {task.deadline}"))

        # Кнопка удаления задачи
        delete_button = QtWidgets.QPushButton("Удалить", self)
        delete_button.clicked.connect(lambda: self.delete_task(task.id, item))
        item_layout.addWidget(delete_button)

        item.setSizeHint(item_layout.sizeHint())
        self.taskListWidget.addItem(item)
        self.taskListWidget.setItemWidget(item, color_square)

    def save_task_to_db(self, task):
        self.cursor.execute(
            'INSERT INTO tasks (user_login, task_name, urgency, reward, deadline) VALUES (?, ?, ?, ?, ?)',
            (self.user_login, task.name, task.urgency, task.reward, task.deadline))
        self.connection.commit()

    def delete_task(self, task_id, item):
        # Удаление задачи из базы данных
        self.cursor.execute('DELETE FROM tasks WHERE id=?', (task_id,))
        self.connection.commit()

        # Удаление задачи из интерфейса (списка)
        self.taskListWidget.takeItem(self.taskListWidget.row(item))

    def closeEvent(self, event):
        self.connection.close()
