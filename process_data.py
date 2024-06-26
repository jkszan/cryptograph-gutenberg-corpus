"""
Process counts for all PG data.

Written by
M. Gerlach and F. Font-Clos

"""
import os
from os.path import join
import argparse
import glob
import ast
import pandas as pd

from src.pipeline import process_book
from src.utils import get_langs_dict


if __name__ == '__main__':

    parser = argparse.ArgumentParser(
        "Processing raw texts from Project Gutenberg:"
        " i) removing headers,ii) tokenizing, and iii) counting words.")
    # raw folder
    parser.add_argument(
        "-r", "--raw",
        help="Path to the raw-folder",
        default='data/raw/',
        type=str)
    # text folder
    parser.add_argument(
        "-ote", "--output_text",
        help="Path to text-output (text_dir)",
        default='data/text/',
        type=str)
    # tokens folder
    parser.add_argument(
        "-oto", "--output_tokens",
        help="Path to tokens-output (tokens_dir)",
        default='data/tokens/',
        type=str)
    # counts folder
    parser.add_argument(
        "-oco", "--output_counts",
        help="Path to counts-output (counts_dir)",
        default='data/counts/',
        type=str)
    
    parser.add_argument(
        "-ong", "--output_ngram",
        help="Path to ngram-statistics output",
        default='data/ngram/',
        type=str)

    # pattern to specify subset of books
    parser.add_argument(
        "-p", "--pattern",
        help="Pattern to specify a subset of books",
        default='*',
        type=str)

    # quiet argument, to suppress info
    parser.add_argument(
        "-q", "--quiet",
        action="store_true",
        help="Quiet mode, do not print info, warnings, etc"
    )

    # log file
    parser.add_argument(
        "-l", "--log_file",
        help="Path to log file",
        default=".log",
        type=str)

    # add arguments to parser
    args = parser.parse_args()

    # check whether the out-put directories exist
    if os.path.isdir(args.output_text) is False:
        raise ValueError("The directory for output of texts '%s' "
                         "does not exist" % (args.output_text))
    if os.path.isdir(args.output_tokens) is False:
        raise ValueError("The directory for output of tokens '%s' "
                         "does not exist" % (args.output_tokens))
    if os.path.isdir(args.output_counts) is False:
        raise ValueError("The directory for output of counts '%s' "
                         "does not exist" % (args.output_counts))

    # load metadata
    metadata = pd.read_csv("metadata/metadata.csv").set_index("id")

    # load languages dict
    langs_dict = get_langs_dict()

    # loop over all books in the raw-folder
    pbooks = 0
    for filename in glob.glob(join(args.raw, 'PG%s_raw.txt' % (args.pattern))):
        # The process_books function will fail very rarely, when
        # a file tagged as UTf-8 is not really UTF-8. We just
        # skip those books.
        try:
            # get PG_id
            PG_id = filename.split("/")[-1].split("_")[0]

            # get language from metadata
            # language is a string representing a list of languages codes
            lang_id = ast.literal_eval(metadata.loc[PG_id, "language"])[0]
            if lang_id in langs_dict.keys():
                language = langs_dict[lang_id]

            # Since we are looking for english text statistics, only process English books
            if language == "english":
                # process the book: strip headers, tokenize, count
                process_book(
                    path_to_raw_file=filename,
                    text_dir=args.output_text,
                    tokens_dir=args.output_tokens,
                    counts_dir=args.output_counts,
                    language=language,
                    log_file=args.log_file
                )
                pbooks += 1

                if not args.quiet:
                    print("Processed %d books..." % pbooks, end="\r")
        except UnicodeDecodeError:
            if not args.quiet:
                print("# WARNING: cannot process '%s' (encoding not UTF-8)" % filename)
        except KeyError:
            if not args.quiet:
                print("# WARNING: metadata for '%s' not found" % filename)
        except Exception as e:
            if not args.quiet:
                print("# WARNING: cannot process '%s' (unkown error)" % filename)
# TODO: Create file analagous to this that combines the functions of getBookSubset.py and generateStatistics.py
