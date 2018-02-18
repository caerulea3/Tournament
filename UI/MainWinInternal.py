"""Version 0.7_Last Updated 20171123"""
# from System import *
from UI import UI_MainWindow
from UI.court_label import *
from UI.match_label import *
# from GoogleAPI import *
import sys
import operator

from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5 import uic
from root import Root

# from PyQt5.QtGui import *
COUNT=5
class MainWinInternal():
    def __init__(self):
        pass

    def _connectEvent(self):
        """Event Connect"""
        self.saveB.clicked.connect(self.saveFile)
        self.openB.clicked.connect(self.openFile)
        self.exitB.clicked.connect(self.exit)
        self.butSizeSlider.valueChanged.connect(self._setButtonSize)
        self.depthSlider.valueChanged.connect(self._setDepth)
        self.courtNumSlider.valueChanged.connect(self._setCourtNum)
        self.fontSizeSlider.valueChanged.connect(self._setFontSize)
        self.findMatchB.clicked.connect(self.showFoundMatch)
        self.resetB.clicked.connect(self.unLockMatch)
        self.findPlayerB.clicked.connect(self.findPlayer)
        self.autoSaveSettingB.clicked.connect(self._getAutosaveInfo)

    def _setVariables(self):
        """Variables"""
        self.presentRoot=self.root.rootmatch()
        self.tourButtons=[]
        self.courtButtons=[]
        self.courtNum=14

        self.schoolDic={}
        self.buttonSize=(70, 85)
        self.pointSize=9
        self.depth=4
        self.matchSequence=[]
        self.waitingArray=[]
        self.counter=-1
        self.URL=None
        self.spreadSheetId=None

    def _setButtonSize(self):
        val=self.butSizeSlider.value()
        self.buttonSize=(val*10, 50+val*5)
        self.update(self.presentRoot)

    def _setDepth(self):
        self.depth=self.depthSlider.value()
        self.update(self.presentRoot)

    def _setCourtNum(self):
        self.courtNum=self.courtNumSlider.value()
        self.update(self.presentRoot)

    def _setFontSize(self):
        self.pointSize=self.fontSizeSlider.value()
        self.update(self.presentRoot)

    def _printMatchInfo(self, target):
        if target._hasBye():
            info="Match {0} Information({lev}) :{1} got bye"\
            .format(target.matchNum, target.player[0].name('schoollong'),
            lev="결승" if target.depth()==0 else str(target.depth()**2)+"강")

        elif target.isReady()==0:
            info="Match {0} Information({lev}) : {1}({2}) : ({3}){4}"\
            .format(target.matchNum, target.player[0].name('schoollong'),target.score[0],\
            target.score[1], target.player[1].name('schoollong'), \
            lev="결승" if target.depth()==0 else str(target.depth()**2)+"강")

        elif target.isReady()!=3:
            udm=target.underMatch[target.isReady()-1]
            info="Match {0} Information({lev}) : Match {1}({2} vs. {3}) Winner vs {4}".format(\
            target.matchNum, udm.matchNum, udm.player[0].name('schoollong'),\
            udm.player[1].name('schoollong'), target.player[target.isReady()%2].name('schoollong')\
            , lev="결승" if target.depth()==0 else str(target.depth()**2)+"강")
        else:
            info="Match {0} Information({lev}) : Match {0} is not yet Ready".format(\
            target.matchNum, lev="결승" if target.depth()==0 else str(target.depth()**2)+"강")

        return info

    def _setWaitingMatches(self):
        pass
        # self.waitingArray=[]
        #
        # if self.matchSequence==[]:
        #     self.matchSequence=self.root.getMatchSequence()
        #
        # for i in range(0, len(self.matchSequence)):
        #     g=self.matchSequence[i]
        #     toappend=True
        #
        #     if g._hasBye():
        #         if g.upperMatch==None:
        #             pass
        #         elif g.upperMatch.underMatch[0]==g:
        #             g.winner=g.player[0]
        #             g.upperMatch.player[0]=g.player[0]
        #         else:
        #             g.winner=g.player[0]
        #             g.upperMatch.player[1]=g.player[0]
        #         g.editLock=True
        #
        #     if g.editLock==True:
        #         toappend=False
        #     else:
        #         for court in self.courtButtons:
        #             if court.match is None:
        #                 continue
        #             elif court.match.matchNum==g.matchNum:
        #                 toappend=False
        #     if toappend:
        #         self.waitingArray.append(g)
        #
        # for court in self.courtButtons:
        #     court.waitings=self.waitingArray


    def _showWaitingMatches(self):
        pass
        # self._setWaitingMatches()
        # self.waitingMatches.clear()
        # self.waitingMatches.setColumnCount(5)
        # self.waitingMatches.setRowCount(len(self.waitingArray))
        # self.waitingMatches.setHorizontalHeaderLabels(["Match Level", "Player1", "player2", "UpperMatch", "MatchNum"])
        #
        # for i in range(len(self.waitingArray)):
        #     g=self.waitingArray[i]
        #     items=[QTableWidgetItem(str(2**(g.depth+1))+"강" if g.depth!=0 else "결승"),\
        #      QTableWidgetItem(g.player[0].nickName(self.schoolDic, type="short")),\
        #      QTableWidgetItem(g.player[1].nickName(self.schoolDic, type="short")),\
        #      QTableWidgetItem("{2}->{1}->{0}".\
        #      format(g.upperMatch.matchNum if g.upperMatch is not None else "-", \
        #      g.upperMatch.upperMatch.matchNum if g.upperMatch is not None \
        #      and g.upperMatch.upperMatch is not None else "-", \
        #      g.upperMatch.upperMatch.upperMatch.matchNum if g.upperMatch is not None\
        #      and g.upperMatch.upperMatch is not None\
        #      and g.upperMatch.upperMatch.upperMatch is not None else "-")),\
        #      QTableWidgetItem(str(g.matchNum))]
        #
            # for j in range(5):
            #     self.waitingMatches.setItem(i, j, items[j])

    def _getUnderMatchs(self, target, depth):
        pass
        # if target is None:
        #     return []
        # targets=target.towrite()
        # ret=[]
        # for mat in targets:
        #     if (target.depth<=mat.depth) and (mat.depth<target.depth+depth):
        #         ret.append(mat)
        # return ret

    def _findMatchRec(self, targetNum, cur):
        pass
    #     if targetNum==cur.matchNum:
    #         return cur
    #     elif cur.underMatch==[]:
    #         return None
    #     else:
    #         left=self._findMatchRec(targetNum, cur.underMatch[0])
    #         right=self._findMatchRec(targetNum, cur.underMatch[1])
    #         if left is not None:
    #             return left
    #         elif right is not None:
    #             return right
    #         else:
    #             return None
    # def _findMatch(self, targetNum):
    pass
    #     target=self._findMatchRec(targetNum, self.root)
    #     if target is None:
    #         return None
    #     else:
    #         return target


    def textForFoundMatch(self, targetNum, found):
        pass
        # toshow=""
        # if found is None:
        #     toshow="There is no match {0} in Tournament".format(targetNum)
        # elif found==self.root:
        #     toshow="match {0} is Root".format(targetNum)
        # else:
        #     up=found
        #     route=""
        #     toshow=""
        #     while up is not None:
        #         route="->{0}".format(up.matchNum)+route
        #         up=up.upperMatch
        #     if found in self.waitingArray:
        #         toshow = "Route to Match : {0}\nMatch {1} is {2}{3} match on waiting\n".format(\
        #         route[2:], targetNum, \
        #         self.waitingArray.index(found)+1, \
        #         "st" if self.waitingArray.index(found)%10==0 else \
        #         ("nd" if self.waitingArray.index(found)%10==1 else "th"))
        #     else:
        #         toshow = "Route to Match : {0}\n".format(route[2:])
        #
        #     toshow+=self._printMatchInfo(found)
        #
        # return toshow

    def _unlockTargetInfo(self, target):
        pass
        # if target.editLock==False:
        #     return ""
        # else:
        #     resetLogInfo=self._unlockTargetInfo(target.upperMatch)
        #     resetLogInfo+=self._printMatchInfo(target)+"\n"
        #     return resetLogInfo

    def _unLockMatchRec(self, target):
        pass
        # if target.editLock==False:
        #     return []
        # else:
        #     resetLog=[]
        #     print(target.matchNum)
        #     target.editLock=False
        #     target.score=[0, 0]
        #     if target.upperMatch.underMatch[0]==target:
        #         target.upperMatch.player[0]=\
        #         target.upperMatch.playerType("#" + str(target.matchNum) + "Winner", 0)
        #     else:
        #         target.upperMatch.player[1]=\
        #         target.upperMatch.playerType("#" + str(target.matchNum) + "Winner", 0)
        #
        #     if target.upperMatch.editLock==True:
        #         resetLog=self._unLockMatchRec(target.upperMatch)
        #     resetLog.append(target)
        #     return resetLog


    def _findPlayer(self, target, schoolCode):
        pass
        # if self.matchSequence==[]:
        #     self.matchSequence=self.root.getMatchSequence()
        # for mat in self.matchSequence:
        #     if (target == mat.player[0].name and mat.player[0].school==schoolCode)\
        #     or (target == mat.player[1].name and mat.player[1].school==schoolCode):
        #         return mat
        # return None

    def _popupForFindPlayer(self, target, lowestMatch):
        pass
        # if lowestMatch is None:
        #     QMessageBox.about(self, "Found Player Information", \
        #     "player {0} is not in the tournament".format(target))
        # else:
        #     infoString=""
        #     route=""
        #     up=lowestMatch
        #     while up is not None:
        #         route="->{0}".format(up.matchNum)+route
        #         up=up.upperMatch
        #     cur=lowestMatch
        #     while target in cur.winner.name and cur.upperMatch is not None:
        #         infoString+="\n"+self._printMatchInfo(cur)
        #         cur=cur.upperMatch
        #     infoString+="\n"+self._printMatchInfo(cur)
        #     infoString="Route of Player : "+route[2:]+"\n"+infoString
        #     QMessageBox.about(self, "Found Player Information", \
        #     infoString)

    def _findSchoolPlayer(self, schoolCode):
        pass
        # players=[]
        # for g in self.matchSequence:
        #     if g.player[0].school==schoolCode:
        #         players.append(g.player[0])
        #     if g.player[1].school==schoolCode:
        #         players.append(g.player[1])
        #     players=sorted(players, key=operator.attrgetter('power'), reverse=True)
        # return players

    def _autoSave(self):
        pass
        # if self.counter==-1:
        #     pass
        # if self.counter!=COUNT:
        #     self.counter+=1
        # else:
        #     pass

    def _getAutosaveInfo(self):
        pass
        # dia=QInputDialog()
        # if self.URL is not None:
        #     url, ok=dia.getText(self, "GoogleDocs Autosave Settings", \
        #     "Google Docs URL", QLineEdit.Normal, self.URL)
        # else:
        #     url, ok=dia.getText(self, "GoogleDocs Autosave Settings", \
        #     "Google Docs URL")
        #
        # if ok:
        #     self.URL=url
        #     self.spreadSheetId=self.URL.split("/")[5]
        #     self._googleSheetWrite()

    def _googleSheetWrite(self):
        pass
        # googleconn=google(auth="rw")
        # googleconn.get_credentials()
        # googleconn.setSheetId(self.spreadSheetId)
        #
        # nodeHeight=7
        # count=1
        # games=self.root.towrite()
        # for x in games:
        #     startHeight=(nodeHeight * x.depth) + 2
        #     countToFormat=""
        #     thiscount=count
        #     while thiscount>25:
        #         countToFormat=chr(int(65+(thiscount%26)))+countToFormat
        #         thiscount=thiscount/26
        #     if count>=26:
        #         countToFormat=chr(int(64+(thiscount%26)))+countToFormat
        #     else:
        #         countToFormat=chr(int(65+(thiscount%26)))+countToFormat
        #     print(count, countToFormat)
        #     print(x.depth)
        #     count+=1
        #     rangeName = '{0}{1}:{0}{2}'.format(countToFormat, startHeight, startHeight+7)
        #     googleconn.addData(rangeName, \
        #     [
        #     ["Match #{0}".format(x.matchNum)],
        #     ['{0} Vs. {1}'.format(x.player[0].nickName(self.schoolDic), x.player[1].nickName(self.schoolDic))],
        #     ['Level : {0}'.format(matchlevel[x.depth])],
        #     ["Score : {0} : {1}".format(x.score[0], x.score[1])],
        #     ["UpperMatch : {0}".format(x.upperMatch.matchNum) if x.upperMatch is not None else ""],
        #     ["UnderMatch : {0}, {1}".format(x.underMatch[0].matchNum,
        #     x.underMatch[1].matchNum) if x.underMatch !=[] else ""],
        #     ["matchSequence : {0}".format(self.matchSequence.index(x)+1)]
        #     ])
        #
        # googleconn.updateData()
