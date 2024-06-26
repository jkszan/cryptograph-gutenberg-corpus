# -*- coding: utf-8 -*-
from .cleanup import strip_headers
from .formatter import format_text
from collections import Counter
import io
import os

def process_book(
	path_to_raw_file=None,
	text_dir=None,
	tokens_dir=None,
	counts_dir=None,
	cleanup_f=strip_headers,
    format_f=format_text,
    overwrite_all=False,
    language="english",
    log_file=""
	):
    """
    Process a book, from raw data to counts.

    The database is structured in the following levels of processing:

    1. raw: the book as downloaded from PG site.
    2. text: the book with headers/legal notices/etc removed.
    3. tokens: the tokenized book. One token per line.
    4. counts: the counts of all types. One type per line.

    This function takes a file at the 'raw' level and computes the counts,
    saving to disk the intermediate 'text' and 'tokens' files.

    Overwrite policy
    ----------------
    By default a book is processed in full except if all the 
    files already exist (raw,text,tokens and counts). The overwrite_all
    keyword can cahnge this behaviour.

    Parameters
    ----------
    overwrite_all : bool
        If set to True, everything is processed regargless of existing files.
    """
    if text_dir is None:
        raise ValueError("You must specify a path to save the text files.")
        
    if path_to_raw_file is None:
        raise ValueError("You must specify a path to the raw file to process.")

    # get PG number
    PG_number = path_to_raw_file.split("/")[-1].split("_")[0][2:]

    if overwrite_all or\
        (not os.path.isfile(os.path.join(text_dir,"PG%s_text.txt"%PG_number))) or \
        (not os.path.isfile(os.path.join(counts_dir,"PG%s_counts.txt"%PG_number))):
        # read raw file
        with io.open(path_to_raw_file, encoding="latin-1") as f:
            text = f.read()

        # clean it up
        clean = cleanup_f(text)
        formatted = format_f(clean)

        # write text file
        target_file = os.path.join(text_dir,"PG%s_text.txt"%PG_number)
        with io.open(target_file,"w", encoding="UTF-8") as f:
            f.write(formatted)
