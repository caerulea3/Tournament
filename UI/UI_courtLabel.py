# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui\UI_courtLabel.ui'
#
# Created by: PyQt5 UI code generator 5.6
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_CourtInfo(object):
    def setupUi(self, CourtInfo):
        CourtInfo.setObjectName("CourtInfo")
        CourtInfo.resize(492, 309)
        self.buttonBox = QtWidgets.QDialogButtonBox(CourtInfo)
        self.buttonBox.setGeometry(QtCore.QRect(120, 240, 341, 32))
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.courtInfo = QtWidgets.QLabel(CourtInfo)
        self.courtInfo.setGeometry(QtCore.QRect(80, 30, 141, 51))
        self.courtInfo.setObjectName("courtInfo")
        self.player1Name = QtWidgets.QLabel(CourtInfo)
        self.player1Name.setGeometry(QtCore.QRect(80, 90, 141, 51))
        self.player1Name.setObjectName("player1Name")
        self.player2Name = QtWidgets.QLabel(CourtInfo)
        self.player2Name.setGeometry(QtCore.QRect(280, 90, 141, 51))
        self.player2Name.setObjectName("player2Name")
        self.player1Score = QtWidgets.QLabel(CourtInfo)
        self.player1Score.setGeometry(QtCore.QRect(80, 160, 141, 61))
        self.player1Score.setObjectName("player1Score")
        self.player1Up = QtWidgets.QPushButton(CourtInfo)
        self.player1Up.setGeometry(QtCore.QRect(220, 170, 21, 21))
        self.player1Up.setObjectName("player1Up")
        self.player1Down = QtWidgets.QPushButton(CourtInfo)
        self.player1Down.setGeometry(QtCore.QRect(220, 190, 21, 21))
        self.player1Down.setObjectName("player1Down")
        self.player2Score = QtWidgets.QLabel(CourtInfo)
        self.player2Score.setGeometry(QtCore.QRect(280, 160, 141, 61))
        self.player2Score.setObjectName("player2Score")
        self.player2Up = QtWidgets.QPushButton(CourtInfo)
        self.player2Up.setGeometry(QtCore.QRect(420, 170, 21, 21))
        self.player2Up.setObjectName("player2Up")
        self.player2Down = QtWidgets.QPushButton(CourtInfo)
        self.player2Down.setGeometry(QtCore.QRect(420, 190, 21, 21))
        self.player2Down.setObjectName("player2Down")
        self.endMatchB = QtWidgets.QPushButton(CourtInfo)
        self.endMatchB.setGeometry(QtCore.QRect(320, 40, 131, 31))
        self.endMatchB.setObjectName("endMatchB")

        self.retranslateUi(CourtInfo)
        self.buttonBox.accepted.connect(CourtInfo.accept)
        self.buttonBox.rejected.connect(CourtInfo.reject)
        QtCore.QMetaObject.connectSlotsByName(CourtInfo)

    def retranslateUi(self, CourtInfo):
        _translate = QtCore.QCoreApplication.translate
        CourtInfo.setWindowTitle(_translate("CourtInfo", "Dialog"))
        self.courtInfo.setText(_translate("CourtInfo", "Court X Information\n"
"Match X(**강)"))
        self.player1Name.setText(_translate("CourtInfo", "Player 1 : "))
        self.player2Name.setText(_translate("CourtInfo", "Player 2 : "))
        self.player1Score.setText(_translate("CourtInfo", "Player 1 Score : "))
        self.player1Up.setText(_translate("CourtInfo", "+"))
        self.player1Down.setText(_translate("CourtInfo", "-"))
        self.player2Score.setText(_translate("CourtInfo", "Player 2 Score : "))
        self.player2Up.setText(_translate("CourtInfo", "+"))
        self.player2Down.setText(_translate("CourtInfo", "-"))
        self.endMatchB.setText(_translate("CourtInfo", "End Match"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    CourtInfo = QtWidgets.QDialog()
    ui = Ui_CourtInfo()
    ui.setupUi(CourtInfo)
    CourtInfo.show()
    sys.exit(app.exec_())

