import spacy, textacy
import logging as log
import pandas as pd
import re
import sys, os
import json

nlp = spacy.load("en_core_web_sm")


log.basicConfig(level=log.INFO)

"""
The dedup phrases functions joins sub phrases that are part of the bigger
phrase. For exmaple, the three candidate phrases will be dedup into the actual phrase 

Candidates:
- supports reusable
- supports reusable application
- supports reusable application components

actual phrase:
- supports reusable application components
"""

def dedup_phrases(phrases: list) -> list:
    
    results = set()
    last_index = len(phrases) - 1
    for i, c in enumerate(phrases):
        if i < last_index:
            results.add(dedup_phrase(c, phrases[i+1]))
        else:
            results.add(str(c))
        
    return list(results)

def dedup_phrase(phrase: str, next_phrase: str) -> str:
        
    if((phrase in next_phrase) and (len(phrase) < len(next_phrase))):
        result = next_phrase
    elif((next_phrase in phrase) and (len(next_phrase) < len(phrase))):
        result = phrase
    else:
        result = phrase

    return result


"""
exctrat_phrases function extract phrases from job description. 
The patterns are design to identify noun and verb phrase that can consider 
candidate for job expirence. Example phrases 
"experience delivering solutions"
"roadmap of existing enterprise platforms"

"""
def extract_phrases(texts: list) -> list:
    
    # Regex to clean hits from non alpha numeric characters and hyphens
    regex = re.compile('[^a-zA-Z0-9\-\s]')
    
    patterns = []
    patterns.append([{"POS": "VERB"}, {"POS": {"IN": ["ADP", "ADJ"]}, "OP": "+"}, {"POS":"NOUN", "OP": "+"}])
    patterns.append([{"POS":"NOUN"}, {"POS": {"IN": ["ADP", "ADJ"]}, "OP": "?"}, {"POS": "VERB", "OP": "+"}, {"POS":"NOUN", "OP": "+"}])
    patterns.append([{"POS":"NOUN"}, {"POS": "VERB", "OP": "+"}, {"POS":"PROPN", "OP": "+"}])
    patterns.append([{"POS": "VERB"}, {"POS": "NOUN"}, {"POS": "CCONJ"}, {"POS": {"IN": ["ADP", "ADJ"]}, "OP": "+"}, {"POS": "CCONJ"}, {"POS":"VERB"}])

    records = []

    for desc in texts:
        doc = nlp(desc)
        for pattern in patterns:
            temp_list = []
            verb_chunks = textacy.extract.token_matches(doc, pattern)
            for vc in verb_chunks:
                ## Convert the span into string and append to list
                temp_list.append(regex.sub('', vc.text).strip())
            if len(temp_list) > 0:
                records.extend(dedup_phrases(temp_list))
    
    return records

def main() -> None:
    lnkjobs = pd.read_csv("data/dice_solution_architect_2021-12-14T17:45:56.csv")
    descs = [jd for jd in lnkjobs ["job_desc"]]


if __name__ == '__main__':
    sys.exit(main())
