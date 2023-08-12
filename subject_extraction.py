import spacy
from collections import Counter
import pandas as pd
import os
from nltk.tag import StanfordNERTagger
from event_extraction_.event_extract import *

java_path = "Java/jre1.8.0_251/bin/java.exe"
os.environ['JAVAHOME'] = java_path

st = StanfordNERTagger(r'SentiSE-master(1)/SentiSE-master/edu/stanford/nlp/models/ner/english.all.3class.caseless.distsim.crf.ser.gz',
                           r'stanford-ner-2020-11-17/stanford-ner.jar',
                           encoding='utf-8')



nlp = spacy.load('en_core_web_sm',disable=['ner','textcat'])
SUBJECTS = ["nsubj", "nsubjpass", "csubj", "csubjpass", "agent", "expl"]
OBJECTS = ["dobj", "dative", "attr", "oprd"]
ADJECTIVES = ["acomp", "advcl", "advmod", "amod", "appos", "nn", "nmod", "ccomp", "complm","hmod", "infmod", "xcomp", "rcmod", "poss"," possessive"]
COMPOUNDS = ["compound"]
PREPOSITIONS = ["prep"]
obj_pronoun = ["me", "him", "her", "them", "you", "us"]
p_pronoun = ["my", "his", "her", "their", "your", "our"]
p = ["i", "we", "you", "they", "he", "she", "my", "his", "her", "their", "your", "our", "me", "him", "them"]



"""using caseless models for checking if the subject is person or not .. when subject is all lower case or capital """
def is_person(text, subject, st=st):
    x = 0
    tokens = []
    for token in text:
        tokens.append(token)
    for i, token in enumerate(tokens):
        if str(token) == str(subject):
            lis = str(text).split()
            for i, j in enumerate(lis):
                j = j.replace("'s", "")
                lis[i] = j
            # print(lis)

            # print(tagged)
            if token.pos_ == "NOUN":
                tagged = st.tag(lis)
                for i, j in enumerate(tagged):
                    if 'PERSON' in j:
                        if str(j[0]) == str(subject):
                            return True
                        if str(j[0]) != str(subject):
                            return False
                for i, j in enumerate(tagged):
                    if 'PERSON' not in j:
                        x += 1
                        if x == len(tokens):
                            return False

            elif token.pos_ == "PRON" and (str(token) in p):
                return True
            elif token.pos_ == "PRON" and (str(token) not in p):
                return False

            elif token.pos_ == "PROPN":
                return True


"""take verb token and sentence then return the object of the verb"""
def find_obj_for_verb(doc, verb):
    tokens = []
    for token in doc:
        tokens.append(token)
    for i, token in enumerate(tokens):
        if str(token) == str(verb):
            for t in tokens[i].rights:
                if t.dep_ == "dobj":
                    return t

                elif t.dep_ == "prep":
                    for t1 in t.rights:
                        if t1.dep_ == "pobj":
                            return t1

            for t in tokens[i].lefts:
                if t.dep_ == "nsubjpass":
                    if token.n_rights > 0:
                        for t1 in token.rights:
                            if t1.dep_ == "agent":
                                return t

""" take subject token then return the other subjects that combine them with and conjunction """
def getSubsFromConjunctions(subs):
    moreSubs = []
    rightDeps = []
    for sub in subs:
        for tok in sub.rights:
            if tok.dep_ == "conj":
                #
                subs = chek_pronoun_verb(tok)
                moreSubs.append(subs)
            if len(moreSubs) > 0:
                moreSubs.extend(getSubsFromConjunctions(moreSubs))
    return moreSubs

""" for checking if the subject has possessive pronoun then return it (my brother) ...> my , this step important for pronoun resolution  """
def chek_pronoun_verb(tok):
    if tok.n_lefts > 0:
        for s in (tok.lefts):
            if (s.dep_ == "poss") and str(s) in p_pronoun:
                return s
            elif (s.dep_ == "poss") and (s.pos_ == "PROPN" or s.pos_ == "NOUN"):
                return s
            else:
                return tok
    else:
        return tok



"""take verb token and sentence then return the subject of the verb"""
def find_sub_for_verb(doc, verb):
    tokens = []
    subs = []
    objs = []
    s = []
    e = []
    p = []
    for token in doc:
        tokens.append(token)

    """when passive verb (but there is no by phrase) or Informative verb  ...> jhon graduated yesterday , subject is (jhon)"""
    for i, token in enumerate(tokens):
        if str(token) == str(verb):
            for tok in token.lefts:
                if tok.dep_ == "auxpass":
                    if tok.pos_ == 'AUX':
                        for t1 in tok.lefts:
                            if t1.dep_ == "nsubj" or t1.dep_ == "nsubjpass":
                                subs.append(t1)


                elif tok.dep_ == "nsubjpass":
                    """when passive verb (but there is by phrase) ...> the car was bought by jhon , subject is (jhon) """

                    objs.append(tok)
                    if token.n_rights > 0:
                        for t in token.rights:
                            if t.dep_ == "agent":
                                for t1 in t.rights:
                                    if t1.dep_ == "pobj":
                                        subs.append(t1)
                            else:
                                subs.append(tok)

                    else:
                        subs.append(tok)


                elif tok.dep_ == "nsubj":

                    """when Informative verb , checking if subject person or not...> (jhon graduated yesterday) , subject is (jhon) ,if we have (people divorced alot) the subject is () because people not person """
                    if is_person(doc, tok) == True:
                        subs.append(tok)

                    else:

                        for t3 in tok.lefts:
                            if t3.dep_ == "poss" and (t3.pos_ == "NOUN" or t3.pos_ == "PROPN" or t3.pos_ == "PRON"):
                                subs.append(tok)
                            else:
                                for t2 in token.rights:
                                    if t2.dep_ == "nsubj":
                                        # if is_person(doc,t2)==True:
                                        subs.append(t2)

        #  get to finish his masters
        """when no of the above rules work , return the subject of aux verb of our verb...> kareem get to finish his masters , subject is (kareem)"""
        if len(subs) == 0:
            if token.dep_ == "acomp" or token.dep_ == "xcomp":
                head = token.head
                if head.pos_ == "VERB" or head.pos_ == "AUX":
                    for t in head.lefts:
                        if t.dep_ == "nsubj" or t.dep_ == "nsubjpass":
                            subs.append(t)

            elif token.dep_ == "conj":
                """when no of the above rules work ,return the subject of the verb which conjunctioned on present verb ...> sally married and passed exam , subject of passed verb is (sally) """
                # print("conj 1")
                h = token.head
                if h.pos_ == "VERB":
                    sub = find_sub_for_verb(doc, h)[0]
                    if sub:
                        subs.append(sub)
                    else:
                        subs.append(None)

        if len(subs) > 0:
            subs = list(pd.Series(subs).drop_duplicates())
            subs.extend(getSubsFromConjunctions(subs))
            for i in subs:
                s.append(chek_pronoun_verb(i))

            for i in s:
                if is_person(doc, i) == False:
                    s.remove(i)

            for i in range(len(s)):
                if s[i] != subs[i] and str(s[i]) in p_pronoun:
                    p.append((s[i], subs[i]))
                elif s[i] != subs[i] and (s[i].pos_ == "PROPN" or s[i].pos_ == "NOUN"):
                    p.append((s[i], subs[i]))

                elif s[i] == subs[i]:

                    p.append(s[i])
                else:
                    p.append(s[i])
                    p.append(subs)

            return p



"""return the subject of events which their patterns extraction from Rule 2 or 1 , the subject here is the subject of the verb event (i married )..> subjects (i)"""
def findSubs_for_verbEvents(doc, list_=[]):
    subs = []
    objs = []
    for token in doc:
        if token.pos_ == "VERB" and str(token.lemma_) in list_:
            obj = find_obj_for_verb(doc, token)
            sub = find_sub_for_verb(doc, token)
            if sub:
                return sub

            else:
                """when the rule failed in finding the subject and there is a refrence on it , in the object pronoun ...>(the studio interviwed me) , subject is (me)"""
                if obj != None:
                    if str(obj) in obj_pronoun:
                        return [obj]

                    """elif obj.n_lefts > 0:
                        #when the rule failed in finding the subject and there is a refrence on it , in the object possisave pronoun ...>(definding my thesis) , subject is (my)
                        for t in obj.lefts :
                            if t.dep_=="poss" and str(t) in p_pronoun :
                                 #[(t,obj)]
                                 return [(t,obj)]"""

"""return the subject of events which their patterns extraction from Rule 5 , the subject here is the possisave pronoun (my wedding )..> subjects (my)"""
def findSubs_for_direct_relation(doc, list_=[]):
    tokens = []
    subs = []
    for token in doc:
        tokens.append(token)
    for i, token in enumerate(tokens):
        if (tokens[i].pos_ == "PRON" or tokens[i].pos_ == "PROPN"):
            head = tokens[i].head
            if tokens[i].dep_ == "poss" and str(head) in list_ and head.pos_ == "NOUN":
                subs.append(token)

            elif tokens[i].dep_ == "poss" and head.pos_ == "NOUN":
                for t in head.lefts:
                    if str(t) in list_ and t.dep_ == "compound":
                        subs.append(token)
        if len(subs) > 0:
            return subs


"""return the subject of events which their patterns extraction from Rule 3 , the subject here is the subject of the verb which the event related to it(i had surgery )..> subjects (i)"""
def findSubs_for_nounsEvents(doc, list_=[]):
    tokens = []
    subs = []
    for token in doc:
        tokens.append(token)
    for i, token in enumerate(tokens):
        if str(token) in list_:

            s = chek_pronoun_verb(token)
            if str(s) == str(token):

                for i, token in enumerate(tokens):
                    if tokens[i].pos_ == 'VERB' or tokens[i].pos_ == 'AUX':
                        obj = find_obj_for_verb(doc, token)
                        sub = find_sub_for_verb(doc, token)
                        for t in tokens[i].rights:
                            if t.dep_ == "dobj" and str(t) in list_:
                                if sub:
                                    if len(sub) > 0:
                                        return sub


                            elif t.dep_ == "prep":
                                for t1 in t.rights:
                                    if t1.dep_ == "pobj" and str(t1) in list_:
                                        if sub:
                                            if len(sub) > 0:
                                                return sub

                            elif t.dep_ == "dobj":
                                for t1 in t.rights:
                                    if t1.dep_ == "prep":
                                        for t2 in t1.rights:
                                            if t2.dep_ == "pobj" and str(t2) in list_:
                                                if sub:
                                                    if len(sub) > 0:
                                                        return sub

            elif s != None and str(s) != str(token):
                return [s]


"""return the subject of events which their patterns extraction from Rule 4 , the subject here is the subject of the verb which the event related to it(i am sick )..> subjects (i)"""
def findSubs_for_adjectiveEvents(doc, list_=[]):
    tokens = []
    subs = []
    for token in doc:
        tokens.append(token)
    for i, token in enumerate(tokens):
        if tokens[i].pos_ == "AUX":
            obj = find_obj_for_verb(doc, token)
            sub = find_sub_for_verb(doc, token)
            for t in tokens[i].rights:
                if t.dep_ == "acomp" and str(t) in list_ and t.pos_ == "ADJ":
                    if sub:
                        if len(sub) > 0:
                            return sub

        elif tokens[i].pos_ == "VERB":
            obj = find_obj_for_verb(doc, token)
            sub = find_sub_for_verb(doc, token)
            for t in tokens[i].rights:
                if t.dep_ == "oprd" and str(t) in list_ and (t.pos_ == "NOUN" or t.pos_ == "ADJ"):
                    if sub:
                        if len(sub) > 0:
                            return sub


"""return the subject of events which their patterns extraction from Rule 6 , the subject here is the subject of the moving event verb (i going to USA )..> subjects (i)"""
def findSubs_for_actionEvents(doc, list_=[]):
    tokens = []
    subs = []
    for token in doc:
        tokens.append(token)
        for i, token in enumerate(tokens):
            if str(tokens[i].lemma_) in list_ and tokens[i].pos_ == 'VERB':
                obj = find_obj_for_verb(doc, token)
                sub = find_sub_for_verb(doc, token)
                for t in tokens[i].rights:
                    if t.dep_ == "prep":
                        if sub:
                            if len(sub) > 0:
                                return sub


"""


"""