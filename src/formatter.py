# -*- coding: utf-8 -*-
"""
Custom formatter to clean punctuation, hyphens, and other non-alphabetic characters from text. Also converts the text to lowercase.
"""

# Importing regex engine for formatting
import re

# Importing nltk for word filtering
import nltk

#import spacy
#from spacy import displacy
#NER = spacy.load("en_core_web_sm")

# Downloading both a corpus of all words/names in the English Language
nltk.download('words')

# Instantiating the constant the set of all words in the nltk word corpus
WORD_SET = nltk.corpus.words.words()
for i in range(len(WORD_SET)):
    WORD_SET[i] = WORD_SET[i].lower()

WORD_SET = set(WORD_SET)

def format_text(text):
    """
    Removes non-alphabetic characters, punctuation, excess whitespace, and capital letters from text.

    Example: "The   quick-brown 34fox22! (@$say@S) Hello world!" -> "the quick brown fox says hello world"
    """

    # Replacing hyphenated words with their space-separated counterparts
    formatted_text = re.sub("-", " ", text)

    # Normalizing newlines and large whitespace to be a single space (for parsing)
    formatted_text = re.sub("(\n|\s{2,})", " ", formatted_text)

    # Removing all non-alphabetic characters from the dataset. Note: This assumes that all tokens are either fully special characters or
    # fully alphabetic. If this assumption does not hold true this may result in partial words being kept
    formatted_text = "".join(char for char in formatted_text if char.isalpha() or char == " ")
    formatted_text = formatted_text.lower()

    # Removing non-English words from the text
    formatted_text = removeNonWords(formatted_text)

    # TODO: Test the effect of including name filtering
    # Removing proper nouns (i.e. Names) from the text
    # formatted_text = removeNamedEntities(formatted_text)

    return formatted_text

def removeNamedEntities(text):

    #tagged_text = NER(text)
    #filtered_text = " ".join([token.text for token in tagged_text.ents if token.label_.lower() in ["person"]])
    #return filtered_text
    pass
                            
def removeNonWords(text):
    filtered_sentence = " ".join([token for token in text.split() if token in WORD_SET or (token[-1] == 's' and token[:-1] in WORD_SET)])
    return filtered_sentence