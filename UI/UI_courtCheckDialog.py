# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'courtCheckDialog.ui'
#
# Created by: PyQt5 UI code generator 5.6
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(400, 300)
        self.buttonBox = QtWidgets.QDialogButtonBox(Dialog)
        self.buttonBox.setGeometry(QtCore.QRect(30, 240, 341, 32))
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.player1Name_2 = QtWidgets.QLabel(Dialog)
        self.player1Name_2.setGeometry(QtCore.QRect(30, 140, 341, 61))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.player1Name_2.setFont(font)
        self.player1Name_2.setAlignment(QtCore.Qt.AlignCenter)
        self.player1Name_2.setObjectName("player1Name_2")
        self.player1Name = QtWidgets.QLabel(Dialog)
        self.player1Name.setGeometry(QtCore.QRect(60, 40, 291, 101))
        self.player1Name.setAlignment(QtCore.Qt.AlignCenter)
        self.player1Name.setObjectName("player1Name")

        self.retranslateUi(Dialog)
        self.buttonBox.accepted.connect(Dialog.accept)
        self.buttonBox.rejected.connect(Dialog.reject)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.player1Name_2.setText(_translate("Dialog", "확정하시겠습니까??\n"
"(경기 결과를 확정하면 더이상 수정할 수 없습니다)"))
        self.player1Name.setText(_translate("Dialog", "현재 경기의 정보는 다음과 같습니다\n"
"Match #{matchnum}\n"
"Player: {ply1}:{ply2}\n"
"Score : {scr1}:{scr2}"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Dialog = QtWidgets.QDialog()
    ui = Ui_Dialog()
    ui.setupUi(Dialog)
    Dialog.show()
    sys.exit(app.exec_())

