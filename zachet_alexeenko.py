import requests

from PySide6 import QtWidgets, QtCore, QtGui

from ui.zachet import Ui_Form
from ui.login import Ui_FormLogin


class DjangoWebQt(QtWidgets.QWidget):

    def __init__(self, parent=None):
        super().__init__(parent)

        self.ui = Ui_Form()
        self.ui.setupUi(self)
        self.current_item = None
        self.list_todo = None

        self.url = 'http://127.0.0.1:8000'

        self.initUi()

    def initUi(self):
        self.setWindowTitle("Работа с БД через API")
        self.setMinimumSize(965, 600)
        self.child_window = Login()
        self.ui.pushButtonGet.clicked.connect(self.onPushButtonNoteGetAll)
        self.ui.pushButtonLogin.clicked.connect(self.onPushButtonLogin)
        self.ui.pushButtonLogOut.clicked.connect(self.onPushButtonLogOut)
        self.ui.comboBox.addItems(['Активно', 'Отложено', 'Выполнено'])
        self.ui.create_todo.clicked.connect(self.postToDo)
        self.child_window.user[str].connect(self.setUserName)
        self.ui.pushButtonLogOut.setEnabled(False)
        self.ui.pushButtonDetails.setEnabled(False)
        self.ui.pushButtonDelete.setEnabled(False)
        self.ui.pushButtonPut.setEnabled(False)
        self.ui.tableView.clicked.connect(self.clicked_table)
        self.ui.pushButtonDelete.clicked.connect(self.onPushButtonNoteDelete)

    def clicked_table(self, item: QtCore.QModelIndex):
        self.ui.pushButtonDelete.setEnabled(True)
        self.ui.pushButtonDetails.setEnabled(True)
        self.ui.pushButtonPut.setEnabled(True)
        self.current_item = item.row()

    def onPushButtonNoteDelete(self):


    def onPushButtonNoteDetail(self):
        ...

    # def event(self, event:QtCore.QEvent) -> bool:
    #     print(event.type())

    def onPushButtonLogOut(self):
        reply = QtWidgets.QMessageBox.question(self,
                                               'Выход', 'Вы действительно хотите выйти?',
                                               QtWidgets.QMessageBox.Yes,
                                               QtWidgets.QMessageBox.No)
        if reply == QtWidgets.QMessageBox.Yes:
            self.ui.label_user.clear()
            self.child_window.token = None
            self.ui.pushButtonLogOut.setEnabled(False)
            self.ui.pushButtonLogin.setEnabled(True)
            self.ui.tableView.setModel(None)

    def setUserName(self, user):
        self.ui.label_user.setText(user)
        self.ui.pushButtonLogOut.setEnabled(True)
        self.ui.pushButtonLogin.setEnabled(False)

    def onPushButtonNoteGetAll(self):
        try:
            resp = requests.get(
                f"{self.url}/api/v1/todo/",
                headers={'Authorization': "token {}".format(self.child_window.token)}
            )
            self.ui.plainTextEdit.setPlainText(str(resp.status_code))

            if resp.status_code == 200:
                self.list_todo = resp.json()
                headers = ["Автор", "Название", "Текст задания", "Крайний срок"]
                stm = QtGui.QStandardItemModel()
                stm.setHorizontalHeaderLabels(headers)

                key_dict = ["author", "title", "message", "deadline"]

                for row in range(len(self.list_todo)):
                    for i in range(len(headers)):
                        stm.setItem(row, i, QtGui.QStandardItem(str(self.list_todo[row][key_dict[i]])))

                self.ui.tableView.setModel(stm)

            elif resp.status_code == 401:
                QtWidgets.QMessageBox.warning(
                    self,
                    "Внимание", "Нужно авторизоваться в системе, чтобы получить список всех дел",
                    QtWidgets.QMessageBox.Yes
                )
            else:
                QtWidgets.QMessageBox.warning(
                    self,
                    "Внимание", "Что-то пошло не так, повторите попытку",
                    QtWidgets.QMessageBox.Yes
                )
        except requests.exceptions.ConnectionError:
            QtWidgets.QMessageBox.warning(
                self,
                "Внимание", "Нет соединения с сервером!",
                QtWidgets.QMessageBox.Yes
            )

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
        try:
            request = requests.post(
                f"{self.url}/api/v1/todo/",
                json=dict_todo,
                headers={'Authorization': "token {}".format(self.child_window.token)}
            )
            print(request.status_code)
            if request.status_code == 200:
                QtWidgets.QMessageBox.warning(self, "Внимание", "Вы создали новое дело!", QtWidgets.QMessageBox.Yes)
                self.ui.lineEdit.clear()
                self.ui.textEdit.clear()

            if request.status_code == 401:
                QtWidgets.QMessageBox.warning(
                    self,
                    "Внимание", "Дело не создано, нужно авторизоваться в системе!",
                    QtWidgets.QMessageBox.Yes
                )
        except requests.exceptions.ConnectionError:
            QtWidgets.QMessageBox.warning(
                self,
                "Внимание", "Нет соединения с сервером!",
                QtWidgets.QMessageBox.Yes
            )

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
    token = None
    user = QtCore.Signal(str)

    def __init__(self, parent=None):
        super().__init__(parent)

        self.ui = Ui_FormLogin()
        self.ui.setupUi(self)

        self.initUi()

    def initUi(self):
        self.setWindowTitle("Авторизация")
        self.ui.pushButtonLogin.clicked.connect(self.onPushButtonLogin)

    def onPushButtonLogin(self):
        try:
            username = self.ui.lineEdit.text()
            password = self.ui.lineEdit_2.text()
            dict_login = dict(username=username, password=password)
            request = requests.post(f"http://127.0.0.1:8000/api/v1/login/", json=dict_login)

            if request.status_code == 200:
                QtWidgets.QMessageBox.warning(self, "Поздравляем", "Вы вошли в систему!")
                self.token = request.json()['token']
                self.user.emit(dict_login["username"])
                self.ui.lineEdit.clear()
                self.ui.lineEdit_2.clear()
                self.close()
            else:
                QtWidgets.QMessageBox.warning(self, "Внимание", "Данные введены неправильно!")
                self.ui.lineEdit.clear()
                self.ui.lineEdit_2.clear()
        except requests.exceptions.ConnectionError:
            QtWidgets.QMessageBox.warning(
                self,
                "Внимание", "Нет соединения с сервером!",
                QtWidgets.QMessageBox.Yes
            )

    def closeEvent(self, event: QtGui.QCloseEvent) -> None:
        self.ui.lineEdit.clear()
        self.ui.lineEdit_2.clear()
        event.accept()


if __name__ == "__main__":
    app = QtWidgets.QApplication()

    myapp = DjangoWebQt()
    myapp.show()

    app.exec_()
