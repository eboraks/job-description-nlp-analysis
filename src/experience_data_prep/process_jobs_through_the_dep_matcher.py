import spacy
import logging as log
from spacy.tokens import DocBin
import pandas as pd
import nltk
import sys, os, glob
import logging as log

from experience_data_prep.extract_phrases import extract_phrases


log.basicConfig(level=log.INFO)

# Initiating the Spacy model adding to it custom annotators
nlp = spacy.load("en_core_web_sm")

log.basicConfig(level=log.INFO)

def annotate(text):
    doc = nlp(text)
    annotations = []
    for ent in doc.ents:
        annotations.append((ent.start_char, ent.end_char, ent.label_))

    if annotations:
        return (text, annotations)
    else:
        return None


def texts_to_annotated_docs(docs):
    
    sent_counter = 0
    ents_counter = 0
    results = []
    for jd in docs:
        for sent in nltk.sent_tokenize(jd):
            sent_counter += 1
            doc = nlp(sent)
            if doc.ents:
                ents_counter += len(doc.ents)
                results.append(doc)
                
    log.info("%s documents with %s annotations found", str(len(results)), ents_counter)
    
    return results

def save_docbin(name, docs):
    
    counter = 0
    docBin = DocBin()
    for doc in docs:
        counter += 1
        docBin.add(doc)

    file = "data/"+name+".spacy"
    log.info("Saving spacy dataset - %s. With %s docs", file, str(counter))
    docBin.to_disk(file)
    log.info("Saved spacy dataset - %s", file)

def annotate_data(path) -> list:

    job_postings = pd.read_csv(path)
    jobdescs = [jd for jd in job_postings["job_desc"]]
    
    # Generate spacy doc with annotation from custom pipes
    docs = texts_to_annotated_docs(jobdescs)
    
    return docs


def main():
    # DataFrame to store the extracted phrases results
    df = pd.DataFrame(columns=["Phrases"])

    # Read the job descriptions
    for file in glob.glob("data/dice*.csv"):
        log.info("Reading file %s", file)
        lnkjobs = pd.read_csv(file)
        job_descriptions = [jd for jd in lnkjobs ["job_desc"]]
        phrases = extract_phrases(job_descriptions)
        log.info("Found %s phrases in %s", str(len(phrases)), file)
        df = df.append(pd.DataFrame(phrases, columns=["Phrases"]), ignore_index=True)
        df = df.drop_duplicates(subset=["Phrases"])
    
    df.to_csv("data/verb_noun_phrases.csv", index=False)

    

if __name__ == '__main__':
    sys.exit(main())