from event_extraction_.event_extract import *

doc="you and me will married this month ."
doc=nlp(doc)
p1=Rules(doc, verbs_without_need_objects)
text=p1.retrival_senetce_rule1()
print(text)

doc="he passed the bar exam"
doc=nlp(doc)
p2=Rules(doc, verbs_with_objects)
text=p2.retrival_senetce_rule2()
print(text)

doc="i got a surgery"
doc=nlp(doc)
p3=Rules(doc, nouns)
text=p3.retrival_senetce_rule3()
print(text)

doc="i am very sick"
doc=nlp(doc)
p4=Rules(doc, adjectives)
text=p4.retrival_senetce_rule4()
print(text)

doc="my wedding was last year"
doc=nlp(doc)
p5=Rules(doc, noun_direct_relation)
text=p5.retrival_senetce_rule5()
print(text)

doc="i am moving to USA"
doc=nlp(doc)
p6=Rules(doc, verb_with_prepo)
text=p6.retrival_senetce_rule6()
print(text)