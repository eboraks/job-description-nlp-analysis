import sys
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.util import ngrams
from collections import Counter

## global stop work object
stop_words = set(stopwords.words('english'))


## Get a list of text and retrun dict with tokens (word) counts 
def token_counter(texts: list) -> Counter:
    tokens = []
    for text in texts:
        tokens.extend(word_tokenize(text.lower()))

    return Counter(tokens)

def remove_stop_words(text: str) -> str:
    tokens = word_tokenize(text)
    clean = [w for w in tokens if not w.lower() in stop_words]
    return " ".join(clean)

def divid_to_ngrams(text: str, n_gram: int) -> str:
    ng = ngrams(word_tokenize(text), n_gram)
    return [" ".join(gram) for gram in ng]


if __name__ == '__main__':
    r = divid_to_ngrams("This google is a test string with she he yours Amazon Amazon Apple Eliran Google Google google", 4)
    print(r)
    sys.exit()