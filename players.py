import random
import operator

class Person():
    """
    Class Variables: count, array, infoDic, scoolDic
    Object Variables : schoolCode, schoolName, personName,
                       SingleObject, DoubleObject, check
    Functions:
        reset(), bye()
        __init__(self), set(self, schoolCode, schoolName, personName),
        setDummy(self, personName), name(self, form="short"), isbye(self)
    """
    count=1
    array=[]
    infoDic={}
    schoolDic={}

    def reset():
        count=1
        array=[]
        infoDic={}
        schoolDic={}

    def bye():
        if (None, "Bye") not in Person.infoDic.keys():
            bye=Person()
            bye.set(None, None, "Bye")
            SinglePlayer(bye)
            DoublePlayer(bye, bye)
            return bye
        else:
            return Person.infoDic[(None, "Bye")]


    def __init__(self):
        """Metaobject Control"""
        self.personNum=Person.count
        Person.count+=1
        Person.array.append(self)

        """Initialization"""
        self.schoolCode=None
        self.schoolName=None
        self.personName=None
        self.singleObject=None
        self.DoubleObject=None
        self.check=False

    def set(self, schoolCode, schoolName, personName):
        #check data perfection
        if (schoolCode, personName) in Person.infoDic.keys():
            Person.array.remove(self)
            return

        self.schoolCode=schoolCode
        self.schoolName=schoolName
        self.personName=personName
        Person.infoDic[(schoolCode, personName)]=self
        if not schoolCode in Person.schoolDic.keys():
            Person.schoolDic[schoolCode]=schoolName
        self.check=True

    def setDummy(self, personName):
        #it doesn't affect to Person.array!
        self.schoolCode=None
        self.schoolName=None
        self.personName=personName
        self.power=0

    def name(self, form="short"):
        if form=="short":
            return self.personName[:4]
        if form=="long":
            return self.personName
        if form=="school":
            return "{0} {1}".format("" if self.schoolName is None else self.schoolName, self.personName[:3])
        if form=="schoollong":
            return "{0} {1}".format("" if self.schoolName is None else self.schoolName, self.personName)

    def isbye(self):
        return (self.schoolCode, self.name())==(None, "Bye")

class SinglePlayer():
    """
    Internal Variables: count, array, topseed
    Object Variables : player, power, seed
    Functions:
        reset(), bye()

        __init__(self, player, seed=6), dummy(name), name(self, form="short")
        school(self), isbye(self)
    """
    count=1
    array=[]
    topseed=[]

    def reset():
        for p in SinglePlayer.array:
            p.power=max(0, random.randint(500, 600)-p.seed*100)
            SinglePlayer.array = sorted(SinglePlayer.array, \
                                 key=operator.attrgetter('power'), reverse=True)
            if (p.school(), p.seed) in SinglePlayer.topseed:
                ind=SinglePlayer.topseed.index((p.school(), p.seed))
                p.power+=5000 if ind==0 else (3000 if ind<3 else 2000)

    def bye():
        return Person.bye().singleObject

    def __init__(self, player, seed=6):
        """Metaobject Control"""
        self.playerNum=SinglePlayer.count
        SinglePlayer.count+=1
        SinglePlayer.array.append(self)

        """Initialization"""
        self.player=player
        if player.singleObject is not None:
            print("Person {0} already has SinglePlayer object for him"\
                        .format(player.name("schoollong")))
            raise ValueError
        player.singleObject=self
        self.power=max(0, random.randint(500, 600)-seed*100)
        self.seed=seed

    def dummy(name):
        #Dummy Player
        player=Person()
        player.setDummy(name)

        #Control Metadata
        dum=SinglePlayer(player)
        SinglePlayer.count-=1
        SinglePlayer.array.pop(-1)
        return dum

    def name(self, form="short", sep=""):
        return self.player.name(form=form)

    def school(self):
        return self.player.schoolCode

    def isbye(self):
        return self.player.isbye()


class DoublePlayer():
    """
    Internal Variables: count, array, topseed
    Object Variables : player1, player2, power, seed
    Functions:
        reset(), bye()

        __init__(self, player1, player2, seed=6), dummy(name),
        name(self, form="short"), school(self), isbye(self)
    """
    count=0
    array=[]
    topseed=[]
    def reset():
        for p in DoublePlayer.array:
            p.power=max(0, random.randint(500, 600)-p.seed*100)
            if (p.school(), p.seed) in DoublePlayer.topseed:
                ind=DoublePlayer.topseed.index((p.school(), p.seed))
                p.power+=5000 if ind==0 else (3000 if ind<3 else 2000)
            DoublePlayer.array = sorted(DoublePlayer.array, \
                                 key=operator.attrgetter('power'), reverse=True)

    def bye():
        return Person.bye().DoubleObject

    def __init__(self, player1, player2, seed=6):
        """Metaobject Control"""
        self.playerNum=DoublePlayer.count
        DoublePlayer.count+=1
        DoublePlayer.array.append(self)

        """Initialization"""
        self.player1=player1
        self.player2=player2
        if player1.DoubleObject is not None:
            raise ValueError
        if player2.DoubleObject is not None:
            raise ValueError
        player1.DoubleObject=self
        player2.DoubleObject=self
        self.power=max(0, random.randint(500, 600)-seed*100)
        self.seed=seed

    def dummy(name):
        #Dummy Player
        player=Person()
        player.setDummy(name)

        #Control Metadata
        dum=DoublePlayer(player, player)
        DoublePlayer.count-=1
        DoublePlayer.array.pop(-1)
        return dum

    def name(self, form="short", sep=" / "):
        return "{0}{1}{2}".format(self.player1.name(form=form), \
                                  sep, self.player2.name(form='long' if 'long'in form else 'short'))

    def school(self):
        return self.player1.schoolCode

    def isbye(self):
        return self.player1.isbye()


if __name__ == '__main__':
    from filecontrol import *
    from games import *
    from consoleAct import test
    import operator

    getPlayers("./Players Skeleton.xlsx")

    print(len(Person.array), len(SinglePlayer.array), len(DoublePlayer.array))

    SinglePlayer.array = sorted(SinglePlayer.array, \
                         key=operator.attrgetter('power'), reverse=True)

    while True:
        Match.matchNum=1
        root=Match()
        for p in SinglePlayer.array:
            print (p.name("schoollong"))
            root.push(p)

        if not test(root):
            break

    writeToExcel("./TestTour01.xlsx", singleRoot=root)
    writeToExcel("./TestTour01_D.xlsx", singleRoot=root, DEBUG=True)
