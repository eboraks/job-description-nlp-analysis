import spacy
from spacy.util import filter_spans
from spacy.tokens import Span
from spacy.language import Language
import re


## TODO: use this script to generate a list of experience sentances that can be use to analysis and building of DependencyMatchers


def search_doc(doc, pattern, label):

    new_ents = []
    original_ents = list(doc.ents)
    for match in re.finditer(pattern, doc.text):
        start, end = match.span()
        span = doc.char_span(start, end)
        if span is not None:
            new_ents.append((span.start, span.end, span.text))
    for ent in new_ents:
        start, end, name = ent
        per_ent = Span(doc, start, end, label=label)
        original_ents.append(per_ent)
    filtered = filter_spans(original_ents)
    doc.ents = filtered
    return (doc)





@Language.component("find_soft_skills")
def find_soft_skill(doc):
    ## I think this section need to be renamed to experience instead of skills
    l = [ 
            "problem[a-z]+\bsolver", 
            "develop", 
            "driv", 
            "strateg",
            "preset",
            "desgin",
            "proactiv",
            "collaborat",
            "adviser",
            "coach",
            "plan"
        ]
    pattern = r"(leader|launch|drive|develop|strateg|present|design|build|proactive|collaborat|adviser|coach|problem[a-z]+\bsolv)[a-z]*\b"
    label = "SOFT_SKILL"
    return search_doc(doc, pattern, label)


@Language.component("find_artifacts")
def find_artifacts(doc):
    pattern = r"(roadmap|product|plan|strategy|architecture|big.*picture|solution|process|project.*plan)[a-z]*\b"
    label = "ARTIFACT"
    return search_doc(doc, pattern, label)


# HDFS, file, database, JSON, HTML, Spark (ML, Mllib, Spark SQL TECHNOLOGY ), R (caret, ggplot2), Python TECHNOLOGY (pandas, numpy, scipy, scikit-learn), Scala, Java TECHNOLOGY , C++, Hive, SQL TECHNOLOGY , Tableau, Alteryx, etc.
@Language.component("find_technologies")
def find_technologies(doc):
    pattern = r"(SQL|BI.*[T|t]ool|Java|Python|GraphQL|REST|microservice|API|MongoDB|Cassandra|RDBMS|ORACLE)[a-z]*\b"
    label = "TECHNOLOGY"
    return search_doc(doc, pattern, label)
    

