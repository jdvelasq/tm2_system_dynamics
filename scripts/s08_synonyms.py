import sys

from tm2p.refine.concept.merge import Manual  # type: ignore

for preferred, variant in [
    ("health care delivery", "care delivery"),
    ("power generation", "electricity generation"),
    ("prefabricated construction", "prefabricated building"),
]:

    sys.stderr.write(f"\nProcessing {preferred} <--- {variant}")
    sys.stderr.flush()
    Manual().having_text_matching(
        (preferred, variant),
    ).where_root_directory("./scopus/").run()
    sys.stderr.write("\n")
    sys.stderr.flush()
