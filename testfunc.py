from root import Root
import sys
from games import Match
from filecontrol import google_writeall
import random

rt=Root()
rt.load("./Realtest/test05.tr")
rt.start()
rt.changecourtnum(14)

while True:
    order=int(input("Enter next order (1 : next result, 2 : court set) : "))
    if order==1:
        cn=random.randint(0, len(rt.Courts)-1)
        tc=rt.Courts[cn]
        t=0
        while tc.empty():
            cn=random.randint(0, len(rt.Courts)-1)
            tc=rt.Courts[cn]
            t+=1
            if t==100:
                print("No courts are on play")
                break
        if tc.game is not None:
            g=tc.game
            if max(g.score[0], g.score[1])==4:
                winning=random.randint(0, 10)%2
                g.score[winning]=6
                g.score[(winning+1)%2]=random.randint(g.score[(winning+1)%2], 7)
                print("Court{0}, Match{3}, {1} vs {2}".format(cn+1, g.player[0].name('schoollong'), g.player[1].name('schoollong'), g.matchNum), g.score)
                tc.clear_court()
            else:
                winning=random.randint(0, 10)%2
                g.score[winning]=4
                g.score[(winning+1)%2]=random.randint(g.score[(winning+1)%2], 4)
                print("Court{0}, Match{3}, {1} vs {2}".format(cn+1, g.player[0].name('schoollong'), g.player[1].name('schoollong'), g.matchNum), g.score)
    if order==2:
        courtnum, matchnum, gametype=\
        int(input("Input Court Number : ")), int(input("Input Match Number : ")),\
        int(input("Input 1 if Singles, 2 if Doubles : "))
        match=None
        waitings=rt.waitingmatches(rt.SingleRoot if gametype==1 else rt.DoubleRoot)
        for m in waitings:
            if m.matchNum==matchnum:
                match=m
        if match is None:
            print("The Match Does Not Exist")
        else:
            print(match.matchNum)
            rt.Courts[courtnum-1].game=match
    if order==0:
        break

    rt.googlesave("1UFZKwYCQZyxoIQfPNjkopIuN5jVocGaSbWicClZ0RaM")
