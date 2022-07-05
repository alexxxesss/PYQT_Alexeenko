import requests

from PySide6 import QtWidgets, QtCore, QtGui

from ui.zachet import Ui_Form
from ui.login import Ui_FormLogin


class DjangoWebQt(QtWidgets.QWidget):

    def __init__(self, parent=None):
        super().__init__(parent)

        self.ui = Ui_Form()
        self.ui.setupUi(self)

        self.url = 'http://127.0.0.1:8000'

        self.initUi()

        self.child_window = Login()

    def initUi(self):
        self.setWindowTitle("Работа с БД через API")
        self.setFixedSize(965, 600)
        self.ui.get_all_todo.clicked.connect(self.getAllToDo)
        self.ui.pushButtonLogin.clicked.connect(self.onPushButtonLogin)
        self.ui.comboBox.addItems(['Активно', 'Отложено', 'Выполнено'])
        self.ui.create_todo.clicked.connect(self.postToDo)

    def getAllToDo(self):
        resp = requests.get(f"{self.url}/api/v1/todo/")
        list_todo = resp.json()
        new_list_todo = []
        self.ui.plainTextEdit.setPlainText(str(list_todo))

        headers = [
            "Автор",
            "Название",
            "Текст TODO",
            "Публичная",
            "Важная",
            "Статус",
            "Крайний срок",
            "Дата создания",
            "Дата обновления"
        ]
        stm = QtGui.QStandardItemModel()
        stm.setHorizontalHeaderLabels(headers)

        key_dict = []
        for key in list_todo[0].keys():
            key_dict.append(key)

        for row in range(len(list_todo)):
            for i in range(len(headers)):
                stm.setItem(row, i, QtGui.QStandardItem(str(list_todo[row][key_dict[i]])))

        self.ui.tableView.setModel(stm)

    def postToDo(self):

        title = self.ui.lineEdit.text()
        message = self.ui.textEdit.toPlainText()

        if self.ui.checkBox.isChecked():
            public = True
        else:
            public = False

        if self.ui.checkBox_2.isChecked():
            importance = True
        else:
            importance = False

        dict_status = {
            "Активно": "Active",
            "Отложено": "Delayed",
            "Выполнено": "Finish"
        }

        status = dict_status[self.ui.comboBox.currentText()]

        deadline = self.ui.dateTimeEdit.dateTime().toString("yyyy-MM-ddTHH:mm:ss")

        dict_todo = dict(
            title=title,
            message=message,
            public=public,
            importance=importance,
            status=status,
            deadline=deadline
        )
        print(dict_todo)

    def onPushButtonLogin(self):
        self.child_window.show()

    def closeEvent(self, event: QtGui.QCloseEvent) -> None:
        reply = QtWidgets.QMessageBox.question(self,
                                               'Закрыть окно?', 'Вы хотите закрыть окно?',
                                               QtWidgets.QMessageBox.Yes,
                                               QtWidgets.QMessageBox.No)
        if reply == QtWidgets.QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()


class Login(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.ui = Ui_FormLogin()
        self.ui.setupUi(self)

        self.initUi()

    def initUi(self):
        self.setWindowTitle("Авторизация")
        self.ui.pushButtonLogin.clicked.connect(self.onPushButtonLogin)

    def onPushButtonLogin(self):
        username = self.ui.lineEdit.text()
        password = self.ui.lineEdit_2.text()
        self.dict_login = dict(username=username, password=password)

        request = requests.post(f"http://127.0.0.1:8000/api/v1/login/", json=self.dict_login)

        if request.status_code == 200:
            QtWidgets.QMessageBox.warning(self, "Поздравляем", "Вы вошли в систему!")
            self.close()
        else:
            QtWidgets.QMessageBox.warning(self, "Внимание", "Данные введены неправильно!")


if __name__ == "__main__":
    app = QtWidgets.QApplication()

    myapp = DjangoWebQt()
    myapp.show()

    app.exec_()
