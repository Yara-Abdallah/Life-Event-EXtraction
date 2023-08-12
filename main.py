from event_extraction_.event_extract import *
from event_extraction_.subject_extraction import *
from event_extraction_.filtering_rules_conflict import *
from event_extraction_.aggregation_all_results import *
from event_extraction_.pronoun_resolution import *

f = open("Dialogs_data.txt", "r")

subject_result_befor_resolution = []
final_results = []
# counter for index of sentences
index = -1
index_of_sentence_in_dialog = []
index_of_sentences_in_all_dialogs = []
#  dialog number
n = 0
aggreigation_dialog = []


def splitting_sayers_and_sentences():
    sentence = []
    sayers = []
    for line in f:
        stripped_line = line.strip()
        sayer = stripped_line[:stripped_line.find(":")]
        sayers.append(sayer)
        stripped_line = stripped_line[stripped_line.find(":") + 1:]
        sentence.append(stripped_line)
    return sayers, sentence


sayers, sentence = splitting_sayers_and_sentences()


def get_sayers_of_all_dialogs(sayers):
    sayers_of_all_dialogs = []
    sy = []
    for i in sayers:
        if i != "":
            sy.append(i)
        if i == "" and len(sy) != 0:
            sayers_of_all_dialogs.append(sy)
            sy = []
    return sayers_of_all_dialogs


sayers_of_all_dialogs = get_sayers_of_all_dialogs(sayers)


def get_len_of_all_dialogs(sayers):
    len_of_all_dialogs = []
    n = 0
    for i in sayers:
        if i != "":
            n += 1
        if i == "" and len_of_all_dialogs != 0:
            len_of_all_dialogs.append(n)
            n = 0
    return len_of_all_dialogs


len_of_all_dialogs = get_len_of_all_dialogs(sayers)


def get_sentences_of_all_dialogs(sentence):
    sentences_of_all_dialogs = []
    sentences_of_each_dialog = []
    for i in sentence:
        if i != "":
            sentences_of_each_dialog.append(i)
        if i == "":
            sentences_of_all_dialogs.append(sentences_of_each_dialog)
            sentences_of_each_dialog = []
    return sentences_of_all_dialogs


sentences_of_all_dialogs = get_sentences_of_all_dialogs(sentence)


#def final_results_func(sentence,):
for j, i in enumerate(sentence):
    print(sayers[j], " ", i)
    list_tuple = []
    t = i.lower()
    doc = nlp(t)

    if i != "":
        index += 1

        index_of_sentence_in_dialog.append(index)

    # print("dialog_number ....... ",n+1)
    p1 = Rules(doc, verbs_without_need_objects)
    text = p1.retrival_senetce_rule1()
    if text != None:
        list_tuple.append(["Rule1 ", text, findSubs_for_verbEvents(nlp(text[0]), verbs_without_need_objects)])

    p2 = Rules(doc, verbs_with_objects)
    text = p2.retrival_senetce_rule2()
    if text != None:
        list_tuple.append(["Rule2 ", text, findSubs_for_verbEvents(nlp(text[0]), verbs_with_objects)])

    p3 = Rules(doc, nouns)
    text = p3.retrival_senetce_rule3()
    if text != None:
        list_tuple.append(["Rule3 ", text, findSubs_for_nounsEvents(nlp(text[0]), nouns)])

    p4 = Rules(doc, adjectives)
    text = p4.retrival_senetce_rule4()
    if text != None:
        list_tuple.append(["Rule4 ", text, findSubs_for_adjectiveEvents(nlp(text[0]), adjectives)])

    p5 = Rules(doc, noun_direct_relation)
    text = p5.retrival_senetce_rule5()
    if text != None:
        list_tuple.append(["Rule5 ", text, findSubs_for_direct_relation(nlp(text[0]), noun_direct_relation)])

    p6 = Rules(doc, verb_with_prepo)
    text = p6.retrival_senetce_rule6()
    if text != None:
        list_tuple.append(["Rule6 ", text, findSubs_for_actionEvents(nlp(text[0]), verb_with_prepo)])
    # for rules conflict
    filtering(list_tuple)
    # for aggregation all subjects or all events for the sentence
    if aggregation_for_sentence(list_tuple) != None:

        if aggregation_for_sentence(list_tuple)[0] != "":
            b = aggregation_for_sentence(list_tuple)

            if len(b[1]) != 0:
                id__ = str(n + 1) + "_" + str(index)

                print("..................subject result befor resolution.................", b[1], "\n")
                subject_result_befor_resolution.append((b[1], id__))

            # make pronoun resolution for getting the real person name
            resolution = pronoun_resolution_for_all_cases_of_pronouns(b, n, index, sentences_of_all_dialogs,
                                                                      num_of_sentence_for_pronoun_resolution,
                                                                      sayers_of_all_dialogs, len_of_all_dialogs)
            # for aggregating the results of filtering and aggregating sentence with the results of pronoun resolution
            aggrigation = aggregation_between_filtering_and_resolution(b, resolution)

            if len(aggrigation) != 0:
                print(" .....................the final results....................... ", aggrigation, "\n")
                id_ = str(n + 1) + "_" + str(index)
                final_results.append((aggrigation, id_))

    if i == "" and len(index_of_sentence_in_dialog) != 0:
        index_of_sentences_in_all_dialogs.append(index_of_sentence_in_dialog)
        index = -1

        index_of_sentence_in_dialog = []
        n += 1
        print("\n")
