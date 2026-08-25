from pathlib import Path  # type: ignore

from tm2p.enum import AnalysisUnit  # type: ignore
from tm2p.enum import AssociationIndex  # type: ignore
from tm2p.enum import GraphClusteringAlgorithm  # type: ignore
from tm2p.ingest.rec import Coverage  # type: ignore

ASSOCIATION_INDEX = AssociationIndex.ASSOCIATION_STRENGTH
CLUSTERING = GraphClusteringAlgorithm.LOUVAIN
ROOT_DIRECTORY = "./scopus/"

YEAR_RANGES = [
    (1991, 2011),
    (2012, 2016),
    (2017, 2020),
    (2021, 2024),
    (2025, 2026),
]


def main():
    for year_range in YEAR_RANGES:
        run_period(year_range[0], year_range[1])


def run_period(year_first, year_last):

    filename = Path("outputs") / f"coverage_{year_first}_{year_last}.txt"

    if filename.exists():
        filename.unlink()

    coverage = (
        Coverage()
        .with_analysis_unit(AnalysisUnit.CONCEPT)
        .where_root_directory(ROOT_DIRECTORY)
        .where_record_years_range(year_first, year_last)
        .where_record_global_citations_range(None, None)
        .where_records_match(None)
        .run()
    )

    with open(filename, "a", encoding="utf-8") as f:
        f.write("\n\n")
        f.write(coverage.to_string(index=False))
        f.write("\n\n")


main()
