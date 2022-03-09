from statistics import median_grouped
from tkinter import N
import spacy
import logging as log
from spacy.tokens import DocBin
import pandas as pd
import nltk
from nltk.stem import PorterStemmer
import sys, os, glob
import logging as log
import textacy

from collections import defaultdict
from experience_data_prep.extract_phrases import extract_phrases
from text_util import remove_stop_words, divid_to_ngrams



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

def extract_ngrams_pipe(num: int = 2, min_frequency: int = 1):
    
    ngrams_dict = defaultdict(int)

    # Read the job descriptions
    for file in glob.glob("data/dice*.csv"):
        log.info("Reading file %s", file)
        lnkjobs = pd.read_csv(file)
        nlp_job_descriptions = [nlp(jd) for jd in lnkjobs ["job_desc"]]
        for desc in nlp_job_descriptions:
            ngrams = textacy.extract.basics.ngrams(desc, num, min_freq = min_frequency)
            for ng in ngrams:
                ngrams_dict[ng.text.lower()] += 1
    
    df = pd.DataFrame.from_dict(ngrams_dict, orient='index')
    filename = "data/ngrams_{}_from_job_description.csv".format(num) 
    log.info("Writing file %s", filename)
    df.to_csv(filename, index=True)
        
    



def extract_phrases_pipe():
    # DataFrame to store the extracted phrases results
    df = pd.DataFrame(columns=["Phrases"])

    # Read the job descriptions
    for file in glob.glob("data/dice*.csv"):
        
        # TODO extract job title from file
        log.info("Reading file %s", file)
        lnkjobs = pd.read_csv(file)
        job_descriptions = [jd for jd in lnkjobs ["job_desc"]]

        # TODO divid job description into 

        ## porter = PorterStemmer() , porter.stem("troubling")
        
        phrases = extract_phrases(job_descriptions)
        log.info("Found %s phrases in %s", str(len(phrases)), file)
        df = df.append(pd.DataFrame(phrases, columns=["Phrases"]), ignore_index=True)
        df = df.drop_duplicates(subset=["Phrases"])
    
    df.to_csv("data/verb_noun_phrases.csv", index=False)

    

if __name__ == '__main__':
    sys.exit(extract_ngrams_pipe(num=4, min_frequency=1))