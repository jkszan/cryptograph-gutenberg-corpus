import pandas as pd
from collections import defaultdict
from src.pipeline import process_book
import os.path

def select_books():
    metadata = pd.read_csv("metadata/metadata.csv").set_index("id")
    print(len(metadata))
    filtered_meta = metadata[metadata["language"].str.contains("en")]
    selectedBooks = filtered_meta[filtered_meta["authoryearofdeath"] >= 1970]

    processedBooks = 0

    for index, _ in selectedBooks.iterrows():
    #for index in ['PG1155']:
        if os.path.isfile("data/raw/" + str(index) + "_raw.txt"):

            process_book(
                path_to_raw_file="data/raw/" + str(index) + "_raw.txt",
                text_dir="data/text/",
                tokens_dir="",
                counts_dir="",
                language="english",
                log_file=".log"
            )

            processedBooks += 1
        else:
            print("ERROR:", index, "SKIPPED")

        print("Processed %d books..." % processedBooks, end="\r")

    
    print("Books Processed:", processedBooks)
    return

select_books()