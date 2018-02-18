import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5 import uic
from root import Root
from ui10.buttons import MatchButton, CourtButton
from dirtyfunctions import WrongActError

form_class = uic.loadUiType("./ui10/UI_MainWindow.ui")[0]

class MainWindow(QMainWindow, form_class):
    def __init__(self, root=None):
        super().__init__()
        self.setupUi(self)
        self.root=Root() if root is None else root
        self.root.setmainwin(self)
        """Match Control"""
        self.focus_single=False
        self.focusedmatch=None
        self.URL=None

        """Design"""
        self.tourbuttons=[]
        self.courtbuttons=[]
        self.buttonsize=(75, 75)
        self.pointsize=9
        self.drawdepth=4

        self.testB.clicked.connect(self.test)

        self.saveB.clicked.connect(self.saveFile)
        self.openB.clicked.connect(self.openFile)
        self.googleB.clicked.connect(self.googlesave)

        self.updateallui()

    def saveFile(self):
        dia=QFileDialog()
        filepath = dia.getSaveFileName(self)[0]
        if filepath!="":
            try:
                self.root.save(filepath)
            except:
                print("Error")

    def openFile(self):
        if len(sys.argv)!=2:
            dia=QFileDialog()
            filepath = dia.getOpenFileName(self)[0]
        if filepath!="":
            try:
                self.root.load(filepath)
            except:
                print("Error")
        self.updateallui()

    def googlesave(self):
        dia=QInputDialog()
        if self.URL is not None:
            url, ok=dia.getText(self, "GoogleDocs Autosave Settings", \
            "Google Docs URL", QLineEdit.Normal, self.URL)
        else:
            url, ok=dia.getText(self, "GoogleDocs Autosave Settings", \
            "Google Docs URL")

        if ok:
            self.URL=url
            self.spreadSheetId=self.URL.split("/")[5]
            self.root.googlesave(self.spreadSheetId)

    def updateallui(self):
        self.root.start()
        target=None
        if self.root.SingleRoot is not None:
            target=self.root.SingleRoot
        if self.root.DoubleRoot is not None:
            target=self.root.DoubleRoot
        if self.focusedmatch is not None:
            target=self.focusedmatch
        if target is not None:
            self.tourdraw(target)
        self.courtdraw(len(self.root.Courts))
        self.update_waitingtable()

    def test(self):
        self.focusedmatch=self.root.DoubleRoot if self.focus_single else self.root.SingleRoot
        self.focus_single=False if self.focus_single else True
        self.updateallui()
        if self.courtbuttons==[]:
            self.courtdraw(14)

    def tourdraw(self, target):
        if target is None:
            return

        depth=self.drawdepth
        self.focusedmatch=target

        #remove all existing tourButtons
        for x in self.tourbuttons:
            x.hide()
        self.tourbuttons=[]

        #find all target matches to draw
        udm=self.focusedmatch.undermatches()
        targets=[]
        for m in udm:
            if m.depth()<self.focusedmatch.depth()+depth:
                targets.append(m)

        xpos=0
        for mat in targets:
            #draw every match
            ypos=mat.depth()-self.focusedmatch.depth()
            todraw=MatchButton(self.root, mat, size=self.buttonsize, point=self.pointsize)
            todraw.move(self.tourGrid, ypos, xpos)
            todraw.show()
            self.tourbuttons.append(todraw)
            xpos+=1

            #connect functions to tourButtons
            if mat.depth()==self.focusedmatch.depth():
                todraw.linkedMatch=self.root.SingleRoot if self.focus_single\
                                else self.root.DoubleRoot
            else:
                todraw.linkedMatch=mat
            todraw.button.clicked.connect(todraw.popup)
            # todraw.button.doubleClicked.connect(lambda : self.tourDraw(todraw.linkedMatch))
        if self.focusedmatch.underMatch==[]:
            self.tourdraw(self.focusedmatch.upperMatch)
        elif self.focusedmatch.underMatch[0].underMatch==[] or self.focusedmatch.underMatch[1].underMatch==[]:
            self.tourdraw(self.focusedmatch.upperMatch)

    def courtdraw(self, newcourtnum):
        for c in self.courtbuttons:
            c.hide()
        self.courtbuttons=[]

        try:
            self.root.changecourtnum(newcourtnum)
        except WrongActError as ex:
            QMessageBox.about(self, "WrongActError", ex)

        for i in range(len(self.root.Courts)):
            thisCourt=CourtButton(self.root, self.root.Courts[i],\
                                     self.buttonsize, self.pointsize)
            self.courtbuttons.append(thisCourt)
            thisCourt.move(self.courtGrid, i%2, i//2)
            thisCourt.setlabel()

    def update_waitingtable(self):
        self.singlewaiting.clear()
        self.singlewaiting.setColumnCount(5)
        # waitingArray=waitingmatches(self.root.SingleRoot)
        self.singlewaiting.setHorizontalHeaderLabels(["Match Level", "Player1", "player2", "UpperMatch", "MatchNum"])
        if self.root is not None and self.root.SingleRoot is not None:
            waitingArray=self.root.waiting_tableform(single=True)
            self.singlewaiting.setRowCount(len(waitingArray))
            for s in waitingArray:
                for j in range(5):
                    self.singlewaiting.setItem(waitingArray.index(s), j, \
                        QTableWidgetItem(s[j]))

        self.doublewaiting.clear()
        self.doublewaiting.setColumnCount(5)
        # waitingArray=waitingmatches(self.root.SingleRoot)
        self.doublewaiting.setHorizontalHeaderLabels(["Match Level", "Player1", "player2", "UpperMatch", "MatchNum"])
        if self.root is not None and self.root.DoubleRoot is not None:
            waitingArray=self.root.waiting_tableform(single=False)
            self.doublewaiting.setRowCount(len(waitingArray))
            for s in waitingArray:
                for j in range(5):
                    self.doublewaiting.setItem(waitingArray.index(s), j, \
                        QTableWidgetItem(s[j]))

if __name__ == "__main__":
    from games import Match
    app = QApplication(sys.argv)
    win = MainWindow()
    win.show()
    app.exec_()
