from GoogleAPI import google
def _zigzagMerge(a, b):
    timeForA=True
    res=[]
    while len(a)!=0 and len(b)!=0:
        if timeForA:
            res.append(a.pop(0))
            timeForA=False
        else:
            res.append(b.pop(0))
            timeForA=True
    if len(a)!=0:
        res+=a
    elif len(b)!=0:
        res+=b
    return res

def _sortForMS(arr):
    maxdepth=0
    ret=[]
    for g in arr:
        if g.depth()>maxdepth:
            maxdepth=g.depth()
    for i in range(maxdepth, -1, -1):
        for g in arr:
            if g.depth()==i:
                ret.append(g)
    return ret

def makeseq(match):
    if len(match.underMatch)==2:
        left=makeseq(match.underMatch[0])
        right=makeseq(match.underMatch[1])
        merge=_zigzagMerge(left, right)
        merge.append(match)
    else:
        merge=[match]

    merge=_sortForMS(merge)
    return merge

class WrongActError(Exception):
    def __init__(self, msg):
        self.msg = msg

    def __str__(self):
        return self.msg

def singleproblem(singleroot):
    return False

def doubleproblem(doubleroot):
    return False

def google_conn(spreadSheetId):
    googleconn=google(auth="rw")
    googleconn.get_credentials()
    googleconn.setSheetId(spreadSheetId)
    return googleconn

def google_singleset(googleconn, matchindex, x, sheetname=""):
    nodeHeight=7
    matchindex+=1

    startHeight=(nodeHeight * x.depth()) + 2
    countToFormat=""
    thiscount=matchindex

    while thiscount>25:
        countToFormat=chr(int(65+(thiscount%26)))+countToFormat
        thiscount=thiscount/26
    if matchindex>=26:
        countToFormat=chr(int(64+(thiscount%26)))+countToFormat
    else:
        countToFormat=chr(int(65+(thiscount%26)))+countToFormat
    # print(matchindex, countToFormat)
    # print(x.depth)

    rangeName = '{3}!{0}{1}:{0}{2}'.\
            format(countToFormat, startHeight, startHeight+7, sheetname)
    googleconn.addData(rangeName, \
    [
    ["Match #" + str(x.matchNum)],
    ["{0} vs. {1}".format(x.player[0].name('schoollong'), x.player[1].name('schoollong'))],
    ["Level : {0}".format(str(2**x.depth()*2)+"강" if x.depth()!=0 else "결승")],
    ["score : {0} : {1}".format(x.score[0], x.score[1])],
    ["power : {0} : {1}".format(x.player[0].power, x.player[1].power)],
    ["UpperMatch" + str(x.upperMatch.matchNum) if x.upperMatch is not None else "-"],
    [
        "UnderMatch {0}, {1}".format(\
        x.underMatch[0].matchNum if len(x.underMatch)!=0 else "-", \
        x.underMatch[1].matchNum if len(x.underMatch)!=0 else "-")\
    ],
    ])


def google_update(googleconn):
    googleconn.updateData()

class DirtyRoot():
    def __init__(self):
        pass

    def waitingmatches(self, root):
        udm=root.undermatches()
        wm=[]
        incourt=[]
        for c in self.Courts:
            if not c.empty():
                incourt.append(c.game)

        for m in udm:
            if m.editable() and (m not in incourt):
                wm.append(m)
        return wm

    def courtbut_exist(self, courtbut):
        if courtbut not in self.mainwin.courtbuttons:
            return None
        else:
            return self.mainwin.courtbuttons.index(courtbut)

    def askcourtlabel(self, courtbut):
        if courtbut not in self.mainwin.courtbuttons:
            raise WrongActError("Asked Court Does Not Exist")
        else:
            courtnum=self.mainwin.courtbuttons.index(courtbut)
            returnstr="Court {0}\n".format(courtnum+1)

            if not self.Courts[courtnum].empty():
                c=self.Courts[courtnum].game
                returnstr+="Match#{4}\n{0}({1})\nvs.\n{2}({3})".\
                        format(c.player[0].name(sep='\n'), \
                        c.score[0], c.player[1].name(sep="\n"), c.score[1],\
                        c.matchNum)

            return returnstr

    def waiting_tableform(self, single=True):
        waitingArray=self.waitingmatches(self.SingleRoot if single else self.DoubleRoot)
        waitingArray=_sortForMS(waitingArray)
        items=[]
        for i in range(len(waitingArray)):
            g=waitingArray[i]
            items.append([str(2**(g.depth()+1))+"강" if g.depth()!=0 else "결승",\
             g.player[0].name("school"),g.player[1].name("school"),"{0}->{1}->{2}".\
             format(g.upperMatch.matchNum if g.upperMatch is not None else "-", \
             g.upperMatch.upperMatch.matchNum if g.upperMatch is not None \
             and g.upperMatch.upperMatch is not None else "-", \
             g.upperMatch.upperMatch.upperMatch.matchNum if g.upperMatch is not None\
             and g.upperMatch.upperMatch is not None\
             and g.upperMatch.upperMatch.upperMatch is not None else "-"),\
             str(g.matchNum)])
        return items
