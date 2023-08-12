
import spacy
from spacy import displacy
nlp = spacy.load('en_core_web_sm',disable=['ner','textcat'])


""" keywords of important life events """

# list of (pos=noun) events ... this list for extracting pattern like (possessive pronoun + noun event) ...> (my wedding )
noun_direct_relation=["wedding","anniversary","graduation","birthday","interview","meeting","resignation","job"]

#list of (pos=noun) events ... this list for extracting pattern like (any verb + noun event) ...> (have pain )
nouns=["pain","birth","surgery","job","cold","flu","fever","wedding","meeting","interview","offer","promotion","headache","exam","divorce","contract","relationship","diploma","masters"]#as object to the aux verb

#list of (pos=verb) events ... this list for extracting pattern like (only verb event) ...> (married )
verbs_without_need_objects=["wed","divorce","divorced","elect","engage","die","married","nominate","promote","marry","graduate","bear","hurt","meet","interview"]

#list of (pos=verb) events ... this list for extracting pattern like (moving verb event + preposition) ...> (traveling to)
verb_with_prepo=["move","go","travel"]

#list of (pos=adjectives) events ... this list for extracting pattern like (any verb + adj event) ...> (i am sick)
adjectives=["sick","ill","pregnant"]

#list of (pos=verb) events ... this list for extracting pattern like (verb event + obj) ...> (passed exam ) , both the verb and obj are the event

verbs_with_objects={"celebrate":["birthday","birth","graduation","anniversary","success","news"],
                   "graduate":["collage","school","university"],
                   "win":["support","award","honor","scholarship","prize","lawsuit","pounds","weight"],
                   "lose":["support","award","honor","scholarship","prize","lawsuit","pounds","weight"],
                   "admit":["university","collage","offer","school"],
                   "pass":["exam","test","semester","midterms","school","interview","meeting"],
                   "present":["essay","thesis","reading","statment","presentation","dissertation","project","research","paper"],
                   "discuss":["essay","thesis","reading","statment","presentation","dissertation","project","research","paper"],
                   "defend":["essay","thesis","dissertation","project","research","paper"],
                   "move":["city","home","apartment","town"],
                   "travel":["city","home","apartment","town"],
                   "contract":["agreement","meeting"],
                   "act":["role","series","movie","theater"],
                   "publish":["book","post","cover","copy"],
                   "pregnant":["baby","boy","girl"],
                   "buy":["car","house","phone","laptope"],
                   "accept":["invite","work","school","business ","university","job","offer","college","program","project","research","paper","invitation"],
                   "visit":["hospital","doctor","city","country"],
                   "go":["trip","vacation","holiday"],
                   "sing":["song","album"],
                   "sold":["car","house","phone"],
                   "sign":["deal","contruct"],
                   "finish":["diploma","masters","trip","vacation","holiday","college","university","job","test","exam","school","semester","midterms","album","book","essay","thesis","reading","statment","presentation","dissertation","project","research","paper"],
                   "start":["diploma","masters","trip","vacation","holiday","college","university","job","test","exam","school","semester","midterms","album","book","essay","thesis","reading","statment","presentation","dissertation","project","research","paper"],
                   "break":["leg","arm","finger","neck","head","Back"],
                   "mark":["anniversary","birthday","birth","graduation","success","death"],
                   "fail":["test","exam","school","semester","midterms"]}

pronoun=["my","his","her","their","your"]
prepo=["to","into","in","on","for"]

""" rules for event extraction """

class Rules:
    def __init__(self, text, list_of_keywords=[]):
        self.text = text
        self.list_of_keywords = list_of_keywords
        self.tokens = []
        self.tokens_ = []
        self.pos_tags = []
        self.dependency = []
        self.lemma = []
        for tok in self.text:
            self.tokens.append(tok.text)
            self.tokens_.append(tok)
            self.pos_tags.append(tok.pos_)
            self.dependency.append(tok.dep_)
            self.lemma.append(tok.lemma_)

    """ this rule use the list verbs_without_need_objects for extract the pattern (verb event)...>(married)"""
    def retrival_senetce_rule1(self):
        for i, lemm in enumerate(self.lemma):

            if lemm in self.list_of_keywords and (self.pos_tags[i] == 'VERB'):
                # or self.pos_tags[i]=='ADV' or self.pos_tags[i]=='ADJ' or self.pos_tags[i]=='NOUN'
                return self.text, self.tokens[i]


    """ this rule use the list verbs_with_objects for extract the pattern (verb event + its object)...>(passed exam)"""
    def retrival_senetce_rule2(self):
        for i, lemm in enumerate(self.lemma):
            if lemm in self.list_of_keywords and self.pos_tags[i] == 'VERB':
                for t in self.tokens_[i].rights:
                    if t.dep_ == "dobj" and str(t.lemma_) in self.list_of_keywords[lemm]:
                        return self.text, self.tokens[i] + " " + t.text

                    elif t.dep_ == "dobj":
                        for t1 in t.rights:
                            if t1.dep_ == "prep":
                                for t2 in t1.rights:
                                    if t2.dep_ == "pobj" and str(t2.lemma_) in self.list_of_keywords[lemm]:
                                        return self.text, self.tokens[i] + " " + t2.text

                    elif t.dep_ == "oprd" and str(t.lemma_) in self.list_of_keywords[lemm]:
                        return self.text, self.tokens[i] + " " + t.text

                    elif t.dep_ == "prep":
                        for t1 in t.rights:
                            if t1.dep_ == "pobj" and str(t1.lemma_) in self.list_of_keywords[lemm]:
                                return self.text, self.tokens[i] + " " + t1.text

                            elif t1.dep_ == "pobj":
                                for t4 in t1.lefts:
                                    if t4.dep_ == "compound" and str(t4.lemma_) in self.list_of_keywords[lemm]:
                                        return self.text, self.tokens[i] + " " + t4.text

                for t in self.tokens_[i].lefts:
                    if t.dep_ == "nsubjpass" and str(t) in self.list_of_keywords[lemm]:
                        return self.text, self.tokens[i] + " " + t.text

    """ this rule use the list nouns for extract the pattern ( any verb  + noun event )...>(got surgery)"""
    def retrival_senetce_rule3(self):
        for i, lemm in enumerate(self.lemma):
            if self.pos_tags[i] == 'VERB' or self.pos_tags[i] == 'AUX':
                for t in self.tokens_[i].rights:
                    if t.dep_ == "dobj" and str(t) in self.list_of_keywords:
                        return self.text, self.tokens[i] + " " + t.text

                    elif t.dep_ == "prep":
                        for t1 in t.rights:
                            if t1.dep_ == "pobj" and str(t1) in self.list_of_keywords:
                                return self.text, self.tokens[i] + " " + t1.text

                    elif t.dep_ == "dobj":
                        for t1 in t.rights:
                            if t1.dep_ == "prep":
                                for t2 in t1.rights:
                                    if t2.dep_ == "pobj" and str(t2) in self.list_of_keywords:
                                        return self.text, self.tokens[i] + " " + t2.text

    """ this rule use the list adjectives for extract the pattern ( any verb  + adjectives event )...>(am sick)"""
    def retrival_senetce_rule4(self):
        for i, lemm in enumerate(self.lemma):
            if self.pos_tags[i] == "AUX":
                for t in self.tokens_[i].rights:
                    if t.dep_ == "acomp" and str(t) in self.list_of_keywords and t.pos_ == "ADJ":
                        print("ad ", t.text)
                        return self.text, self.tokens[i] + " " + t.text


            elif self.pos_tags[i] == "VERB":
                for t in self.tokens_[i].rights:
                    if t.dep_ == "oprd" and str(t) in self.list_of_keywords and (t.pos_ == "NOUN" or t.pos_ == "ADJ"):
                        return self.text, self.tokens[i] + " " + t.text

    """ this rule use the list noun_direct_relation for extract the pattern ( possessive pronoun  + noun event )...>(my graduation)"""
    def retrival_senetce_rule5(self):
        for i, lemm in enumerate(self.lemma):
            if (self.pos_tags[i] == "PRON" or self.pos_tags[i] == "PROPN"):
                head = self.tokens_[i].head
                if self.tokens_[i].dep_ == "poss" and str(head) in self.list_of_keywords and head.pos_ == "NOUN":
                    return self.text, self.tokens[i] + " " + head.text

                elif self.tokens_[i].dep_ == "poss" and head.pos_ == "NOUN":
                    for t in head.lefts:
                        if str(t) in self.list_of_keywords and t.dep_ == "compound":
                            return self.text, self.tokens[i] + " " + t.text


    """ this rule use the list verb_with_prepo for extract the pattern ( moving verb event + preposition )...>(moving to)"""
    def retrival_senetce_rule6(self):
        for i, lemm in enumerate(self.lemma):
            if lemm in self.list_of_keywords and self.pos_tags[i] == 'VERB':
                for t in self.tokens_[i].rights:
                    if t.dep_ == "prep" and str(t) in prepo:
                        return self.text, self.tokens[i] + " " + t.text
                """for t in self.tokens_[i].lefts:
                    if t.dep_=="aux" and str(t) == "to":
                        return None"""




"""

"""