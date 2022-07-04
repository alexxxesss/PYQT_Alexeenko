import time

from PySide6 import QtCore, QtWidgets

from ui.practice_form_design import Ui_Form


class QThreadPractice(QtWidgets.QWidget):

    def __init__(self, parent=None):
        super().__init__(parent)

        self.ui = Ui_Form()
        self.ui.setupUi(self)

        self.initUi()
        self.initThreads()

    def initThreads(self):
        self.timerThread = TimerThread()
        self.timerThread.timerSignal.connect(self.timerThreadTimerSignal)
        self.timerThread.started.connect(self.timerThreadStarted)
        self.timerThread.finished.connect(self.timerThreadFinished)

    def initUi(self):
        self.setWindowTitle("3 практика")

        self.ui.pushButtonStartTimer.clicked.connect(self.onPushButtonStartTimer)
        self.ui.pushButtonStopTimer.clicked.connect(self.onPushButtonStopTimer)

    def onPushButtonStartTimer(self):

        self.timerThread.timerCount = self.ui.spinBoxTimerCount.value()
        if self.timerThread.timerCount == 0:
            QtWidgets.QMessageBox.warning(self, "Внимание", "Выберите значение")
        self.timerThread.start()

    def onPushButtonStopTimer(self):

        self.timerThread.status = False

    def timerThreadTimerSignal(self, emit_value):
        self.ui.lineEditTimerEnd.setText(emit_value)

    def timerThreadStarted(self):
        self.ui.pushButtonStartTimer.setEnabled(False)
        self.ui.pushButtonStartTimer.setEnabled(True)
        self.ui.lineEditTimerEnd.setEnabled(False)

    def timerThreadFinished(self):
        self.ui.pushButtonStopTimer.setEnabled(False)
        self.ui.pushButtonStopTimer.setEnabled(True)
        self.ui.lineEditTimerEnd.setEnabled(True)
        self.ui.lineEditTimerEnd.setText("")
        QtWidgets.QMessageBox.about(self, "Ура!!!", "Отсчет закончен!")

class TimerThread(QtCore.QThread):

    timerSignal = QtCore.Signal(str)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.timerCount = None
        self.status = None

    def run(self) -> None:
        self.status = True

        while self.status:
            if self.timerCount < 1:
                break

            time.sleep(1)
            self.timerCount -= 1
            self.timerSignal.emit(str(self.timerCount))


if __name__ == "__main__":
    app = QtWidgets.QApplication()

    myapp = QThreadPractice()
    myapp.show()

    app.exec_()
