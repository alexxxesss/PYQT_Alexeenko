import time

from PySide6 import QtCore, QtWidgets

from ui.P2_practice import Ui_Form


class MyApp(QtWidgets.QWidget):

    def __init__(self, parent=None):
        super().__init__(parent)

        self.initUi()
        self.initThreads()

    def initThreads(self):
        self.timerThread = TimerThread()

    def initUi(self):
        self.setFixedSize(300, 200)

        self.lineEditStart = QtWidgets.QLineEdit()
        self.lineEditStart.setPlaceholderText("Введите количество секунд")

        self.pushButtonStart = QtWidgets.QPushButton()
        self.pushButtonStart.setText("Старт")
        self.pushButtonStart.setSizePolicy(QtWidgets.QSizePolicy.Policy.Expanding,
                                           QtWidgets.QSizePolicy.Policy.Expanding)

        self.pushButtonStop = QtWidgets.QPushButton()
        self.pushButtonStop.setText("Стоп")
        self.pushButtonStop.setSizePolicy(QtWidgets.QSizePolicy.Policy.Expanding,
                                           QtWidgets.QSizePolicy.Policy.Expanding)

        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(self.lineEditStart)
        layout.addWidget(self.pushButtonStart)
        layout.addWidget(self.pushButtonStop)

        self.setLayout(layout)

        layout.addSpacerItem(
            QtWidgets.QSpacerItem(
                1,
                1,
                QtWidgets.QSizePolicy.Policy.Expanding,
                QtWidgets.QSizePolicy.Policy.Expanding
            )
        )

        self.pushButtonStart.clicked.connect(self.onPushButtonStartClicked)

    # pushButtonStart clots

    def onPushButtonStartClicked(self):
        self.timerThread.timerCount = int(self.lineEditStart.text())
        self.timerThread.start()


class TimerThread(QtCore.QThread):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.timerCount = None

    def run(self) -> None:
        if self.timerCount is None:
            self.timerCount = 10
        for i in range(self.timerCount, 0, -1):
            print(i)
            time.sleep(1)


if __name__ == "__main__":
    app = QtWidgets.QApplication()

    myapp = MyApp()
    myapp.show()

    app.exec_()
