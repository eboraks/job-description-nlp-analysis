import spacy
from spacy.tokens import Doc
from spacy.language import Language


experience_getter = lambda doc: any(exp in doc.text for exp in ("experience", "Experience"))
Doc.set_extension("has_experience", getter=experience_getter)

nlp = spacy.load("en_core_web_lg")

def skills_one(doc):

    # Finding expirence that is also the sentance root
    experience = ()
    nouns = []
    propn = []
    for i, t in enumerate(doc):
        print((i, t.text, t.pos_, t.dep_))
        if (t.text == "experience" and t.dep_ == "ROOT"):
            experience = (i, t)
            for i, t in enumerate(doc):
                if(i < experience[0] and t.pos_ == "NOUN"):
                    nouns.append(t)
                if(i > experience[0] and t.pos_ == "PROPN"):
                    propn.append(t)
    
    if (nouns and propn):
        print(nouns)
        print(propn)


    return doc



# Experience in programming data/analytic software/languages/tools; e.g., Spark (ML, Mllib, Spark SQL TECHNOLOGY ), R (caret, ggplot2), Python TECHNOLOGY (pandas, numpy, scipy, scikit-learn), Scala, Java TECHNOLOGY , C++, Hive, SQL TECHNOLOGY , Tableau, Alteryx, etc.

# pattern: Noun, Experience, Propnouns
#doc = nlp("Proficient programming experience using SAS Python R.")

# pattern: Experience, VERB, Nouns
#doc = nlp("Experience effectively communicating and presenting data to a variety of audiences required.")

# pattern: Experience, VERBs Nouns
doc = nlp("Experience working with health care administrative claims data (ICD-10, MS-DRG, CPT/ HCPCS ) or electronic medical record data tools")
skills_one(doc)