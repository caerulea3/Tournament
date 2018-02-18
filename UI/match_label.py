"""Version 0.6_Last Updated 20171123"""
import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5 import uic



class QDoublePushButton(QPushButton):
    doubleClicked = pyqtSignal()
    clicked = pyqtSignal()

    def __init__(self, *args, **kwargs):
        QPushButton.__init__(self, *args, **kwargs)
        self.timer = QTimer()
        self.timer.setSingleShot(True)
        self.timer.timeout.connect(self.clicked.emit)
        super().clicked.connect(self.checkDoubleClick)

    @pyqtSlot()
    def checkDoubleClick(self):
        if self.timer.isActive():
            self.doubleClicked.emit()
            self.timer.stop()
        else:
            self.timer.start(250)


matchlevel=["결승", "4강", "8강", "16강", "32강", "64강", "128강"]

class MatchLabel():
    """
    Class Info :Dialog about Single class for each buttons and control about it
                for describing tournaments at GraphicUi.py

    Class Variables : button, connectedMatch, mainWin
            mainWin : parent object to draw - usually MainUI, used to initiate button

    Class Functions :
        Internal Functions : __init__(self, match, window, size=(50, 75), point=9)

            __init__(self, match, window) : Initiate class.
                able to set size and point of letters of button

        Public Functions : move(grid), show(), hide(), popup()
            move(grid) : add widget to given grid
            popup() : make and show QMessageBox about the match

    """
    def __init__(self, match, window, size=(50, 75), point=9):
        name1=match.player[0].name[7:] if match.player[0].name.startswith("Match") \
                                        else match.player[0].name
        name2=match.player[1].name[7:] if match.player[1].name.startswith("Match") \
                                        else match.player[1].name
        self.button=QDoublePushButton("{0}({1})\n{2}({3})\nvs\n{5}({4})".\
                        format(matchlevel[match.depth], match.matchNum, \
                        name1[:4], match.score[0], match.score[1], name2[:4]), window)

        self.button.setFixedSize(size[0], size[1])
        font=QFont()
        font.setPointSize(point)
        self.button.setFont(font)
        self.connectedMatch=match
        self.mainWin=window
        self.linkedMatch=None
        self.button.doubleClicked.connect(lambda : window.tourDraw(self.linkedMatch))

    def move(self, grid, x, y):
        grid.addWidget(self.button, x, y)

    def show(self):
        self.button.show()

    def hide(self):
        self.button.hide()

    def popup(self):
        self.dia=QMessageBox()
        mat=self.connectedMatch
        self.dia.about(self.dia, "Match Information", self.mainWin._printMatchInfo(mat))
