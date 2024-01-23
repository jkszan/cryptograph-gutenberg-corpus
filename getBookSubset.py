import pandas as pd
from collections import defaultdict
from src.pipeline import process_book
import os.path

# TODO: Add param allowing %/number of books to select and by which metric / order to select (i.e. 30%, authoryearofdeath, desc)
def select_books():
    metadata = pd.read_csv("metadata/metadata.csv").set_index("id")
    print(len(metadata))
    filtered_meta = metadata[metadata["language"].str.contains("en")]

    # Arbitrary selection metric
    # TODO: Sort metadata by yearOfDeath and take top n% entries
    selectedBooks = filtered_meta[filtered_meta["authoryearofdeath"] >= 1970]

    processedBooks = 0

    for index, _ in selectedBooks.iterrows():
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
