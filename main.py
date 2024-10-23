import sys

from PyQt5.QtWidgets import QApplication, QWidget
from PyQt5 import uic, QtCore, QtTest
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import QThread

from TOTP import *
from time import sleep

class AddCode(QThread):
    def __init__(self, name:str, secret:str):
        QThread.__init__(self)
        self.name = name
        self.secret = secret

    def run(self):
        if self.secret != "_":
            ACCOUNT_ADD(self.name, self.secret)
        else:
            ACCOUNT_REMOVE(self.name)

class ShowCodes(QThread):
    codesShow = QtCore.pyqtSignal(str)
    def __init__(self):
        QThread.__init__(self)

    def run(self):
        while True:
            LIST = ""
            CODEs = SHOW_ALL_CODES()
            if CODEs != None:
                for label, key in sorted(list(CODEs.items())):
                    try:
                        LIST += (f"{label}: {get_totp_token(key)}\n")
                    except:
                        LIST += (f"{label}: ______\n")
            else:
                pass
            self.codesShow.emit(f"{LIST}")
            sleep(0.1)

class App(QWidget):
    def __init__(self):
        QWidget.__init__(self)
        self.set()

    def set(self):
        self.w_root = uic.loadUi('root.ui', self)
        self.runShow()
        self.pushButton.clicked.connect(self.runFunc)
        self.w_root.show()

    def setTextBrowser(self, val):
        self.w_root.textBrowser.setText(val)

    def runShow(self):
        self.ShowCODE = ShowCodes()
        self.ShowCODE.codesShow.connect(self.setTextBrowser)
        self.ShowCODE.start()

    def runFunc(self):
        try:
            name = str(self.nameEdit.text())
            secret = str(self.secretEdit.text())
            if name == "" or secret == "":
                raise ValueError
            self.AddCODE = AddCode(name, secret)
            self.AddCODE.start()
        except:
            pass

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    app.exec_()