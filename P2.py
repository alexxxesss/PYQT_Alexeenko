import time

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

        self.ui.pushButton_6.clicked.connect(self.onPBGetMonitorInfo)

        self.ui.dial.valueChanged.connect(self.showLCD)
        self.ui.horizontalSlider.valueChanged.connect(self.showLCD)

        self.ui.comboBox.addItems(["HEX", "DEC", "OCT", "BIN"])
        self.ui.comboBox.currentIndexChanged.connect(self.changeLCDview)

        self.ui.dial.installEventFilter(self)

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

        self.move((screen_width - program_width) / 2, (screen_height - program_height) / 2)

    def onPBLBClicked(self):
        screen_height = QtWidgets.QApplication.primaryScreen().size().height()

        program_height = self.height()

        self.move(0, screen_height - program_height - 72)

    def onPBRBClicked(self):
        screen_width = QtWidgets.QApplication.screenAt(self.pos()).size().width()
        screen_height = QtWidgets.QApplication.screenAt(self.pos()).size().height()

        program_width = self.width()
        program_height = self.height()

        self.move(screen_width - program_width, screen_height - program_height - 72)

    def onPBGetMonitorInfo(self):
        self.ui.plainTextEdit.appendPlainText("*" * 15)
        self.ui.plainTextEdit.appendPlainText(f"Количество экранов: {str(len(QtWidgets.QApplication.screens()))}")
        self.ui.plainTextEdit.appendPlainText(f"Наименование экрана: {QtWidgets.QApplication.primaryScreen().name()}")
        self.ui.plainTextEdit.appendPlainText(
            "Разрешение экрана: " +
            str(QtWidgets.QApplication.screenAt(self.pos()).size().width()) +
            " на " +
            str(QtWidgets.QApplication.screenAt(self.pos()).size().height())
        )
        self.ui.plainTextEdit.appendPlainText(
            f"Окно находится на экране: {QtWidgets.QApplication.screenAt(self.pos()).name()}"
        )
        self.ui.plainTextEdit.appendPlainText(
            f"Размеры окна:  Ширина {self.size().width()}  Высота {self.size().height()}"
        )
        self.ui.plainTextEdit.appendPlainText(
            f"Минимальные размеры окна:  Ширина {self.minimumWidth()}  Высота {self.minimumHeight()}"
        )
        self.ui.plainTextEdit.appendPlainText(
            f"Текущее положение окна:\n" 
            f"X: {self.pos().x()}  " 
            f"Y: {self.pos().y()}"
        )
        self.ui.plainTextEdit.appendPlainText(
            f"Центр окна:\n"
            f"X: {self.pos().x() + self.width() / 2}  "
            f"Y: {self.pos().y() + self.height() / 2}"
        )
        self.ui.plainTextEdit.appendPlainText("*" * 15)

    def changeEvent(self, event: QtCore.QEvent) -> None:
        print(event.type())
        if event.type() == QtCore.QEvent.Type.WindowStateChange:
            if self.isMinimized():
                self.ui.plainTextEdit.appendPlainText(f"{time.ctime()}: Окно свернуто")

            if self.isMaximized():
                self.ui.plainTextEdit.appendPlainText(f"{time.ctime()}: Окно развёрнуто")

            if self.isHidden():
                self.ui.plainTextEdit.appendPlainText(f"{time.ctime()}: Окно прятано")

    def moveEvent(self, event: QtGui.QMoveEvent) -> None:
        print(self.pos().x(), self.pos().y())

    def resizeEvent(self, event: QtGui.QResizeEvent) -> None:
        print(self.size())

    def keyPressEvent(self, event: QtGui.QKeyEvent) -> None:
        print(event.text())

    def change(self):
        pass

    def event(self, event: QtCore.QEvent) -> bool:
        if event.type() == QtCore.QEvent.KeyPress:
            print(f"{event.key()} is pressed")

        return QtWidgets.QWidget.event(self, event)

    def eventFilter(self, watched: QtCore.QObject, event: QtCore.QEvent) -> bool:

        if watched == self.ui.dial and event.type() == QtCore.QEvent.KeyPress:
            if event.text() == "+":
                self.ui.dial.setValue(self.ui.dial.value() + 1)
            if event.text() == "-":
                self.ui.dial.setValue(self.ui.dial.value() - 1)

            self.ui.plainTextEdit.appendPlainText(f"Новое значение мощности: {self.ui.dial.value()}")

        return super(MyWidgetsForm, self).eventFilter(watched, event)

    def showLCD(self):

        if self.sender().objectName() == "dial":
            value = self.ui.dial.value()
            self.ui.horizontalSlider.setValue(value)

        if self.sender().objectName() == "horizontalSlider":
            value = self.ui.horizontalSlider.value()
            self.ui.dial.setValue(value)

        self.ui.lcdNumber.display(value)

    def changeLCDview(self):

        dict_LCD = {
            "HEX": self.ui.lcdNumber.setHexMode,
            "BIN": self.ui.lcdNumber.setBinMode,
            "OCT": self.ui.lcdNumber.setOctMode,
            "DEC": self.ui.lcdNumber.setDecMode
        }

        dict_LCD[self.ui.comboBox.currentText()]()


if __name__ == "__main__":
    app = QtWidgets.QApplication()

    myapp = MyWidgetsForm()
    myapp.show()

    app.exec_()
