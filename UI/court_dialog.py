"""Version 0.6_Last Updated 20171123"""
import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from UI.UI_courtLabel import *

matchlevel=["결승", "4강", "8강", "16강", "32강", "64강", "128강"]

class CourtDialog(Ui_CourtInfo, QDialog):
    """
    Class Info : Class for showing up Information about each court
                    when court has match on it


    Class Variables : match

    Class Functions :
        Internal Functions : __init__(match), ply1up(), ply1down(), ply2up(), ply2down()

            __init__(match, courtNum) : Initiate class.

        Public Functions : setButton(), setLabel()

            setLabel() : update labels about match
            setButton() : Connect Buttons to each Function

    """
    def __init__(self, match, courtNum, mainWin):
        super().__init__()
        self.setupUi(self)
        self.match=match
        self.setButton()
        self.courtNum=courtNum
        self.mainWin=mainWin

    def setButton(self):
        self.player1Up.clicked.connect(self.ply1up)
        self.player1Down.clicked.connect(self.ply1down)
        self.player2Up.clicked.connect(self.ply2up)
        self.player2Down.clicked.connect(self.ply2down)

    def ply1up(self):
        if self.match is not None and self.match.score[0]<7:
            self.match.score[0]+=1
            self.setLabel()

    def ply1down(self):
        if self.match is not None and self.match.score[0]>0:
            self.match.score[0]-=1
            self.setLabel()

    def ply2up(self):
        if self.match is not None and self.match.score[1]<7:
            self.match.score[1]+=1
            self.setLabel()

    def ply2down(self):
        if self.match is not None and self.match.score[1]>0:
            self.match.score[1]-=1
            self.setLabel()

    def setLabel(self):
        if self.match is not None:
            self.courtInfo.setText("Court {0} Information\nMatch {1}({2})".\
            format(self.courtNum, self.match.matchNum, matchlevel[self.match.depth]))
            self.player1Name.setText("Player 1 : \n{0}"\
            .format(self.match.player[0].nickName(self.mainWin.schoolDic)))
            self.player2Name.setText("Player 2 : \n{0}"\
            .format(self.match.player[1].nickName(self.mainWin.schoolDic)))
            self.player1Score.setText("Player 1 Score : {0}"\
            .format(self.match.score[0]))
            self.player2Score.setText("Player 2 Score : {0}"\
            .format(self.match.score[1]))
