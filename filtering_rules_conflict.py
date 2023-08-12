import pandas as pd


"""aggregiation all possible (events and subjects) for the sentence in one list"""


def aggregation_for_sentence(list_tuple):
    ag = []
    events = []
    subjects = []
    sub = []
    s = []
    if len(list_tuple) >= 1:
        for i in range(len(list_tuple)):
            # event
            lis1 = list_tuple[i][1]
            # subject
            lis2 = list_tuple[i][2]
            if lis2 != None:
                if lis1 != None:
                    ag.append([lis1[1], lis2])

        for i in range(len(ag)):
            events.append(ag[i][0])

            # has subject
            if len(ag[i]) == 2:
                sub_ = ag[i][1]
                for index in range(len(sub_)):
                    if isinstance(sub_[index], tuple) == False:
                        if sub_[index] not in s:
                            s.append(sub_[index])
                            if s != None:
                                if len(s) != 0:
                                    for j in range(len(s)):
                                        subjects.append(s[j])


                    else:
                        subjects.append(sub_[index])

        subjects = list(pd.Series(subjects).drop_duplicates())
        return events, subjects

"""filtering all cases for rules conflict"""
def filtering(list_tuple=[]):
    if len(list_tuple) >= 6:
        _6_rules(list_tuple)
        if len(list_tuple) >= 5:
            _5_rules(list_tuple)
            if len(list_tuple) >= 4:
                _4_rules(list_tuple)
                if len(list_tuple) >= 3:
                    _3_rules(list_tuple)
                    if len(list_tuple) >= 2:
                        _2_rules(list_tuple)

    if len(list_tuple) >= 5:
        _5_rules(list_tuple)
        if len(list_tuple) >= 4:
            _4_rules(list_tuple)
            if len(list_tuple) >= 3:
                _3_rules(list_tuple)
                if len(list_tuple) >= 2:
                    _2_rules(list_tuple)

    if len(list_tuple) >= 4:
        _4_rules(list_tuple)
        if len(list_tuple) >= 3:
            _3_rules(list_tuple)
            if len(list_tuple) >= 2:
                _2_rules(list_tuple)

    if len(list_tuple) >= 3:
        _3_rules(list_tuple)
        if len(list_tuple) >= 2:
            _2_rules(list_tuple)

    if len(list_tuple) >= 2:
        _2_rules(list_tuple)



"""All possible permutations of rules conflict """


def _6_rules(list_tuple=[]):
    if (list_tuple[0][0] == "Rule1 " and list_tuple[1][0] == "Rule2 " and list_tuple[2][0] == "Rule3 " and
            list_tuple[3][0] == "Rule4 " and list_tuple[4][0] == "Rule5 " and list_tuple[5][0] == "Rule6 "):
        lis1 = str(list_tuple[2][1][1]).split()
        lis2 = str(list_tuple[5][1][1]).split()
        if str(lis1[1]) == str(lis2[1]):
            print(lis1[0] + " " + lis2[1] + " " + lis1[1])
            list_tuple.remove(list_tuple[2])
            list_tuple.remove(list_tuple[5])


def _5_rules(list_tuple=[]):
    if (list_tuple[0][0] == "Rule1 " and list_tuple[1][0] == "Rule2 " and list_tuple[2][0] == "Rule3 " and
            list_tuple[3][0] == "Rule4 " and list_tuple[4][0] == "Rule5 "):
        lis1 = str(list_tuple[2][1][1]).split()
        lis2 = str(list_tuple[4][1][1]).split()
        if str(lis1[1]) == str(lis2[1]):
            list_tuple.remove(list_tuple[4])


    elif (list_tuple[0][0] == "Rule1 " and list_tuple[1][0] == "Rule2 " and list_tuple[2][0] == "Rule3 " and
          list_tuple[3][0] == "Rule4 " and list_tuple[4][0] == "Rule5 "):
        lis1 = str(list_tuple[1][1][1]).split()
        lis2 = str(list_tuple[4][1][1]).split()
        if str(lis1[1]) == str(lis2[1]):
            list_tuple.remove(list_tuple[4])


    elif (list_tuple[0][0] == "Rule1 " and list_tuple[1][0] == "Rule2 " and list_tuple[2][0] == "Rule3 " and
          list_tuple[3][0] == "Rule4 " and list_tuple[4][0] == "Rule6 "):
        lis1 = str(list_tuple[2][1][1]).split()
        lis2 = str(list_tuple[4][1][1]).split()
        if str(lis1[1]) == str(lis2[1]):
            print(lis1[0] + " " + lis2[1] + " " + lis1[1])
            list_tuple.remove(list_tuple[2])
            list_tuple.remove(list_tuple[4])

    elif (list_tuple[0][0] == "Rule1 " and list_tuple[1][0] == "Rule2 " and list_tuple[2][0] == "Rule3 " and
          list_tuple[3][0] == "Rule5 " and list_tuple[4][0] == "Rule6 "):
        lis1 = str(list_tuple[2][1][1]).split()
        lis2 = str(list_tuple[4][1][1]).split()
        if str(lis1[1]) == str(lis2[1]):
            print(lis1[0] + " " + lis2[1] + " " + lis1[1])
            list_tuple.remove(list_tuple[2])
            list_tuple.remove(list_tuple[4])

    elif (list_tuple[0][0] == "Rule2 " and list_tuple[1][0] == "Rule3 " and list_tuple[2][0] == "Rule4 " and
          list_tuple[3][0] == "Rule5 " and list_tuple[4][0] == "Rule6 "):
        lis1 = str(list_tuple[1][1][1]).split()
        lis2 = str(list_tuple[4][1][1]).split()
        if str(lis1[1]) == str(lis2[1]):
            print(lis1[0] + " " + lis2[1] + " " + lis1[1])
            list_tuple.remove(list_tuple[1])
            list_tuple.remove(list_tuple[4])

    elif (list_tuple[0][0] == "Rule1 " and list_tuple[1][0] == "Rule3 " and list_tuple[2][0] == "Rule4 " and
          list_tuple[3][0] == "Rule5 " and list_tuple[4][0] == "Rule6 "):
        lis1 = str(list_tuple[1][1][1]).split()
        lis2 = str(list_tuple[4][1][1]).split()
        if str(lis1[1]) == str(lis2[1]):
            print(lis1[0] + " " + lis2[1] + " " + lis1[1])
            list_tuple.remove(list_tuple[1])
            list_tuple.remove(list_tuple[4])


def _4_rules(list_tuple=[]):
    if (list_tuple[0][0] == "Rule1 " and list_tuple[1][0] == "Rule2 " and list_tuple[2][0] == "Rule3 " and
            list_tuple[3][0] == "Rule5 "):
        lis1 = str(list_tuple[0][1][1]).split()
        lis2 = str(list_tuple[3][1][1]).split()
        if str(lis1[1]) == str(lis2[1]):
            list_tuple.remove(list_tuple[3])

    elif (list_tuple[0][0] == "Rule2 " and list_tuple[1][0] == "Rule3 " and list_tuple[2][0] == "Rule4 " and
          list_tuple[3][0] == "Rule5 "):
        lis1 = str(list_tuple[0][1][1]).split()
        lis2 = str(list_tuple[3][1][1]).split()
        if str(lis1[1]) == str(lis2[1]):
            list_tuple.remove(list_tuple[3])

    elif (list_tuple[0][0] == "Rule1 " and list_tuple[1][0] == "Rule2 " and list_tuple[2][0] == "Rule4 " and
          list_tuple[3][0] == "Rule5 "):
        lis1 = str(list_tuple[1][1][1]).split()
        lis2 = str(list_tuple[3][1][1]).split()
        if str(lis1[1]) == str(lis2[1]):
            list_tuple.remove(list_tuple[3])

    elif (list_tuple[0][0] == "Rule1 " and list_tuple[1][0] == "Rule3 " and list_tuple[2][0] == "Rule4 " and
          list_tuple[3][0] == "Rule5 "):
        lis1 = str(list_tuple[1][1][1]).split()
        lis2 = str(list_tuple[3][1][1]).split()
        if str(lis1[1]) == str(lis2[1]):
            list_tuple.remove(list_tuple[3])

    elif (list_tuple[0][0] == "Rule2 " and list_tuple[1][0] == "Rule3 " and list_tuple[2][0] == "Rule4 " and
          list_tuple[3][0] == "Rule5 "):
        lis1 = str(list_tuple[1][1][1]).split()
        lis2 = str(list_tuple[3][1][1]).split()
        if str(lis1[1]) == str(lis2[1]):
            list_tuple.remove(list_tuple[3])

    elif (list_tuple[0][0] == "Rule1 " and list_tuple[1][0] == "Rule2 " and list_tuple[2][0] == "Rule3 " and
          list_tuple[3][0] == "Rule5 "):
        lis1 = str(list_tuple[2][1][1]).split()
        lis2 = str(list_tuple[3][1][1]).split()
        if str(lis1[1]) == str(lis2[1]):
            list_tuple.remove(list_tuple[3])

    elif (list_tuple[0][0] == "Rule1 " and list_tuple[1][0] == "Rule2 " and list_tuple[2][0] == "Rule3 " and
          list_tuple[3][0] == "Rule6 "):
        lis1 = str(list_tuple[2][1][1]).split()
        lis2 = str(list_tuple[3][1][1]).split()
        if str(lis1[0]) == str(lis2[0]):
            print(lis1[0] + " " + lis2[1] + " " + lis1[1])
            list_tuple.remove(list_tuple[2])
            list_tuple.remove(list_tuple[3])

    elif (list_tuple[0][0] == "Rule1 " and list_tuple[1][0] == "Rule3 " and list_tuple[2][0] == "Rule4 " and
          list_tuple[3][0] == "Rule6 "):
        lis1 = str(list_tuple[1][1][1]).split()
        lis2 = str(list_tuple[3][1][1]).split()
        if str(lis1[0]) == str(lis2[0]):
            print(lis1[0] + " " + lis2[1] + " " + lis1[1])
            list_tuple.remove(list_tuple[1])
            list_tuple.remove(list_tuple[3])

    elif (list_tuple[0][0] == "Rule1 " and list_tuple[1][0] == "Rule3 " and list_tuple[2][0] == "Rule5 " and
          list_tuple[3][0] == "Rule6 "):
        lis1 = str(list_tuple[1][1][1]).split()
        lis2 = str(list_tuple[3][1][1]).split()
        if str(lis1[0]) == str(lis2[0]):
            print(lis1[0] + " " + lis2[1] + " " + lis1[1])
            list_tuple.remove(list_tuple[1])
            list_tuple.remove(list_tuple[3])

    elif (list_tuple[0][0] == "Rule2 " and list_tuple[1][0] == "Rule3 " and list_tuple[2][0] == "Rule5 " and
          list_tuple[3][0] == "Rule6 "):
        lis1 = str(list_tuple[1][1][1]).split()
        lis2 = str(list_tuple[3][1][1]).split()
        if str(lis1[0]) == str(lis2[0]):
            print(lis1[0] + " " + lis2[1] + " " + lis1[1])
            list_tuple.remove(list_tuple[1])
            list_tuple.remove(list_tuple[3])


    elif (list_tuple[0][0] == "Rule2 " and list_tuple[1][0] == "Rule3 " and list_tuple[2][0] == "Rule4 " and
          list_tuple[3][0] == "Rule6 "):
        lis1 = str(list_tuple[1][1][1]).split()
        lis2 = str(list_tuple[3][1][1]).split()
        if str(lis1[0]) == str(lis2[0]):
            print(lis1[0] + " " + lis2[1] + " " + lis1[1])
            list_tuple.remove(list_tuple[1])
            list_tuple.remove(list_tuple[3])

    elif (list_tuple[0][0] == "Rule3 " and list_tuple[1][0] == "Rule4 " and list_tuple[2][0] == "Rule5 " and
          list_tuple[3][0] == "Rule6 "):
        lis1 = str(list_tuple[0][1][1]).split()
        lis2 = str(list_tuple[3][1][1]).split()
        if str(lis1[0]) == str(lis2[0]):
            print(lis1[0] + " " + lis2[1] + " " + lis1[1])
            list_tuple.remove(list_tuple[0])
            list_tuple.remove(list_tuple[3])


def _3_rules(list_tuple=[]):
    if (list_tuple[0][0] == "Rule1 " and list_tuple[1][0] == "Rule2 " and list_tuple[2][0] == "Rule3 "):
        lis1 = str(list_tuple[1][1][1]).split()
        lis2 = str(list_tuple[2][1][1]).split()
        if str(lis1[1]) == str(lis2[1]):
            list_tuple.remove(list_tuple[2])


    elif (list_tuple[0][0] == "Rule1 " and list_tuple[1][0] == "Rule2 " and list_tuple[2][0] == "Rule5 "):
        lis1 = str(list_tuple[1][1][1]).split()
        lis2 = str(list_tuple[2][1][1]).split()
        if str(lis1[1]) == str(lis2[1]):
            list_tuple.remove(list_tuple[2])

    elif (list_tuple[0][0] == "Rule2 " and list_tuple[1][0] == "Rule3 " and list_tuple[2][0] == "Rule5 "):
        lis1 = str(list_tuple[0][1][1]).split()
        lis2 = str(list_tuple[2][1][1]).split()
        if str(lis1[1]) == str(lis2[1]):
            list_tuple.remove(list_tuple[2])

    elif (list_tuple[0][0] == "Rule2 " and list_tuple[1][0] == "Rule4 " and list_tuple[2][0] == "Rule5 "):
        lis1 = str(list_tuple[0][1][1]).split()
        lis2 = str(list_tuple[2][1][1]).split()
        if str(lis1[1]) == str(lis2[1]):
            list_tuple.remove(list_tuple[2])

    elif (list_tuple[0][0] == "Rule1 " and list_tuple[1][0] == "Rule3 " and list_tuple[2][0] == "Rule5 "):
        lis1 = str(list_tuple[1][1][1]).split()
        lis2 = str(list_tuple[2][1][1]).split()
        if str(lis1[1]) == str(lis2[1]):
            list_tuple.remove(list_tuple[2])

    elif (list_tuple[0][0] == "Rule2 " and list_tuple[1][0] == "Rule3 " and list_tuple[2][0] == "Rule5 "):
        lis1 = str(list_tuple[1][1][1]).split()
        lis2 = str(list_tuple[2][1][1]).split()
        if str(lis1[1]) == str(lis2[1]):
            list_tuple.remove(list_tuple[2])

    elif (list_tuple[0][0] == "Rule3 " and list_tuple[1][0] == "Rule4 " and list_tuple[2][0] == "Rule5 "):
        lis1 = str(list_tuple[0][1][1]).split()
        lis2 = str(list_tuple[2][1][1]).split()
        if str(lis1[1]) == str(lis2[1]):
            list_tuple.remove(list_tuple[2])

    elif (list_tuple[0][0] == "Rule1 " and list_tuple[1][0] == "Rule3 " and list_tuple[2][0] == "Rule6 "):
        lis1 = str(list_tuple[1][1][1]).split()
        lis2 = str(list_tuple[2][1][1]).split()
        if str(lis1[0]) == str(lis2[0]):
            print(lis1[0] + " " + lis2[1] + " " + lis1[1])
            list_tuple.remove(list_tuple[1])
            list_tuple.remove(list_tuple[2])

    elif (list_tuple[0][0] == "Rule2 " and list_tuple[1][0] == "Rule3 " and list_tuple[2][0] == "Rule6 "):
        lis1 = str(list_tuple[1][1][1]).split()
        lis2 = str(list_tuple[2][1][1]).split()
        if str(lis1[0]) == str(lis2[0]):
            print(lis1[0] + " " + lis2[1] + " " + lis1[1])
            list_tuple.remove(list_tuple[1])
            list_tuple.remove(list_tuple[2])

    elif (list_tuple[0][0] == "Rule3 " and list_tuple[1][0] == "Rule4 " and list_tuple[2][0] == "Rule6 "):
        lis1 = str(list_tuple[0][1][1]).split()
        lis2 = str(list_tuple[2][1][1]).split()
        if str(lis1[0]) == str(lis2[0]):
            print(lis1[0] + " " + lis2[1] + " " + lis1[1])
            list_tuple.remove(list_tuple[0])
            list_tuple.remove(list_tuple[2])

    elif (list_tuple[0][0] == "Rule3 " and list_tuple[1][0] == "Rule5 " and list_tuple[2][0] == "Rule6 "):
        lis1 = str(list_tuple[0][1][1]).split()
        lis2 = str(list_tuple[2][1][1]).split()
        if str(lis1[0]) == str(lis2[0]):
            print(lis1[0] + " " + lis2[1] + " " + lis1[1])
            list_tuple.remove(list_tuple[0])
            list_tuple.remove(list_tuple[2])


def _2_rules(list_tuple=[]):
    if (list_tuple[0][0] == "Rule1 " and list_tuple[1][0] == "Rule2 "):
        lis = str(list_tuple[1][1][1]).split()
        if str(list_tuple[0][1][1]) == str(lis[0]):
            list_tuple.remove(list_tuple[0])

    elif (list_tuple[0][0] == "Rule2 " and list_tuple[1][0] == "Rule3 "):
        lis1 = str(list_tuple[0][1][1]).split()
        lis2 = str(list_tuple[1][1][1]).split()
        if str(lis1[1]) == str(lis2[1]):
            list_tuple.remove(list_tuple[1])

    elif (list_tuple[0][0] == "Rule2 " and list_tuple[1][0] == "Rule5 "):
        lis1 = str(list_tuple[0][1][1]).split()
        lis2 = str(list_tuple[1][1][1]).split()
        if str(lis1[1]) == str(lis2[1]):
            list_tuple.remove(list_tuple[1])

    elif (list_tuple[0][0] == "Rule3 " and list_tuple[1][0] == "Rule5 "):
        lis1 = str(list_tuple[0][1][1]).split()
        lis2 = str(list_tuple[1][1][1]).split()
        if str(lis1[1]) == str(lis2[1]):
            list_tuple.remove(list_tuple[1])

    elif (list_tuple[0][0] == "Rule3 " and list_tuple[1][0] == "Rule6 "):
        lis1 = str(list_tuple[0][1][1]).split()
        lis2 = str(list_tuple[1][1][1]).split()
        if str(lis1[0]) == str(lis2[0]):
            list_tuple.remove(list_tuple[1])