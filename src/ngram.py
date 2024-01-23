# -*- coding: utf-8 -*-
"""
Parse ngram (unigram, bigram, trigram, quadgram, quintagram) letter statistics for books, with and without spaces
"""

import os
import json
import io
from collections import defaultdict

# TODO: Make unigram, bigram, trigram, quadgram, and quintagram letter stats
# TODO: Have a version of these letter stats that includes spaces and a version that ignores them
# TODO: Have the program also do word counts and organize them by frequency

# TODO: For heuristic search (genetic algo), have mutation letters be selected with probability proportional to loss function of the characters
# TODO: Loss function of the characters can be deviation from unigram frequency plus deviation from bigram and trigram frequency for which the char is a part of
# The loss for bigram/trigram is doubled and tripled if the letter is repeated
# TODO: Since we know spaces (in the spaced variant) we should not include spaces in our unigram statistics and should seperate bigram and trigram
# arrangements where a space is present. A separate statistical distribution per position of the space
# TODO: Simple counting algo of for i in range(len(book)): book[i], book[i-1:i], book[i-2:i] should suffice here, not counting special case for spaces
# TODO: For unspaced variant just do spaced on a book text that has removed spaces from it
# Num books (initial): 2343

def generateAllNgramCounts(path_to_text_dir="./data/text/", path_to_counts_dir="./data/counts/", spacesRemoved=False):
    processedCounts = 0

    if spacesRemoved:
        path_to_counts_dir += "spaceless/"
    else:
        path_to_counts_dir += "spaced/"

    for file in os.listdir(path_to_text_dir):
        if file.endswith(".txt"):
            path_to_text_file = path_to_text_dir + file
            PG_Number = int(path_to_text_file.split("/")[-1].split("_")[0][2:])

                
            with open(path_to_text_file, "r", encoding="UTF-8") as file:
                text = file.read()

            if spacesRemoved:
                text = text.replace(" ", "")

            generateNgramCount(PG_Number, text, path_to_counts_dir)

            processedCounts += 1
            print("Processed %d counts..." % processedCounts, end="\r")
    print("Successfully finished processing counts!")

def generateNgramCount(PG_Number,
                        text,
                        path_to_counts_dir=None,
                        ):

    ngramCounts = defaultdict(lambda: 0)
    unigramTotal = 0
    bigramTotal = 0

    # Statistics for bigrams of the form " x"
    bigramSpaceOneTotal = 0

    # Statistics for bigrams of the form "x "
    bigramSpaceTwoTotal = 0

    # Statistics for trigrams without spaces
    trigramTotal = 0

    # Statistics for trigrams of the form " xx"
    trigramSpaceOneTotal = 0

    # Statistics for trigrams of the form "x x"
    trigramSpaceTwoTotal = 0
    
    # Statistics for trigrams of the form "xx "
    trigramSpaceThreeTotal = 0

    # Statistics for trigrams of the form " x "
    trigramSpaceOneThreeTotal = 0

    for i in range(len(text)):

        if text[i] != " ":
            ngramCounts[text[i]] += 1
            unigramTotal += 1

        if i > 0:
            bigram = text[i-1:i+1]
            ngramCounts[bigram] += 1

            if bigram[0] == " ":
                bigramSpaceOneTotal += 1

            elif bigram[1] == " ":
                bigramSpaceTwoTotal += 1

            else:
                bigramTotal += 1
        
        if i > 1:
            trigram = text[i-2: i+1]
            ngramCounts[trigram] += 1

            if trigram[1] == " ":
                trigramSpaceTwoTotal += 1

            elif trigram[0] == " " and trigram[2] == " ":
                trigramSpaceOneThreeTotal += 1

            elif trigram[0] == " ":
                trigramSpaceOneTotal += 1

            elif trigram[2] == " ":
                trigramSpaceThreeTotal += 1

            else:
                trigramTotal += 1

    ngramData = {"Counts": ngramCounts,
                 "unigramTotal": unigramTotal,
                 "bigramTotal": bigramTotal,
                 "bigramSpaceOneTotal": bigramSpaceOneTotal,
                 "bigramSpaceTwoTotal": bigramSpaceTwoTotal,
                 "trigramTotal": trigramTotal,
                 "trigramSpaceOneTotal": trigramSpaceOneTotal,
                 "trigramSpaceTwoTotal": trigramSpaceTwoTotal,
                 "trigramSpaceThreeTotal": trigramSpaceThreeTotal,
                 "trigramSpaceOneThreeTotal": trigramSpaceOneThreeTotal
                 }

    # write text file
    target_file = os.path.join(path_to_counts_dir,"PG%s_counts.json"%PG_Number)
    with io.open(target_file,"w", encoding="UTF-8") as f:
        json.dump(ngramData, f, indent=4)


def aggregateCounts(path_to_counts_dir="data/counts/", path_to_ngram_dir="data/ngram/", spacesRemoved=False):

    aggregateCounts = defaultdict(lambda: 0)
    unigramTotal = 0
    bigramTotal = 0

    # Statistics for bigrams of the form " x"
    bigramSpaceOneTotal = 0

    # Statistics for bigrams of the form "x "
    bigramSpaceTwoTotal = 0

    # Statistics for trigrams without spaces
    trigramTotal = 0

    # Statistics for trigrams of the form " xx"
    trigramSpaceOneTotal = 0

    # Statistics for trigrams of the form "x x"
    trigramSpaceTwoTotal = 0
    
    # Statistics for trigrams of the form "xx "
    trigramSpaceThreeTotal = 0

    # Statistics for trigrams of the form " x "
    trigramSpaceOneThreeTotal = 0

    if spacesRemoved:
        path_to_counts_dir += "spaceless/"
    else:
        path_to_counts_dir += "spaced/"

    for file in os.listdir(path_to_counts_dir):
        if file.endswith(".json"):
            with io.open(path_to_counts_dir+file,"r") as countFile:
                countJSON = json.load(countFile)

            for ngram, count in countJSON["Counts"].items():
                aggregateCounts[ngram] += count
            
            unigramTotal += countJSON["unigramTotal"]
            bigramTotal += countJSON["bigramTotal"]
            trigramTotal += countJSON["trigramTotal"]
            bigramSpaceOneTotal += countJSON["bigramSpaceOneTotal"]
            bigramSpaceTwoTotal += countJSON["bigramSpaceTwoTotal"]
            trigramSpaceOneTotal += countJSON["trigramSpaceOneTotal"]
            trigramSpaceTwoTotal += countJSON["trigramSpaceTwoTotal"]
            trigramSpaceThreeTotal += countJSON["trigramSpaceThreeTotal"]
            trigramSpaceOneThreeTotal += countJSON["trigramSpaceOneThreeTotal"]
    
    ngramData = {"Counts": aggregateCounts,
                "unigramTotal": unigramTotal,
                "bigramTotal": bigramTotal,
                "bigramSpaceOneTotal": bigramSpaceOneTotal,
                "bigramSpaceTwoTotal": bigramSpaceTwoTotal,
                "trigramTotal": trigramTotal,
                "trigramSpaceOneTotal": trigramSpaceOneTotal,
                "trigramSpaceTwoTotal": trigramSpaceTwoTotal,
                "trigramSpaceThreeTotal": trigramSpaceThreeTotal,
                "trigramSpaceOneThreeTotal": trigramSpaceOneThreeTotal
                }

    if spacesRemoved:
        path_to_ngram_dir += "spaceless/"
    else:
        path_to_ngram_dir += "spaced/"

    # write ngram counts file
    target_file = os.path.join(path_to_ngram_dir,"aggregate_ngram_counts.json")
    with io.open(target_file,"w", encoding="UTF-8") as f:
        json.dump(ngramData, f, indent=4)
    
    ngramProbability = {}
    for ngram, count in aggregateCounts.items():

        if len(ngram) == 1:
            ngramProbability[ngram] = count/unigramTotal

        if len(ngram) == 2:

            if ngram[0] == " ":
                ngramProbability[ngram] = count/bigramSpaceOneTotal

            elif ngram[1] == " ":
                ngramProbability[ngram] = count/bigramSpaceTwoTotal

            else:
                ngramProbability[ngram] = count/bigramTotal
        
        if len(ngram) == 3:

            if ngram[1] == " ":
                ngramProbability[ngram] = count/trigramSpaceTwoTotal

            elif ngram[0] == " " and ngram[2] == " ":
                ngramProbability[ngram] = count/trigramSpaceOneThreeTotal

            elif ngram[0] == " ":
                ngramProbability[ngram] = count/trigramSpaceOneTotal

            elif ngram[2] == " ":
                ngramProbability[ngram] = count/trigramSpaceThreeTotal

            else:
                ngramProbability[ngram] = count/trigramTotal

    # write ngram probability file
    target_file = os.path.join(path_to_ngram_dir,"aggregate_ngram_probabilities.json")
    with io.open(target_file,"w", encoding="UTF-8") as f:
        json.dump(ngramProbability, f, indent=4)
    print("Successfully created probability file at", path_to_ngram_dir + "aggregate_ngram_probabilities.json")