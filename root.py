from players import Person, SinglePlayer, DoublePlayer
from games import Match, Court
import filecontrol
from dirtyfunctions import makeseq, singleproblem, doubleproblem, DirtyRoot

class Root(DirtyRoot):
    """
    Internal Variables:
    Object Variables : SingleRoot, DoubleRoot, SingleSequence,
                       DoubleSequence, Courts, singlegoogle, doublegoogle
    Functions:
        __init__(self, singleroot=None, doubleroot=None)

        start(self)

        save(self, filepath), load(self, filepath),
        changecourtnum(self, newcourtnum)

        setmainwin(self, win), maketour(self), haveproblem(self)

        at DirtyRoot :
        waitingmatches(self, root), courtbut_exist(self, courtbut),
        askcourtlabel(self, courtbut), waiting_tableform(self, single=True),

    """


    def __init__(self, singleroot=None, doubleroot=None):
        super().__init__()
        self.SingleRoot=singleroot
        self.DoubleRoot=doubleroot
        self.SingleSequence=[]
        self.DoubleSequence=[]
        self.Courts=[]
        self.mainwin=None


    """Match Functions"""
    def start(self):
        #Refine Matches With Bye
        if self.SingleRoot is not None:
            singleMatches=self.SingleRoot.undermatches()
            for m in singleMatches:
                if m.player[1].isbye() and m.editable():
                    m.result(6, 0)
                    m.endmatch()
        if self.DoubleRoot is not None:
            doubleMatches=self.DoubleRoot.undermatches()
            for m in doubleMatches:
                if m.player[1].isbye() and m.editable():
                    m.result(6, 0)
                    m.endmatch()

        #Make MatchSequence
        if self.SingleRoot is not None and len(self.SingleSequence)==0:
            SingleSequence=makeseq(self.SingleRoot)
        if self.DoubleRoot is not None and len(self.DoubleSequence)==0:
            DoubleSequence=makeseq(self.DoubleRoot)


    """Control Functions"""
    def save(self, filepath):
        path=filepath
        if "." in filepath[-5:]:
            path=filepath[filepath.index(".")-1:]

        filecontrol.write_excel(path+".xlsx", self.SingleRoot, self.DoubleRoot)
        filecontrol.write_pickle(path+".tr", self)

    def load(self, filepath):
        filecontrol.read_pickle(filepath, self)

    def googlesave(self, spreadsheetId):
        if self.SingleRoot is not None:
            filecontrol.google_writeall(spreadsheetId, self.SingleRoot, "Singles")
        if self.DoubleRoot is not None:
            filecontrol.google_writeall(spreadsheetId, self.DoubleRoot, "Doubles")

    def changecourtnum(self, newcourtnum):
        while len(self.Courts)!=newcourtnum:
            if len(self.Courts)!=0 and len(self.Courts)>newcourtnum and self.Courts[-1].empty():
                self.Courts[-1].pop()
            if len(self.Courts)!=0 and len(self.Courts)>newcourtnum and (not self.Courts[-1].empty()):
                raise WrongActError("{0}번 코트는 경기가 진행중입니다!".format(len(self.Courts)+1))
            if len(self.Courts)<newcourtnum:
                self.Courts.append(Court())

    def setmainwin(self, win):
        self.mainwin=win

    """Tour Making Functions"""
    def maketour(self):
        """Reset and Initializing"""
        SinglePlayer.reset()
        DoublePlayer.reset()

        """singles"""
        Match.matchNum=0
        self.SingleRoot=Match(SinglePlayer)
        for x in SinglePlayer.array:
            print(x.name('schoollong'))
            self.SingleRoot.push(x)

        """doubles"""
        Match.matchNum=0
        self.DoubleRoot=Match(DoublePlayer)
        for x in DoublePlayer.array:
            self.DoubleRoot.push(x)

    def haveproblem(self):
        return singleproblem(self.SingleRoot) or doubleproblem(self.DoubleRoot)
