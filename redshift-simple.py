from __future__ import division
from subprocess import check_output
from os import system
from sys import exit, argv
from PySide.QtGui import QApplication, QSystemTrayIcon, QIcon, QAction, QMenu
from PySide.QtGui import QWidget, QDesktopWidget, QMessageBox, QFont


class Window(QWidget):
    def __init__(self):
        super(Window, self).__init__()
        self.center()
        self.setWindowIcon(QIcon('images/favicon.png'))

    def msgApp(self, title, msg):
        uinfo = QMessageBox.question(self, title,
                                     msg, QMessageBox.Yes | QMessageBox.No)
        if uinfo == QMessageBox.Yes:
            return 'y'
        if uinfo == QMessageBox.No:
            return 'n'

    def exitIT(self, event=None):
        response = self.msgApp(
            "Making sure",
            "Do youn want to restore screen color to default, before exiting ?")
        if response == 'y':
            system("redshift -x &> /dev/null")
        else:
            exit(0)

    def redshiftMissing(self):
        msgg = "<center>"
        msgg += " Error, Could not find Redshift command. Install it from your"
        msgg += " package manager or from "
        msgg += "<a href='https://github.com/jonls/redshift'> Redshift</a>"
        msgg += "</center>"
        mm = QMessageBox.critical(
            self,
            "Critical Error",
            msgg,
            QMessageBox.Ok)
        exit(0)

    def center(self):
        qrect = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qrect.moveCenter(cp)
        self.move(qrect.topLeft())


class redshiftSimple(QSystemTrayIcon):
    def __init__(self, parent):
        super(redshiftSimple, self).__init__()
        self.parent = parent
        self.menu = QMenu(parent)
        self.On = True
        self.CM = 4000
        if not self.isRedshift():
            parent.redshiftMissing()
        self.perLabel = QAction(self.getIT(), self)
        self.perLabel.setFont(QFont("", 13))
        self.perLabel.setEnabled(False)
        self.setIT(self.CM)
        self.setIcon(QIcon('images/favicon.png'))
        self.setToolTip("redshift-simple (Right\Left-Click)")
        self.onAction = QAction("On", self)
        self.onAction.setEnabled(False)
        self.offAction = QAction("Off", self)
        self.onAction.triggered.connect(self.onToggle)
        self.offAction.triggered.connect(self.onToggle)
        self.activated.connect(self.toggleP)
        self.increseAction = QAction("Increase", self)
        self.increseAction.triggered.connect(self.increse)
        self.decreseAction = QAction("Decrease", self)
        self.decreseAction.triggered.connect(self.decrese)
        self.exitAction = QAction("Exit", self)
        self.exitAction.triggered.connect(self.exitIT)
        self.menu.addAction(self.perLabel)
        self.menu.addSeparator()
        self.menu.addAction(self.onAction)
        self.menu.addAction(self.offAction)
        self.menu.addSeparator()
        self.menu.addAction(self.increseAction)
        self.menu.addAction(self.decreseAction)
        self.menu.addSeparator()
        self.menu.addAction(self.exitAction)
        self.setContextMenu(self.menu)

    def onToggle(self):
        if self.On is None:
            self.On = True
            self.onAction.setEnabled(False)
            self.offAction.setEnabled(True)
            self.increseAction.setEnabled(True)
            self.decreseAction.setEnabled(True)
            self.setIT(self.CM)
        else:
            self.On = None
            self.onAction.setEnabled(True)
            self.offAction.setEnabled(False)
            self.increseAction.setEnabled(False)
            self.decreseAction.setEnabled(False)
            system("redshift -x &> /dev/null")

    def toggleP(self, ar):
        if ar != QSystemTrayIcon.ActivationReason.Context:
            self.onToggle()

    def exitIT(self):
        if self.On is not None and self.CM < 6500:
            return self.parent.exitIT()
        exit(0)

    def increse(self):
        if self.CM >= 6500:
            self.CM = 5500
        if self.CM <= 1000:
            self.CM = 2000
        self.CM += 1000
        return self.setIT(self.CM)

    def decrese(self):
        if self.CM >= 6500:
            self.CM = 5500
        if self.CM <= 1000:
            self.CM = 2000
        self.CM -= 1000
        self.setIT(self.CM)

    def setIT(self, value):
        self.perLabel.setText(self.getIT())
        system("redshift -O " + str(value) + " &> /dev/null")

    def getIT(self):
        return str(int((self.CM / 6500) * 100)) + "%"

    def isRedshift(self):
        """ Check if redshift does exist or not """
        try:
            redshift = str(check_output(['whereis', '-b', 'redshift']))
            redshift = redshift.split(':')[1][1:]
            if len(redshift) < 4:
                return False
            return True
        except:
            return False


if __name__ == '__main__':
    app = QApplication(argv)
    fwindow = Window()
    window = redshiftSimple(fwindow)
    window.show()
    exit(app.exec_())
