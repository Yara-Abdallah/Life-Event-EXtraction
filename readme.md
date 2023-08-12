
# Life Event Extraction

The approach to addressing this requirement has been successfully accomplished across four distinct stages:

- Identifying the most important events.
  

                  {
                  "celebrate":["birthday","birth","graduation","anniversary","success","news"],

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
                   
                   "finish":["diploma","masters","trip","vacation","holiday","college","university","job","test","exam","school","semester",
                  
                   "midterms","album","book","essay","thesis","reading","statment","presentation","dissertation","project","research","paper"],
                   
                   "start":["diploma","masters","trip","vacation","holiday","college","university","job","test","exam","school","semester","midterms",
                   
                   "album","book","essay","thesis","reading","statment","presentation","dissertation","project","research","paper"],
                   
                   "break":["leg","arm","finger","neck","head","Back"],
                   
                   "mark":["anniversary","birthday","birth","graduation","success","death"],
                   
                   "fail":["test","exam","school","semester","midterms"]
                   }


- Event extraction.

1-  The first rule retrieves a pattern of the form.
   
     [verb event]

2-  The second rule retrieves a pattern of the form.

    [verb event + object].

3-  The third rule retrieves a pattern of the form.
    
    [any verb + noun event].

4-  The fourth rule retrieves a pattern of the form.
    
    [any verb + adjective event].

5-  The fifth rule retrieves a pattern of the form.
    
    [possessive pronoun + noun event].

6-  The sixth rule retrieves a pattern of the form.
    
    [moving verb + preposition].

- Subject extraction.

1-  If the verb is in the active voice and the subject represents a specific person.

    Susan is going to get a divorce  →  [Susan]  

2-  If the verb is in the passive voice and is accompanied by the word "by" the subject comes after "by" .

    The car was bought by Jhon → [Jhon]

3-  If the event is in the passive voice and the sentence does not contain the word "by",should check if the subject is a person's name or a pronoun representing them.
  
    When we got married in my hometown →  [we]

4-  the subject might be indicated in the object pronoun.
  
    The Roman Studio interviewed me  →  [me]

5-  the event's subject can be deduced from another dependent verb if it doesn't fit the aforementioned scenarios.
   
    She passed her exam and married  →  [she] 

6-  the subject is expressed by the possessive pronoun.
  
    Today is my 11th wedding anniversary → [my] 

(( Event and subject extraction are conducted using rules grounded in both part-of-speech tagging and dependency trees, utilizing the Spacy library ))

- Pronoun resolution.

During this phase, we leveraged the AllenNLP Predictor.
This tool offers a range of classifiers, each associated with names and pronouns that are interconnected. 
Afterwards, filtering rules were developed to process the output,these rules played a critical role in identifying the explicit noun associated with each pronoun.

## requirement 

[AllenNLP](https://storage.googleapis.com/allennlp-public-models/coref-spanbert-large-2021.03.10.tar.gz)

-------------------------------------------------------------------------------------------------------------------------------------------
[Stanford NER](https://github.com/amiangshu/SentiSE/blob/master/edu/stanford/nlp/models/ner/english.all.3class.caseless.distsim.crf.ser.gz)

-------------------------------------------------------------------------------------------------------------------------------------------


