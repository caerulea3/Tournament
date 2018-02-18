"""Version 0.6_Last Updated 20171123"""
import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5 import uic
from UI.UI_courtCheckDialog import *

class CourtEndDialog(Ui_Dialog, QDialog):
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
