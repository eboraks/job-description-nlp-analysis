import spacy
import components.compound_chainer

nlp = spacy.load("en_core_web_lg")
nlp.add_pipe("compound_chainer")
print(nlp.pipe_names)
doc = nlp("Experience developing product roadmaps for data and/or technical solutions in a B2B environment.")

for token in doc:
    print((token.text, token._.is_compound_chain))