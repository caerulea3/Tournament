"""Version 0.6_Last Updated 20171123"""
import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5 import uic


class CourtButton():
    """Basic Design"""
    def __init__(self, root, court, size=(50, 75), point=9):
        self.root=root
        self.button=QPushButton(root.mainwin)
        self.button.clicked.connect(self.popup)
        self.size=size
        self.point=point
        self.updateDesign(newsize=size, newpoint=point)
        self.court=court

    def setlabel(self):
        self.button.setText(self.root.askcourtlabel(self))

    def updateDesign(self, newsize=None, newpoint=None):
        if newsize is not None:
            self.size=newsize
        if newpoint is not None:
            self.point=newpoint

        self.button.setFixedSize(self.size[0]+10, self.size[1]+30)
        font=QFont()
        font.setPointSize(self.point)
        self.button.setFont(font)

    def court(self):
        return self.court

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
        if self.court.empty():
            self.setDia=CourtSetDialog(self.root, self)
            self.setDia.show()
            self.setDia.exec_()
            self.setlabel()
        else:
            self.courtDia=CourtDialog(self.root, self)
            self.courtDia.show()
            self.courtDia.exec_()
            self.setlabel()
        self.root.mainwin.updateallui()

    """Match Functions"""

csform=uic.loadUiType("./ui10/UI_CourtSetDialog.ui")[0]
class CourtSetDialog(QDialog, csform):
    def __init__(self, root, courtbut):
        super().__init__()
        self.setupUi(self)
        self.root=root
        self.update_waitingtable()
        self.courtbut=courtbut
        self.singlesetB.clicked.connect(self.setSingles)
        self.doublesetB.clicked.connect(self.setDoubles)

    def update_waitingtable(self):
        self.singlewaiting.clear()
        self.singlewaiting.setColumnCount(5)
        # waitingArray=waitingmatches(self.root.SingleRoot)
        waitingArray=self.root.waiting_tableform(single=True)
        self.singlewaiting.setRowCount(len(waitingArray))
        self.singlewaiting.setHorizontalHeaderLabels(["Match Level", "Player1", "player2", "UpperMatch", "MatchNum"])
        for s in waitingArray:
            for j in range(5):
                self.singlewaiting.setItem(waitingArray.index(s), j, \
                    QTableWidgetItem(s[j]))

        self.doublewaiting.clear()
        self.doublewaiting.setColumnCount(5)
        # waitingArray=waitingmatches(self.root.SingleRoot)
        waitingArray=self.root.waiting_tableform(single=False)
        self.doublewaiting.setRowCount(len(waitingArray))
        self.doublewaiting.setHorizontalHeaderLabels(["Match Level", "Player1", "player2", "UpperMatch", "MatchNum"])
        for s in waitingArray:
            for j in range(5):
                self.doublewaiting.setItem(waitingArray.index(s), j, \
                    QTableWidgetItem(s[j]))

    def setSingles(self):
        if self.singlewaiting.selectedIndexes()==[]:
            self.done(0)
            return
        idx=self.singlewaiting.selectedIndexes()[0].row()
        match=self.root.waitingmatches(self.root.SingleRoot)[idx]
        self.courtbut.court.setgame(match)
        self.done(1)

    def setDoubles(self):
        if self.doublewaiting.selectedIndexes()==[]:
            self.done(0)
            return
        idx=self.doublewaiting.selectedIndexes()[0].row()
        match=self.root.waitingmatches(self.root.DoubleRoot)[idx]
        self.courtbut.court.setgame(match)
        self.done(1)

cdform=uic.loadUiType("./ui10/UI_courtLabel.ui")[0]
matchlevel=["결승", "4강", "8강", "16강", "32강", "64강", "128강"]
class CourtDialog(cdform, QDialog):
    """
    Class Info : Class for showing up Information about each court
                    when court has match on it


    Class Variables : root, courtbut, courtnum, court, match

    Class Functions :
        Internal Functions : __init__(match), ply1up(), ply1down(), ply2up(), ply2down()

            __init__(match, courtNum) : Initiate class.

        Public Functions : setButton(), setLabel()

            setLabel() : update labels about match
            setButton() : Connect Buttons to each Function

    """
    def __init__(self, root, courtbut):
        super().__init__()
        self.setupUi(self)
        self.root=root
        self.courtbut=courtbut
        self.match=self.courtbut.court.match
        self.courtNum=self.courtbut.court.courtnum
        self.setButton()
        self.setLabel()

    def setButton(self):
        self.player1Up.clicked.connect(self.ply1up)
        self.player1Down.clicked.connect(self.ply1down)
        self.player2Up.clicked.connect(self.ply2up)
        self.player2Down.clicked.connect(self.ply2down)
        self.endMatchB.clicked.connect(self.matchend)
        self.cancelB.clicked.connect(self.cancel_matchset)

    def ply1up(self):
        if self.match.score[0]<7:
            self.match.score[0]+=1
            self.setLabel()

    def ply1down(self):
        if self.match.score[0]>0:
            self.match.score[0]-=1
            self.setLabel()

    def ply2up(self):
        if self.match.score[1]<7:
            self.match.score[1]+=1
            self.setLabel()

    def ply2down(self):
        if self.match.score[1]>0:
            self.match.score[1]-=1
            self.setLabel()

    def setLabel(self):
        if self.match is not None:
            self.courtInfo.setText("Court {0} Information\nMatch {1}({2})".\
            format(self.courtNum, self.match.matchNum, matchlevel[self.match.depth()]))
            self.player1Name.setText("Player 1 : \n{0}"\
            .format(self.match.player[0].name('schoollong'))),
            self.player2Name.setText("Player 2 : \n{0}"\
            .format(self.match.player[1].name('schoollong'))),
            self.player1Score.setText("Player 1 Score : {0}"\
            .format(self.match.score[0])),
            self.player2Score.setText("Player 2 Score : {0}"\
            .format(self.match.score[1]))

    def cancel_matchset(self):
        reply = QMessageBox.question(QMessageBox(),  "Cancel Confirmation", \
            "{0}번 코트를 정말로 비우시겠습니까? 현재 진행중인 경기는 초기화됩니다.".\
            format(self.courtNum), QMessageBox.Yes, QMessageBox.No)

        if reply==QMessageBox.Yes:
            self.match.score=[0, 0]
            self.courtbut.court.match=None
            self.courtbut.match=None
            self.courtbut.setlabel()
            self.done(2)

    def matchend(self):
        check=CourtEndDialog()
        check.label1.setText("현재 경기의 정보는 다음과 같습니다\n\
        Match #{matchnum}\nPlayer: {ply1}:{ply2}\nScore : {scr1}:{scr2}".format(\
        matchnum=self.match.matchNum, ply1=self.match.player[0].name, ply2=self.match.player[1].name,\
        scr1=self.match.score[0], scr2=self.match.score[1]))
        reply=check.exec_()
        if reply==1:
            self.courtbut.court.clear_court()
            self.done(0)
        else:
            self.done(1)

edform=csform=uic.loadUiType("./ui10/UI_courtEndDialog.ui")[0]
class CourtEndDialog(edform, QDialog):
    def __init__(self   ):
        super().__init__()
        self.setupUi(self)
        self.yesB.clicked.connect(self.yes)
        # self.noB.clicked.connect(self.no)

    def yes(self):
        self.done(1)

    def no(self):
        self.done(0)

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

class MatchButton():
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
    def __init__(self, root, match, size=(50, 75), point=9):
        self.root=root
        self.button=QDoublePushButton(self.root.mainwin)
        self.button.setText("{0}({1})\n{2}({3})\nvs\n{5}({4})".\
                        format(matchlevel[match.depth()], match.matchNum, \
                        match.player[0].name(), match.score[0], \
                        match.score[1], match.player[1].name()))

        self.button.setFixedSize(size[0], size[1])
        font=QFont()
        font.setPointSize(point)
        self.button.setFont(font)

        self.connectedMatch=match
        self.mainWin=self.root.mainwin
        self.linkedMatch=None
        self.button.doubleClicked.connect\
            (lambda : self.root.mainwin.tourdraw(self.linkedMatch))

    def move(self, grid, x, y):
        grid.addWidget(self.button, x, y)

    def show(self):
        self.button.show()

    def hide(self):
        self.button.hide()

    def popup(self):
        self.dia=QMessageBox()
        mat=self.connectedMatch
        self.dia.about(self.dia, "Match Information", \
            "self.mainWin._printMatchInfo(mat)")
