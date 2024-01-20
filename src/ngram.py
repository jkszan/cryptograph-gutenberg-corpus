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
# TODO: List counts of ngrams / words alongside total ngrams / words so that we can combine the stats of many books together to make our
# overall stats

# TODO: For heuristic search (genetic algo), have mutation letters be selected with probability proportional to loss function of the characters
# TODO: Loss function of the characters can be deviation from unigram frequency plus deviation from bigram and trigram frequency for which the char is a part of
# The loss for bigram/trigram is doubled and tripled if the letter is repeated
# TODO: Since we know spaces (in the spaced variant) we should not include spaces in our unigram statistics and should seperate bigram and trigram
# arrangements where a space is present. A separate statistical distribution per position of the space
# TODO: Simple counting algo of for i in range(len(book)): book[i], book[i-1:i], book[i-2:i] should suffice here, not counting special case for spaces
# TODO: For unspaced variant just do spaced on a book text that has removed spaces from it
# Num books (initial): 2343

def generateNgramStatistics(PG_Number, 
                            path_to_text_file=None,
                            path_to_counts_dir=None,
                            ):
    
    with open(path_to_text_file, "r", encoding="UTF-8") as file:
        text = file.read()


    unigramCounts = defaultdict(lambda: 0)
    unigramTotal = 0

    bigramCounts = defaultdict(lambda: 0)
    bigramTotal = 0

    # Statistics for bigrams of the form " x"
    bigramSpaceOne = defaultdict(lambda: 0)
    bigramSpaceOneTotal = 0

    # Statistics for bigrams of the form "x "
    bigramSpaceTwo = defaultdict(lambda: 0)
    bigramSpaceTwoTotal = 0

    # Statistics for trigrams without spaces
    trigramCount = defaultdict(lambda: 0)
    trigramTotal = 0

    # Statistics for trigrams of the form " xx"
    trigramSpaceOne = defaultdict(lambda: 0)
    trigramSpaceOneTotal = 0

    # Statistics for trigrams of the form "x x"
    trigramSpaceTwo = defaultdict(lambda: 0)
    trigramSpaceTwoTotal = 0
    
    # Statistics for trigrams of the form "xx "
    trigramSpaceThree = defaultdict(lambda: 0)
    trigramSpaceThreeTotal = 0

    # Statistics for trigrams of the form " x "
    trigramSpaceOneThree = defaultdict(lambda: 0)
    trigramSpaceOneThreeTotal = 0

    for i in range(len(text)):

        if text[i] != " ":
            unigramCounts[text[i]] += 1
            unigramTotal += 1

        if i > 0:
            bigram = text[i-1:i+1]

            if bigram[0] == " ":
                bigramSpaceOne[bigram] += 1
                bigramSpaceOneTotal += 1

            elif bigram[1] == " ":
                bigramSpaceTwo[bigram] += 1
                bigramSpaceTwoTotal += 1
            else:
                bigramCounts[bigram] += 1
                bigramTotal += 1
        
        if i > 1:
            trigram = text[i-2: i+1]

            if trigram[1] == " ":
                trigramSpaceTwo[trigram] += 1
                trigramSpaceTwoTotal += 1

            elif trigram[0] == " " and trigram[2] == " ":
                trigramSpaceOneThree[trigram] += 1
                trigramSpaceOneThreeTotal += 1

            elif trigram[0] == " ":
                trigramSpaceOne[trigram] += 1
                trigramSpaceOneTotal += 1

            elif trigram[2] == " ":
                trigramSpaceThree[trigram] += 1
                trigramSpaceThreeTotal += 1

            else:
                trigramCount[trigram] += 1
                trigramTotal += 1

    ngramData = {"x": (unigramCounts, unigramTotal),
                 "xx": (bigramCounts, bigramTotal),
                 " x": (bigramSpaceOne, bigramSpaceOneTotal),
                 "x ": (bigramSpaceTwo, bigramSpaceTwoTotal),
                 "xxx": (trigramCount, trigramTotal),
                 " xx": (trigramSpaceOne, trigramSpaceOneTotal),
                 "x x": (trigramSpaceTwo, trigramSpaceTwoTotal),
                 "xx ": (trigramSpaceThree, trigramSpaceThreeTotal),
                 " x ": (trigramSpaceOneThree, trigramSpaceOneThreeTotal)}
    # write text file
    target_file = os.path.join(path_to_counts_dir,"PG%s_counts.json"%PG_Number)
    with io.open(target_file,"w", encoding="UTF-8") as f:
        json.dump(ngramData, f, indent=4)

generateNgramStatistics(34, path_to_text_file="./data/text/PG34_text.txt", path_to_counts_dir="./data/counts/")