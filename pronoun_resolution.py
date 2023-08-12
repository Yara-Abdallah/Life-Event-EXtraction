
import pandas as pd
from allennlp.predictors.predictor import Predictor
predictor = Predictor.from_path("I17-1099.Datasets/EMNLP_dataset/coref-spanbert-large-2021.03.10(3).tar.gz")

p = ["he", "she", "her", "his", "him", "they", "their", "them", "us", "we", "our", "me", "my", "you", "your", "i"]
# the number of sentence we need for making pronoun resolution
num_of_sentence_for_pronoun_resolution = 2


# getting corference clusters
def pronoun_resolution_allen(sent, predictor=predictor):
    pred = predictor.predict(
        document=sent
    )

    clusters = pred['clusters']
    document = pred['document']
    n = 0
    doc = {}
    for obj in document:
        doc.update({n: obj})
        # what I'm doing here is creating a dictionary of each word with its respective index, making it easier later.
        n = n + 1

    clus_all = []
    cluster = []
    clus_one = {}
    s = ""
    for i in range(0, len(clusters)):
        one_cl = clusters[i]
        for count in range(0, len(one_cl)):
            obj = one_cl[count]
            for num in range((obj[0]), (obj[1] + 1)):
                for n in doc:
                    if num == n:
                        if obj[1] - obj[0] > 0:
                            s += " " + str(doc[n])
                            if len(s.split()) >= 2:
                                cluster.append(s)
                        elif obj[1] - obj[0] == 0:
                            cluster.append(doc[n])
        clus_all.append(cluster)
        cluster = []
    return clus_all


""" my rules for pronoun resolution for i pronoun return the sayer of this sentence """
def my_pronoun_resolution_for_i(sub, sub2, dialog_number, index_of_sentence, sayers_of_dialog):
   subjects = ""
   if str(sub2) == " ":
       subjects = sayers_of_dialog[dialog_number][index_of_sentence]
   elif str(sub2) != " ":
       c = sayers_of_dialog[dialog_number][index_of_sentence] + " " + str(sub2)
       subjects = c
   return subjects


""" my rules for pronoun resolution for you pronoun return the sayer of next sentence or this , depend on the long of the dialog"""
def my_pronoun_resolution_for_you(sub, sub2, dialog_number, index_of_sentence, sayers_of_dialog,len_of_dialog):
    subjects = ""
    if len_of_dialog[dialog_number] - 1 == index_of_sentence:
        if sayers_of_dialog[dialog_number][index_of_sentence - 1] != sayers_of_dialog[dialog_number][index_of_sentence]:
            if str(sub2) == " ":
                subjects = sayers_of_dialog[dialog_number][index_of_sentence - 1]
            elif str(sub2) != " ":
                c = sayers_of_dialog[dialog_number][index_of_sentence - 1] + " " + str(sub2)
                subjects = c
    if len_of_dialog[dialog_number] - 1 > index_of_sentence:
        if sayers_of_dialog[dialog_number][index_of_sentence + 1] != sayers_of_dialog[dialog_number][index_of_sentence]:
            if str(sub2) == " ":
                subjects = sayers_of_dialog[dialog_number][index_of_sentence + 1]
            elif str(sub2) != " ":
                c = sayers_of_dialog[dialog_number][index_of_sentence + 1] + " " + str(sub2)
                subjects = c
    return subjects


""" my rules for pronoun resolution for we pronoun return the sayers of this dialog"""
def my_pronoun_resolution_rules_for_we(sub, sub2, dialog_number, index_of_sentence, sayers_of_dialog,len_of_dialog):
   subjects = ""
   if len_of_dialog[dialog_number] - 1 == index_of_sentence:
       if sayers_of_dialog[dialog_number][index_of_sentence - 1] != sayers_of_dialog[dialog_number][index_of_sentence]:
           if str(sub2) == " ":
               c = sayers_of_dialog[dialog_number][index_of_sentence - 1] + " and " + sayers_of_dialog[dialog_number][
                   index_of_sentence]
               subjects = c
           elif str(sub2) != " ":
               c = sayers_of_dialog[dialog_number][index_of_sentence - 1] + " and " + sayers_of_dialog[dialog_number][
                   index_of_sentence] + " " + str(sub2)
               subjects = c

   if len_of_dialog[dialog_number] - 1 > index_of_sentence:
       if sayers_of_dialog[dialog_number][index_of_sentence + 1] != sayers_of_dialog[dialog_number][index_of_sentence]:
           if str(sub2) == " ":
               c = sayers_of_dialog[dialog_number][index_of_sentence + 1] + " and " + sayers_of_dialog[dialog_number][
                   index_of_sentence]
               subjects = c
           elif str(sub2) != " ":
               c = sayers_of_dialog[dialog_number][index_of_sentence + 1] + " and " + sayers_of_dialog[dialog_number][
                   index_of_sentence] + " " + str(sub2)
               subjects = c
   return subjects


def check_type_of_subject(sub):
   if isinstance(sub, tuple) == False:
       return sub, " "
   if isinstance(sub, tuple) == True:
       return sub[0], sub[1]


def getting_n_previous_sentences(index_of_sentence, num_of_sentence_for_pronoun_resolution, sentences_of_dialogs,
                                dialog_number):
   sentence = []
   text = ""
   index_of_sentence1 = index_of_sentence
   while (index_of_sentence1 >= 0 and num_of_sentence_for_pronoun_resolution >= 0):
       sentence.append(sentences_of_dialogs[dialog_number][index_of_sentence1])
       index_of_sentence1 -= 1
       num_of_sentence_for_pronoun_resolution -= 1
   for i in range(len(sentence)):
       text += " " + str(sentence[len(sentence) - i - 1])
   return text



"""like my sister after pronoun resolution should make pronoun again using my rules"""

def check_need_for_more_resol(element, dialog_number, index_of_sentence, sayers_of_dialog):
    count = element.count(' and ')

    while (count >= 0):

        if " my " in element:
            subb = my_pronoun_resolution_for_i(element, " ", dialog_number, index_of_sentence, sayers_of_dialog)
            element = element.replace(" my ", " " + str(subb) + " ")

        elif element.endswith(' my') == True:
            subb = my_pronoun_resolution_for_i(element, " ", dialog_number, index_of_sentence, sayers_of_dialog)
            element = element.replace(" my", " " + str(subb))

        elif " i " in element:
            subb = my_pronoun_resolution_for_i(element, " ", dialog_number, index_of_sentence, sayers_of_dialog)
            element = element.replace(" i ", " " + str(subb) + " ")
            print("element .... ", element)

        elif element.endswith(' i') == True:
            subb = my_pronoun_resolution_for_i(element, " ", dialog_number, index_of_sentence, sayers_of_dialog)
            element = element.replace(" i", " " + str(subb))
            print("element .... ", element)

        elif " me " in element:
            subb = my_pronoun_resolution_for_i(element, " ", dialog_number, index_of_sentence, sayers_of_dialog)
            element = element.replace(" me ", " " + str(subb) + " ")

        elif element.endswith(' me') == True:
            subb = my_pronoun_resolution_for_i(element, " ", dialog_number, index_of_sentence, sayers_of_dialog)
            element = element.replace(" me", " " + str(subb))


        elif " you " in element:
            subb = my_pronoun_resolution_for_you(element, " ", dialog_number, index_of_sentence, sayers_of_dialog)
            element = element.replace(" you ", " " + str(subb) + " ")

        elif element.endswith(' you') == True:
            subb = my_pronoun_resolution_for_you(element, " ", dialog_number, index_of_sentence, sayers_of_dialog)
            element = element.replace(" you", " " + str(subb))


        elif " your " in element:
            subb = my_pronoun_resolution_for_you(element, " ", dialog_number, index_of_sentence, sayers_of_dialog)
            element = element.replace(" your ", " " + str(subb) + " ")

        elif element.endswith(' your') == True:
            subb = my_pronoun_resolution_for_you(element, " ", dialog_number, index_of_sentence, sayers_of_dialog)
            element = element.replace(" your", " " + str(subb))

        elif (" my " not in element) and (" i " not in element) and (" me " not in element) and (
                " your " not in element) and (" you " not in element) and (element.endswith(' you') == False) and (
                element.endswith(' your') == False) and (element.endswith(' i') == False) and (
                element.endswith(' my') == False) and (element.endswith(' me') == False):
            element = " "

        count -= 1

    return element



def pronoun_resolution_for_all_cases_of_pronouns(aggrigation_list=[], dialog_number=0, index_of_sentence=0,
                                                 sentences_of_dialogs=[], num_of_sentence_for_pronoun_resolution=3,sayers_of_dialog=[],len_of_dialog=[]):
    b = aggrigation_list

    if len(b[0]) != 0 and len(b[1]) != 0:
        subjects = []

        for i in range(len(b[1])):

            sub, sub2 = check_type_of_subject(b[1][i])

            if str(sub) == "i" or str(sub) == "my" or str(sub) == "me":
                subjects.append(
                    my_pronoun_resolution_for_i(sub, sub2, dialog_number, index_of_sentence, sayers_of_dialog))


            elif str(sub) == "you" or str(sub) == "your":
                subjects.append(
                    my_pronoun_resolution_for_you(sub, sub2, dialog_number, index_of_sentence, sayers_of_dialog,len_of_dialog))


            elif str(sub) == "her" or str(sub) == "she":

                text = getting_n_previous_sentences(index_of_sentence, num_of_sentence_for_pronoun_resolution,
                                                    sentences_of_dialogs, dialog_number)

                print("....... more than one sentence for making pro resolution ....... (", (text), ")", "\n")

                resol = pronoun_resolution_allen(text)

                if len(resol) != 0:
                    for i in resol:
                        if "her" in i or "she" in i:
                            for element in i:
                                if len(element.split()) == 1:
                                    if element not in p:
                                        if str(sub2) == " ":
                                            subjects.append(element)
                                        elif str(sub2) != " ":
                                            c = element + " " + str(sub2)
                                            subjects.append(c)
                                elif len(element.split()) == 2:
                                    ele = check_need_for_more_resol(element, dialog_number, index_of_sentence,
                                                                    sayers_of_dialog)
                                    # like my sister after pronoun resolution should make pronoun again using my rules
                                    if ele == " ":
                                        if str(sub2) == " ":
                                            subjects.append(element)
                                        elif str(sub2) != " ":
                                            c = element + " " + str(sub2)
                                            subjects.append(c)
                                    else:
                                        if str(sub2) == " ":
                                            subjects.append(ele)
                                        elif str(sub2) != " ":
                                            c = ele + " " + str(sub2)
                                            subjects.append(c)






            elif str(sub) == "he" or str(sub) == "his" or str(sub) == "him":

                text = getting_n_previous_sentences(index_of_sentence, num_of_sentence_for_pronoun_resolution,
                                                    sentences_of_dialogs, dialog_number)

                print("............... more than one sentence for making pro resolution ...............(", (text), ")", "\n")

                resol = pronoun_resolution_allen(text)

                if len(resol) != 0:
                    for i in resol:
                        if "his" in i or "he" in i or "him" in i:
                            for element in i:
                                if len(element.split()) == 1:
                                    if element not in p:
                                        if str(sub2) == " ":
                                            subjects.append(element)
                                        elif str(sub2) != " ":
                                            c = element + " " + str(sub2)
                                            subjects.append(c)
                                elif len(element.split()) == 2:
                                    # like my sister after pronoun resolution should make pronoun again using my rules

                                    ele = check_need_for_more_resol(element, dialog_number, index_of_sentence,
                                                                    sayers_of_dialog)
                                    if ele == " ":
                                        if str(sub2) == " ":
                                            subjects.append(element)
                                        elif str(sub2) != " ":
                                            c = element + " " + str(sub2)
                                            subjects.append(c)
                                    else:
                                        if str(sub2) == " ":
                                            subjects.append(ele)
                                        elif str(sub2) != " ":
                                            c = ele + " " + str(sub2)
                                            subjects.append(c)





            elif str(sub) == "they" or str(sub) == "their":

                text = getting_n_previous_sentences(index_of_sentence, num_of_sentence_for_pronoun_resolution,
                                                    sentences_of_dialogs, dialog_number)

                print("............... more than one sentence for making pro resolution ............... (", (text), ")", "\n")

                resol = pronoun_resolution_allen(text)

                if len(resol) != 0:
                    for i in resol:
                        for element in i:
                            if (" and " in element) and (" they " not in element) and (" their " not in element) and (
                                    element.endswith('and') == False):
                                if element.endswith('they') == False and element.endswith('their') == False:
                                    if len(element.split()) >= 3:
                                        ele = check_need_for_more_resol(element, dialog_number, index_of_sentence,
                                                                        sayers_of_dialog)

                                        if ele == " ":
                                            if str(sub2) == " ":
                                                subjects.append(element)
                                            elif str(sub2) != " ":
                                                c = element + " " + str(sub2)
                                                subjects.append(c)
                                        else:
                                            if str(sub2) == " ":
                                                subjects.append(ele)
                                            elif str(sub2) != " ":
                                                c = ele + " " + str(sub2)
                                                subjects.append(c)


            elif str(sub) == "we" or str(sub) == "our" or str(sub) == "us":

                text = getting_n_previous_sentences(index_of_sentence, num_of_sentence_for_pronoun_resolution,
                                                    sentences_of_dialogs, dialog_number)

                print("............... more than one sentence for making pro resolution ............... (", (text), ")", "\n")

                resol = pronoun_resolution_allen(text)

                if len(resol) != 0:
                    for i in resol:
                        for element in i:
                            if (" and " in element) and (" we " not in element) and (" our " not in element) and (
                                    " us " not in element) and element.endswith('and') == False:
                                if element.endswith('we') == False and element.endswith(
                                        'our') == False and element.endswith('us') == False:
                                    if len(element.split()) >= 3:
                                        ele = check_need_for_more_resol(element, dialog_number, index_of_sentence,
                                                                        sayers_of_dialog)

                                        if ele == " ":
                                            if str(sub2) == " ":
                                                subjects.append(element)
                                            elif str(sub2) != " ":
                                                c = element + " " + str(sub2)
                                                subjects.append(c)
                                        else:
                                            if str(sub2) == " ":
                                                subjects.append(ele)
                                            elif str(sub2) != " ":
                                                c = ele + " " + str(sub2)
                                                subjects.append(c)

                if len(subjects) == 0:
                    subjects.append(my_pronoun_resolution_rules_for_we(sub, sub2, dialog_number, index_of_sentence, sayers_of_dialog,len_of_dialog))

        subjects = list(pd.Series(subjects).drop_duplicates())
        return subjects

