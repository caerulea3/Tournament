"""Version 0.7_Last Updated 20171123"""
# from System import fileControl, MedicalTennis, Tournament
from UI import UI_MainWindow
from UI.court_label import *
from UI.match_label import *
import sys

from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from MainWinInternal import MainWinInternal as internal
# from PyQt5.QtGui import *

from root import Root

class MainUI(QMainWindow, UI_MainWindow.Ui_TournamentController, internal):
    """
    Class Info :

    Class Variables : root, presentRoot, tourButtons, courtButtons, courtNum
                      schoolDic, buttonSize, pointSize, depth, matchSequence, waitingArray

    Connections :
        self.saveB.clicked                  - self.saveFile
        self.exitB.clicked                  - self.exit
        self.butSizeSlider.valueChanged     - self._setButtonSize
        self.depthSlider.valueChanged       - self._setDepth
        self.courtNumSlider.valueChanged    - self._setCourtNum
        self.fontSizeSlider.valueChanged    - self._setFontSize
        self.testB.clicked                  - self.testfunc
        self.findMatchB.clicked             - self.showFoundMatch
        self.versionShowB.clicked           - self.versionShow
        self.resetB.clicked                 - self.unLockMatch

    Class Functions :
        Internal Functions : __init__(self), _savefile(self, filepath), _openfile(self, filepath),
                            _setButtonSize(self), _setDepth(self), _setCourtNum(self), _setFontSize(self),
                             _setWaitingMatches(self), _showWaitingMatches(self), _getUnderMatchs(self, target, depth),
                            tourDraw(self, target), courtDraw(self), saveFile(self),
                            openFile(self), exit(self), versionShow(self), update(self, target),testfunc(self),

            __init__(self) :initialize function
            _savefile(self, filepath) : save file to filepath, called by openfile()
            _openfile(self, filepath) : open file from filepath, called by openfile()
            _setButtonSize(self) : change self.buttonsize, called by butSizeSlider.valueChanged
            _setDepth(self) : change self.depth, called by depthSlider.valueChanged
            _setCourtNum(self) : change self.courtNum, called by courtNumSlider
            _setWaitingMatches(self) : revise matches in matchSequence to self.waitingArray
                                        -make matchSequence if not existing
                                        -update CourtLabel.waitingMatches
            _showWaitingMatches(self) : update self.waitingMatches panel
            _getUnderMatchs(self, target, depth) : find underMatch of target until it gets under depth, in left->right order
            _findMatchRec(self, targetNum, cur) : private function for recursive programming of findMatch
            tourDraw(self, target) : draw tournament on ui
            courtDraw(self) : draw court on ui
            findMatch(self, targetNum) : find targetNum match and return the match. return None if there is no such match
            showFoundMatch(self) : function to get targetNum and find the match
            update(self, target) :
    """
    def __init__(self, root):
        super().__init__()
        self.setupUi(self)
        self._connectEvent()
        self._setVariables()
        self.root=root


    def saveFile(self):
        dia=QFileDialog()
        filepath = dia.getSaveFileName(self)[0]
        if filepath!="":
            self.root.save(filepath)

    def openFile(self):
        if len(sys.argv)!=2:
            dia=QFileDialog()
            filepath = dia.getOpenFileName(self)[0]
        elif sys.argv[1]=="debug":
            filepath="./testtour/test01_nonSimul.tor"
        elif sys.argv[1]=="simul":
            filepath="./testtour/test01_Simul.tor"
        if filepath!="":
            self.root.load(filepath)
            self.update(self.root)

    def exit(self):
        QCoreApplication.instance().quit()

    def versionShow(self):
        dia=QMessageBox(self)
        dia.about(self, "Version Information", "Version 0.7")

    def update(self, target):
        self._setWaitingMatches()
        self._showWaitingMatches()
        self.tourDraw(target)
        self.courtDraw()

    def testfunc(self):
        pass

    def tourDraw(self, target):
        if target is None:
            return
        depth=self.depth
        self.presentRoot=target
        #remove all existing tourButtons
        for x in self.tourButtons:
            x.hide()
        self.tourButtons=[]

        #find all target matches to draw
        targets=rt.rootmatch().undermatches(target, depth)
        xpos=0
        for mat in targets:
            #draw every match
            ypos=mat.depth-target.depth
            todraw=MatchLabel(mat, self, size=self.buttonSize, point=self.pointSize)
            todraw.move(self.tourGrid, ypos, xpos)
            todraw.show()
            self.tourButtons.append(todraw)
            xpos+=1

            #connect functions to tourButtons
            if mat.depth==target.depth:
                todraw.linkedMatch=self.root
            else:
                todraw.linkedMatch=mat
            todraw.button.clicked.connect(todraw.popup)
            # todraw.button.doubleClicked.connect(lambda : self.tourDraw(todraw.linkedMatch))
        if target.underMatch==[]:
            self.tourDraw(target.upperMatch)
        elif target.underMatch[0].underMatch==[] or target.underMatch[1].underMatch==[]:
            self.tourDraw(target.upperMatch)

    def courtDraw(self):
        pass
        # try:
        #     rt.changecourtnum(self.courtNum)
        # except WrongActError as ex:
        #     QMessageBox.about(self, "WrongActError", ex)
        #
        # if len(self.courtButtons)>self.courtNum:
        #     for court in self.courtButtons[self.courtNum:]:
        #         court.hide()
        #     self.courtButtons=self.courtButtons[:self.courtNum]
        #
        # elif len(self.courtButtons)<self.courtNum:
        #     for i in range(len(self.courtButtons), self.courtNum):
        #         thisCourt=CourtLabel(i+1, self, self.waitingArray, size=self.buttonSize, point=self.pointSize)
        #         thisCourt.move(self.courtGrid, i%2, i//2)
        #         self.courtButtons.append(thisCourt)
        #
        # for court in self.courtButtons:
        #     court.updateDesign(size=self.buttonSize, point=self.pointSize)

    def showFoundMatch(self):
        pass
        # dialogInput, ok = QInputDialog.getInt(self, '경기 검색', '검색할 경기 번호를 입력하십시오')
        # if ok:
        #     targetNum=dialogInput
        # else:
        #     return
        # found=self._findMatch(targetNum)
        # QMessageBox.about(self, "Found Match Information", \
        # self.textForFoundMatch(targetNum, found))

    def unLockMatch(self):
        pass
        # dialogInput, ok = QInputDialog.getInt(self, '경기 초기화', '초기화할 경기 번호를 입력하십시오')
        # if ok:
        #     targetNum=dialogInput
        # else:
        #     return
        # target=self._findMatch(targetNum)
        # if target is None:
        #     toshow="There is no match {0} in Tournament".format(targetNum)
        # else:
        #     qm = QMessageBox()
        #     ret=qm.question(self,"Reset Match Information",\
        #     self._unlockTargetInfo(target)+"초기화된 경기는 복구할 수 없습니다!!", qm.Yes | qm.No)
        #     if ret==qm.Yes:
        #         self._unLockMatchRec(target)
        #     else:
        #         pass
        # self.update(self.presentRoot)

    def findPlayer(self):
        pass
        # values=[]
        # for k in self.schoolDic.keys():
        #     values.append(self.schoolDic[k])
        # if values[-1]=="Bye":
        #     values=values[:-1]
        # dialogInput, ok = QInputDialog().getItem(self, "선수 검색", "검색할 선수의 학교를 선택하십시오", values, False)
        # if ok:
        #     target=dialogInput
        #     schoolCode=""
        #     for x in self.schoolDic.keys():
        #         if self.schoolDic[x]==target:
        #             schoolCode=x
        #     players=self._findSchoolPlayer(schoolCode)
        #     playerNames=[]
        #     realPlayers=[]
        #     for p in players:
        #         if p.nickName(self.schoolDic, type="fullname") not in playerNames:
        #             playerNames.append(p.nickName(self.schoolDic, type="fullname"))
        #             realPlayers.append(p)
        #     dialogInput, ok = QInputDialog().getItem(self, "선수 검색", "검색할 선수 이름을 선택하십시오", playerNames, False)
        #     if ok:
        #         lowestMatch=self._findPlayer(realPlayers[playerNames.index(dialogInput)].name, schoolCode)
        #         self._popupForFindPlayer(realPlayers[playerNames.index(dialogInput)].name, lowestMatch)


if __name__ == '__main__':
    app=QApplication(sys.argv)
    rt=Root()
    win=MainUI(rt)
    win.show()
    app.exec_()
