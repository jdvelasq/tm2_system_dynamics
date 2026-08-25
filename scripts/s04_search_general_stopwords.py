import sys

import nltk
from tm2p._intern import Params  # type: ignore
from tm2p._intern import ParamsMixin  # type: ignore
from tm2p._intern.packag_data.word_lists.update_stopwords import update_stopwords
from tm2p.enum import ThField  # type: ignore
from tm2p.enum import AnalysisUnit, ThFile  # type: ignore
from tm2p.refine._intern.data_access import load_thesaurus_as_dataframe  # type: ignore

nltk.download("words")
from nltk.corpus import words

english_words = set(words.words())

PREFERRED = ThField.PREFERRED.value
VARIANT = ThField.VARIANT.value
N_WORDS = "N_WORDS"


def is_valid_word(text: str) -> bool:
    return text.lower() in english_words


def main():

    params = Params()
    params.root_directory = "./scopus/"
    params.thesaurus_file = ThFile.CONCEPT
    df = load_thesaurus_as_dataframe(params=params)
    df = df[[PREFERRED, VARIANT]]

    df[N_WORDS] = df[PREFERRED].str.split().str.len()
    df = df[df[N_WORDS] == 1]
    df = df[~df[PREFERRED].str.startswith("#")]
    df = df[~df[PREFERRED].str.contains("-")]
    df = df[~df[PREFERRED].str.contains("/")]
    df = df[df[PREFERRED].str.isalpha()]
    df = df[df[PREFERRED].apply(lambda x: is_valid_word(x) if len(x) == 1 else True)]
    df = df[df[PREFERRED].apply(is_valid_word)]
    df = df[df[PREFERRED].str.len() > 3]
    df = df.reset_index(drop=True)

    for index, row in df.iterrows():

        preferred = row[PREFERRED]
        variants = row[VARIANT].split("; ")
        variants = [v.strip() for v in variants]

        sys.stderr.write(f"{index+1}/{len(df)}  Checking: {preferred}")
        answer = update_stopwords(preferred, variants)
        if answer != "no":
            sys.stderr.write(f" ---> {answer}\n")
        else:
            sys.stderr.write("\n")
        sys.stderr.flush()


if __name__ == "__main__":
    main()
