"""Version 0.6_Last Updated 20171123"""
import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5 import uic
from UiCompile import *

matchlevel=["결승", "4강", "8강", "16강", "32강", "64강", "128강"]

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
        self.button=QDoublePushButton("{0}({1})\n{2}\nvs\n{3}".\
                        format(matchlevel[match.depth], match.matchNum, name1, name2), window)

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
        if mat._hasBye():
            self.dia.about(self.dia, "Match Popup", "{0} got bye"\
            .format(mat.player[0].nickName(self.mainWin.schoolDic)))

        elif mat.isReady()==3:
            self.dia.about(self.dia, "Match Popup", "Match {0} is not yet ready".format(mat.matchNum))

        elif mat.isReady()!=0:
            udm=mat.underMatch[mat.isReady()-1]
            self.dia.about(self.dia, "Match Popup", "Match {0} is not yet ready\nMatch {1}({2} vs. {3}) Winner\n\
            Will have match with {4}".format(mat.matchNum, udm.matchNum, udm.player[0].nickName(self.mainWin.schoolDic),\
            udm.player[1].nickName(self.mainWin.schoolDic), mat.player[mat.isReady()%2].nickName(self.mainWin.schoolDic)))

        else:
            self.dia.about(self.dia,"Match Popup",
            "Match Popup about Match {0}\n{1}({2}) : ({3}){4}"\
            .format(mat.matchNum, mat.player[0].nickName(self.mainWin.schoolDic),mat.score[0],\
            mat.score[1], mat.player[1].nickName(self.mainWin.schoolDic)))



class CourtDialog(Ui_InfoDialog, QDialog):
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


class CourtSetDialog(Ui_CourtSetDialog, QDialog):
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

class CourtEndDialog(Ui_EndCheckDialog, QDialog):
    """
    Class Info : Check up dialog for finishing up the match


    Class Variables :

    Class Functions :
        Internal Functions : __init__()

            __init__() : Initiate class.

        Public Functions :

    """
    def __init__(self):
        super().__init__()
        self.setupUi(self)

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
        self.button=QPushButton("Court{0}\n\nMatch{1}".\
                        format(self.courtNum, ("-" if self.match==None else self.match.matchNum)))
        self.button.clicked.connect(self.popup)
        self.button.setFixedSize(size[0], size[1])
        font=QFont()
        font.setPointSize(point)
        self.button.setFont(font)

    def updateDesign(self, size=(50, 75), point=9):
        self.button.setFixedSize(size[0], size[1])
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
                self.button.setText("Court{0}\n\nMatch{1}".\
                format(self.courtNum, ("-" if self.match==None else self.match.matchNum)))

                self.mainWin.update(self.mainWin.presentRoot)
        else:
            self.dialog.match=self.match
            self.dialog.show()

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
        print("Match{0} Locked".format(self.match.matchNum))
        self.dialog.endMatchB.disconnect()
        up=self.match.upperMatch
        if up.underMatch[0]==self.match:
            up.player[0]=self.match.player[0] if self.match.score[0]>self.match.score[1] else self.match.player[1]
        else:
            up.player[1]=self.match.player[0] if self.match.score[0]>self.match.score[1] else self.match.player[1]

        self.match=None
        self.mainWin.update(self.mainWin.presentRoot)

        self.button.setText("Court{0}\n\nMatch{1}".\
        format(self.courtNum, ("-" if self.match==None else self.match.matchNum)))
