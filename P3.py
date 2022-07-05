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

        self.timerThread.started.connect(self.timerThreadStarted)
        self.timerThread.finished.connect(self.timerThreadFinished)

        self.timerThread.timerSignal.connect(self.timerThreadTimerSignal)

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
        self.pushButtonStop.setEnabled(False)

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
        self.pushButtonStop.clicked.connect(self.onPushButtonStopClicked)

    # pushButtonStart clots

    def onPushButtonStartClicked(self):
        try:
            self.timerThread.timerCount = int(self.lineEditStart.text())
            self.timerThread.start()
        except ValueError:
            self.lineEditStart.setText("")
            QtWidgets.QMessageBox.warning(self, "Ошибка", "Таймер поддерживает только целочисленные значения!")

    # thread slots

    def timerThreadStarted(self):
        self.pushButtonStart.setEnabled(False)
        self.pushButtonStop.setEnabled(True)
        self.lineEditStart.setEnabled(False)

    def timerThreadFinished(self):
        self.pushButtonStop.setEnabled(False)
        self.pushButtonStart.setEnabled(True)
        self.lineEditStart.setEnabled(True)
        self.lineEditStart.setText("")
        QtWidgets.QMessageBox.about(self, "Ура!!!", "Отсчет закончен!")

    def timerThreadTimerSignal(self, emit_value):
        self.lineEditStart.setText(emit_value)

    def onPushButtonStopClicked(self):
        self.timerThread.status = False


class TimerThread(QtCore.QThread):

    timerSignal = QtCore.Signal(str)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.timerCount = None
        self.status = None

    def run(self) -> None:
        self.status = True

        if self.timerCount is None:
            self.timerCount = 10

        while self.status:
            if self.timerCount < 1:
                break

            time.sleep(1)
            self.timerCount -= 1
            self.timerSignal.emit(str(self.timerCount))


if __name__ == "__main__":
    app = QtWidgets.QApplication()

    myapp = MyApp()
    myapp.show()

    app.exec_()
