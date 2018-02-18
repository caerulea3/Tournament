import sys
import os
from players import Person, SinglePlayer, DoublePlayer
from filecontrol import read_excel, write_excel, write_pickle
from games import Match
from root import Root

warnings=True
trialNum=0
filename=""
path=""

"""open file"""
playersFileName=input("Enter Filename of players : ")
while not os.path.exists("./"+playersFileName):
    if playersFileName=="?":
        print(os.system("dir"))
    else:
        print("Invalid Filename")
    playersFileName=input("Enter Filename of players : ")
read_excel("./"+playersFileName)

rt=Root()

while warnings==True:
    rt.maketour()
    warnings=rt.haveproblem()

"""Write To Files"""
if filename=="":
    folder=input("Enter Folder Name(Present Folder if enters none) :")
    if folder!="" and not os.path.exists("./"+folder):
        os.makedirs("./"+folder)
        print("MakeDir Success")
    path="./" if folder=="" else "./"+folder+"/"
    filename=input("Enter FileName : ")
    filename=path + filename
rt.save(filename)
