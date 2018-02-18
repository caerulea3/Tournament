"""Version 0.6_Last Updated 20171123"""
import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5 import uic
from UI.UI_courtSetDialog import *

class CourtSetDialog(Ui_Dialog, QDialog):
    """
    Class Info :  Class for showing up Information about each court
                    when court don't has match on it, to conncet match with court


    Class Variables :

    Class Functions :
        Internal Functions : __init__(games, courtNum), setSelected()

            __init__(games, coutNum) : Initiate class. should give comming up games
                                usually give CourtLabel.waitings

        Public Functions :

    """
    def __init__(self, games, courtNum):
        super().__init__()
        self.setupUi(self)
        self.games=games
        self.courtNum=courtNum
        self.label.setText("Court {0}에 배정된 경기가 없습니다.\n\
        경기를 배정하십시오".format(self.courtNum))
        for i in range(min(10, len(games))):
            g=games[i]
            if g.isReady()==0 and not g._hasBye():
                self.waitingMatches.addItem("M.{0:03d}({1})\t{2}\tvs.  {3}\t{6}->{5}->{4}"\
                .format(g.matchNum, str(2**(g.depth+1))+"강" if g.depth!=0 else "결승", \
                g.player[0].name[:3], g.player[1].name[:3]\
                , g.upperMatch.matchNum if g.upperMatch is not None else "-", \
                g.upperMatch.upperMatch.matchNum if g.upperMatch is not None \
                and g.upperMatch.upperMatch is not None else "-", \
                g.upperMatch.upperMatch.upperMatch.matchNum if g.upperMatch is not None\
                and g.upperMatch.upperMatch is not None\
                and g.upperMatch.upperMatch.upperMatch is not None else "-"))
        self.selectedMatch=self.games[0] if len(games)!=0 else None
        self.waitingMatches.currentIndexChanged.connect(self.setSelected)

    def setSelected(self):
        self.selectedMatch=self.games[self.waitingMatches.currentIndex()]
