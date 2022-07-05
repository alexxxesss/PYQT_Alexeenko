import requests

from PySide6 import QtWidgets, QtCore, QtGui

from ui.zachet import Ui_Form


class DjangoWebQt(QtWidgets.QWidget):

    def __init__(self, parent=None):
        super().__init__(parent)

        self.ui = Ui_Form()
        self.ui.setupUi(self)

        self.url = 'http://127.0.0.1:8000'

        self.initUi()

    def initUi(self):
        self.ui.get_all_todo.clicked.connect(self.getAllToDo)

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

    def closeEvent(self, event: QtGui.QCloseEvent) -> None:
        reply = QtWidgets.QMessageBox.question(self,
                                               'Закрыть окно?', 'Вы хотите закрыть окно?',
                                               QtWidgets.QMessageBox.Yes,
                                               QtWidgets.QMessageBox.No)
        if reply == QtWidgets.QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()


if __name__ == "__main__":
    app = QtWidgets.QApplication()

    myapp = DjangoWebQt()
    myapp.show()

    app.exec_()
