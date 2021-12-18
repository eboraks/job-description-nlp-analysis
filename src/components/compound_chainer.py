#
# Compound Chain is a Spacy pipe that create a chain of compounds token. 
# For example in the sentance "leadership experience in Product Management"
# the chainer will tag "leadership experience" and "Product Management" as compound chains
#
# Auther Eliran Boraks eboraks@gmail.com
# Dec, 18, 2021


import spacy
from spacy.tokens import Token, Span
from spacy.language import Language


@Language.component("compound_chainer")
def find_compounds(doc):
    
    Token.set_extension("is_compound_chain", default=False)

    com_range = []
    max_ind = len(doc)
    for idx, tok in enumerate(doc):
        if((tok.dep_ == "compound") and (idx < max_ind)):
            com_range.append([idx, idx+1])

    to_remove = []
    intersections = []
    for t1 in com_range:
        for t2 in com_range:
            if(t1 != t2):
                s1 = set(t1)
                s2 = set(t2)
                if(len(s1.intersection(s2)) > 0):
                    to_remove.append(t1)
                    to_remove.append(t2)
                    union = list(s1.union(s2))
                    if union not in intersections:
                        intersections.append(union)

    r = [t for t in com_range if t not in to_remove]

    compound_ranges = r + intersections

    spans = [] 
    for cr in compound_ranges:
    # Example cr [[0, 1], [3, 4], [12, 13], [16, 17, 18]]
        entity = Span(doc, min(cr), max(cr)+1, label="compound_chain")

        for token in entity:
            token._.set("is_compound_chain", True)
        spans.append(entity)

    doc.ents = list(doc.ents) + spans
    
    return doc
        
