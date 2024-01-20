import json
import io

def test():
    with io.open("data/counts/PG34_counts.json", "r") as file:
        ngramCounts = json.load(file)

    unigramSum = 0
    bigramSum = 0
    bigramSpaceOne = 0
    bigramS2 = 0
    trigram = 0
    trigramS1 = 0
    trigramS2 = 0
    trigramS3 = 0
    trigramS1S3 = 0
    print("test")
    for ngram, count in ngramCounts["Counts"].items():
        if len(ngram) == 1:
            #print(ngram, count/ngramCounts['unigramTotal'])
            unigramSum += count/ngramCounts['unigramTotal']

    for ngram, count in ngramCounts["Counts"].items():
        if len(ngram) == 2 and ngram[0] == " " and ngram[1] != " ":
            print(ngram, count/ngramCounts['bigramSpaceOneTotal'])
            bigramSpaceOne += count/ngramCounts['bigramSpaceOneTotal']

    print(bigramSpaceOne)
    #print(unigramSum, bigramSum)
print("!")
test()

