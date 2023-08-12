p = ["i", "we", "you", "they", "he", "she", "my", "his", "her", "their", "your", "our", "me", "him", "them"]

def equal_subjects(subject1 ,subject2):
    p_feminine =["she" ,"her"]
    p_masculine =["he" ,"his" ,"him"]
    p_self_speaker =["i" ,"my" ,"me"]
    p_you =["you" ,"your"]
    p_they =["they" ,"their"]
    p_we =["we" ,"our" ,"us"]

    if str(subject1 )==str(subject2):
        return True
    elif str(subject1) in p_feminine and str(subject2) in p_feminine:
        return True
    elif str(subject1) in p_masculine and str(subject2) in p_masculine:
        return True
    elif str(subject1) in p_self_speaker and str(subject2) in p_self_speaker:
        return True
    elif str(subject1) in p_you and str(subject2) in p_you:
        return True
    elif str(subject1) in p_they and str(subject2) in p_they:
        return True
    elif str(subject1) in p_we and str(subject2) in p_we:
        return True
    else:
        False


def aggregation_between_filtering_and_resolution(aggregation_for_sentence, resolution):
    agg = []
    b = aggregation_for_sentence
    if resolution != None and len(resolution) == 0 and (len(b) == 2):
        agg.append(b)
    if resolution != None and len(resolution) != 0 and (len(b) == 2):
        if b[0] != 0 and b[1] != 0:
            if len(b[1]) == 1:
                if isinstance(b[1][0], tuple) == True:
                    agg.append((b[0], resolution))
                elif isinstance(b[1][0], tuple) == False:
                    if str(b[1][0]) in p:
                        agg.append((b[0], resolution))
                    elif str(b[1][0]) not in p:
                        agg.append((b[0], b[1]))
            elif len(b[1]) > 1:
                if len(b[1]) == len(resolution):
                    agg.append((b[0], resolution))

                elif len(b[1]) != len(resolution):
                    for i in range(len(b[1])):
                        if i + 1 < len(b[1]):
                            if equal_subjects(b[1][i], b[1][i + 1]):
                                b[1].remove(b[1][i])
                    for i in range(len(resolution)):
                        for j in range(len(b[1])):
                            if isinstance(b[1][j], tuple) == False:
                                if str(b[1][j]) in p:
                                    b[1][j] = resolution[i]
                                    continue
                            elif isinstance(b[1][j], tuple) == True:
                                c = b[1][j]
                                if str(c[0]) in p:
                                    b[1][j] = resolution[i]

                                    continue
                    agg.append((b[0], b[1]))
    return agg