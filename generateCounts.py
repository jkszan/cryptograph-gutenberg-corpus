import os
from src.ngram import generateNgramCounts, aggregateCounts

def generateAllCounts(path_to_text_dir="./data/text/", path_to_counts_dir="./data/counts/"):
    processedCounts = 0

    for file in os.listdir(path_to_text_dir):
        if file.endswith(".txt"):
            path_to_text_file = path_to_text_dir + file
            PG_Number = int(path_to_text_file.split("/")[-1].split("_")[0][2:])
            generateNgramCounts(PG_Number, path_to_text_file, path_to_counts_dir)

            processedCounts += 1
            print("Processed %d counts..." % processedCounts, end="\r")


#generateAllCounts()
aggregateCounts()