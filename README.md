# job-description-nlp-analysis
A project is dedicated to learning different NLP technologies while analyzing job descriptions. 

What problem? How to identify soft or implicit skills in the job description. Example of soft skills phrases I am after: 
- provide technical leadership
- apply strategic thinking
- delivering high-quality software
- invest in strategic modernization

## Methodology 
Since this is a work-in-a-progress learning project, the methodology I am applying keeps involved as I progress. 

Public available NER models are not trained to identify such specific parts of the text. My first attempt was to annotate training data manually. Still, I pretty quickly concluded that to get a large enough sample, I would need to invest a lot of time, and I decided to try to find a way to better way or a more exciting way to generate training data. 

### Step 1: Identifying Linguistic Features Soft Skills Phrases
I used Spacy.io's dependency tree to find linguistics features common to the phrases I am after. Here are four patterns that show promise: 
```
patterns.append([{"POS": "VERB"}, {"POS": {"IN": ["ADP", "ADJ"]}, "OP": "+"}, {"POS":"NOUN", "OP": "+"}])
patterns.append([{"POS":"NOUN"}, {"POS": {"IN": ["ADP", "ADJ"]}, "OP": "?"}, {"POS": "VERB", "OP": "+"}, {"POS":"NOUN", "OP": "+"}])
patterns.append([{"POS":"NOUN"}, {"POS": "VERB", "OP": "+"}, {"POS":"PROPN", "OP": "+"}])
patterns.append([{"POS": "VERB"}, {"POS": "NOUN"}, {"POS": "CCONJ"}, {"POS": {"IN": ["ADP", "ADJ"]}, "OP": "+"}, {"POS": "CCONJ"}, {"POS":"VERB"}])
``` 
[code: extract_phrases.py](src/experience_data_prep/extract_phrases.py)  or [VERB NOUN Phrases Extractor Notebook](notebook/VERB_NOUN_Phrase_Extractor.ipynb)

The patterns extract pretty good results, but the results also include phrases that don't describe soft skills, so the next step is to separate the wheat from the chaff. 

```
Experience developing product roadmaps
developing new capabilities
vaccinated against COVID-19 *
protected by law * 
develop creative solutions
plans into phased actions *
build new capabilities
overcome complex systems integration challenges
power of emerging technologies
principles to developing marketing technology solutions
incorporate key technologies

Note: * represent chaff phrases that don't represent skills
```

These days I am experimenting with different clustering algorithms to group cluster phrases's vectors to separate the what (skill phrase) from the chaff (unrelated to skills phrases). [Vectorize and Cluster Phrases Notebook](notebook/Vectorize_and_Cluster_Phrases.ipynb)





