from pathlib import Path  # type: ignore

from tm2p.enum import UnitOrderBy  # type: ignore
from tm2p.portfolio.perform_metr.main import Metrics  # type: ignore

ROOT_DIRECTORY = "./scopus/"


def main():

    df = (
        Metrics()
        #
        # DATABASE:
        .where_root_directory(ROOT_DIRECTORY)
        .where_record_years_range(None, None)
        .where_record_global_citations_range(None, None)
        .where_records_match(None)
        #
        .run()
    )

    filename = Path("outputs") / "general_metrics.txt"

    df.to_string(filename, index=True, encoding="utf-8")
    filename = filename.with_suffix(".tsv")
    df.to_csv(filename, index=True, encoding="utf-8", sep="\t")


if __name__ == "__main__":
    main()
