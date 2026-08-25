import sys

from tm2p.refine.concept.stop import Stopword  # type: ignore

for word in sorted(
    [
        "vensim simulation",
        "vensim modeling",
    ]
):

    sys.stderr.write(f"\nProcessing stop word: {word}\n")
    sys.stderr.flush()
    Stopword().having_word(word).where_root_directory("./scopus/").run()
    sys.stderr.write("\n")
    sys.stderr.flush()
