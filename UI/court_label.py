"""Version 0.6_Last Updated 20171123"""
import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5 import uic

from UI.court_dialog import *
from UI.court_set_dialog import *
from UI.court_end_dialog import *


class CourtLabel():
    """
    Class Info :Dialog about Single class for each buttons and control about it
                for describing courts at GraphicUi.py

    Class Variables : dialog, match, courtNum, waitings, mainWin, button

    Class Functions :
        Internal Functions : __init__(courtNum, window, waitingGames, size=(50, 75), point=9),
                        setMatch(match), dialogUpdate(), checkEnd(), finishMatch()

            __init__(courtNum, window, waitingGames, size=(50, 75), point=9) :
                Initiate class. able to set size and point of letters of button
            setMatch(match) : connect self.match with given match
            dialogUpdate() : update self.dialog
            checkEnd() : confirm end of the match
            finishMatch() : set editlock and reset court

        Public Functions : move(), show(), hide(), popup(), updateDesign()
            popup() : show popup about the court
                -if has no connected Match : pop CourtSetDialog and connect next match
                    --connections : change text about court, update mainWin.waitingmatches
                -if has connectedMatch : show self.dialog(=CourtDialog Class)

    """

    def __init__(self, courtNum, window, waitingGames, size=(50, 75), point=9):
        self.match=None
        self.courtNum=courtNum
        self.waitings=waitingGames
        self.mainWin=window
        self.dialog=CourtDialog(self.match, self.courtNum, self.mainWin)
        self.button=QPushButton()
        self.setLabel()
        self.button.clicked.connect(self.popup)
        self.updateDesign(size=size, point=point)

    def updateDesign(self, size=(50, 75), point=9):
        self.button.setFixedSize(size[0]+10, size[1]+30)
        font=QFont()
        font.setPointSize(point)
        self.button.setFont(font)


    def move(self, grid, x, y):
        grid.addWidget(self.button, x, y)

    def show(self):
        self.button.show()

    def hide(self):
        self.button.hide()

    def popup(self):
        # self.dia=QMessageBox()
        # self.dia.about(self.dia,"Court Popup", "Court Popup about Court {0}".\
        #                                     format(self.courtNum))
        if self.match is None:
            self.setDia=CourtSetDialog(self.waitings, self.courtNum)
            # self.setDia.show()
            if self.setDia.exec_():
                self.setMatch(self.setDia.selectedMatch)
                self.setLabel()
        else:
            self.dialog.match=self.match
            self.dialog.exec_()
        self.mainWin.update(self.mainWin.presentRoot)
        self.setLabel()

    def setMatch(self, match):
        self.match=match
        self.dialogUpdate()
        self.dialog.endMatchB.clicked.connect(self.checkEnd)

    def dialogUpdate(self):
        if self.match is None:
            self.dialog=CourtDialog(self.courtNum, self.mainWin)
        else:
            self.dialog.match=self.match
            self.dialog.setLabel()

    def setLabel(self):
        self.button.setText("Court{0}\nMatch{1}".format\
        (self.courtNum, ("-" if self.match==None else self.match.matchNum))
        +("" if self.match is None else "\n{0}({1})\nvs\n{2}({3})".format(\
        self.match.player[0].name[:3], self.match.score[0], self.match.player[1].name[:3], \
        self.match.score[1])))

    def checkEnd(self):
        self.checkDia=CourtEndDialog()
        self.checkDia.player1Name.setText("현재 경기의 정보는 다음과 같습니다\n\
        Match #{matchnum}\nPlayer: {ply1}:{ply2}\nScore : {scr1}:{scr2}".format(\
        matchnum=self.match.matchNum, ply1=self.match.player[0].name, ply2=self.match.player[1].name,\
        scr1=self.match.score[0], scr2=self.match.score[1]))
        if self.checkDia.exec_():
            if self.match.score[0]!=self.match.score[1]:
                self.finishMatch()
                self.dialog.hide()
            else:
                self.dia=QMessageBox()
                self.dia.about(self.dia,"Error","Two Players Has Same Score!!")


    def finishMatch(self):
        self.match.editLock=True
        self.dialog.endMatchB.disconnect()
        up=self.match.upperMatch
        if up.underMatch[0]==self.match:
            self.match.winner=self.match.player[0] if self.match.score[0]>self.match.score[1] else self.match.player[1]
            self.match.loser=self.match.player[0] if self.match.score[0]<self.match.score[1] else self.match.player[1]
            up.player[0]=self.match.winner
        else:
            self.match.loser=self.match.player[0] if self.match.score[0]>self.match.score[1] else self.match.player[1]
            self.match.winner=self.match.player[0] if self.match.score[0]<self.match.score[1] else self.match.player[1]
            up.player[1]=self.match.winner

        self.match=None
        self.mainWin.update(self.mainWin.presentRoot)
        self.setLabel()
