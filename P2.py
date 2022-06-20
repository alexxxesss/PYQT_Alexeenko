from PySide6 import QtCore, QtWidgets, QtGui
from ui.P2_practice import Ui_Form


class MyWidgetsForm(QtWidgets.QWidget):

    def __init__(self, parent=None):
        super().__init__(parent)

        self.ui = Ui_Form()
        self.ui.setupUi(self)

        self.setMouseTracking(True)

        self.initUi()

    def initUi(self):
        self.setWindowTitle("Моя программа")

        self.ui.pushButton.clicked.connect(self.onPBLTClicked)
        self.ui.pushButton_2.clicked.connect(self.onPBRTClicked)
        self.ui.pushButton_3.clicked.connect(self.onPBCClicked)
        self.ui.pushButton_4.clicked.connect(self.onPBLBClicked)
        self.ui.pushButton_5.clicked.connect(self.onPBRBClicked)

    def onPBLTClicked(self):
        self.move(0, 0)

    def onPBRTClicked(self):
        screen_width = QtWidgets.QApplication.primaryScreen().size().width()
        program_width = self.width()

        self.move(screen_width - program_width, 0)

    def onPBCClicked(self):
        screen_width = QtWidgets.QApplication.primaryScreen().size().width()
        screen_height = QtWidgets.QApplication.primaryScreen().size().height()

        program_width = self.width()
        program_height = self.height()

        self.move((screen_width - program_width)/2, (screen_height - program_height)/2)

    def onPBLBClicked(self):
        screen_height = QtWidgets.QApplication.primaryScreen().size().height()

        program_height = self.height()

        self.move(0, screen_height - program_height)

    def onPBRBClicked(self):
        screen_width = QtWidgets.QApplication.screenAt(self.pos()).size().width()
        screen_height = QtWidgets.QApplication.screenAt(self.pos()).size().height()

        program_width = self.width()
        program_height = self.height()

        self.move(screen_width - program_width, screen_height - program_height)

    # def event(self, event: QtCore.QEvent) -> bool:
    #     if event.type() == QtCore.QEvent.Move:
    #         print(event.pos().x(), event.pos().y())
    #
    #     return QtWidgets.QWidget.event(self, event)


if __name__ == "__main__":
    app = QtWidgets.QApplication()

    myapp = MyWidgetsForm()
    myapp.show()

    app.exec_()
