from PySide6 import QtWidgets, QtCore, QtGui

from ui.zachet import Ui_Form


class DjangoWebQt(QtWidgets.QWidget):

    def __init__(self, parent=None):
        super().__init__(parent)

        self.ui = Ui_Form()
        self.ui.setupUi(self)

        self.initUi()

    def initUi(self):
        ...


if __name__ == "__main__":
    app = QtWidgets.QApplication()

    myapp = DjangoWebQt()
    myapp.show()

    app.exec_()
