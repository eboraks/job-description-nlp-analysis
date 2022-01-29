import spacy
from spacy.matcher import DependencyMatcher

nlp = spacy.load("en_core_web_sm")
matcher = DependencyMatcher(nlp.vocab)
pattern = [
  {
    "RIGHT_ID": "anchor_founded",       # unique name
    "RIGHT_ATTRS": {"ORTH": "founded"}  # token pattern for "founded"
  },
  {
    "LEFT_ID": "anchor_founded", 
    "REL_OP": ">",
    "RIGHT_ID": "founded_subject",
    "RIGHT_ATTRS": {"DEP": "nsubj"},  
  },
  {
    "LEFT_ID": "anchor_founded", 
    "REL_OP": ">",
    "RIGHT_ID": "founded_object",
    "RIGHT_ATTRS": {"DEP": "dobj"},  
  },
  {
    "LEFT_ID": "founded_object",
    "REL_OP": ">",
    "RIGHT_ID": "founded_object_modifier",
    "RIGHT_ATTRS": {"DEP": {"IN": ["amod", "compound"]}},
  }
]
matcher.add("FOUNDED", [pattern])
doc = nlp("Williams initially founded an insurance company in 1987.")
matches = matcher(doc)
print(matches) # [(4851363122962674176, [1])]

match_id, token_ids = matches[0]
for i in range(len(token_ids)):
    print(pattern[i]["RIGHT_ID"] + ":", doc[token_ids[i]].text)