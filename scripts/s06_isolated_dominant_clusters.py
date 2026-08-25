from pathlib import Path

from tm2p.enum import AnalysisUnit  # type: ignore
from tm2p.enum import AssociationIndex  # type: ignore
from tm2p.enum import GraphClusteringAlgorithm  # type: ignore
from tm2p.enum import UnitOrderBy  # type: ignore
from tm2p.portfolio.thematic_struct.co_occur.direct import UnitsByCluster

ASSOCIATION_INDEX = AssociationIndex.ASSOCIATION_STRENGTH
CLUSTERING = GraphClusteringAlgorithm.LOUVAIN
ROOT_DIRECTORY = "./scopus/"

MAX_RECURSIVE_CLUSTERING_DEPTH = 3
MIN_RECURSIVE_CLUSTER_SIZE = 8
MINIMUM_PAIR_CO_OCCURRENCE = 1
TOP_N_UNITS = 10000

PARAMETERS = [
    # {
    #     "YEAR_RANGE": (1991, 2011),
    #     "MIN_OCC": 2,
    # },
    # {
    #     "YEAR_RANGE": (2012, 2016),
    #     "MIN_OCC": 2,
    # },
    # {
    #     "YEAR_RANGE": (2017, 2020),
    #     "MIN_OCC": 2,
    # },
    # {
    #     "YEAR_RANGE": (2021, 2024),
    #     "MIN_OCC": 2,
    # },
    {
        "YEAR_RANGE": (2025, 2026),
        "MIN_OCC": 2,
    },
    # {
    #     "YEAR_RANGE": (1991, 2026),
    #     "MIN_OCC": 3,
    # },
]


def main():
    report_units_by_cluster()


def report_units_by_cluster():
    for period_parameters in PARAMETERS:
        report_units_by_cluster_per_period(period_parameters)


def report_units_by_cluster_per_period(period_parameters):

    year_start, year_end = period_parameters["YEAR_RANGE"]
    min_occ = period_parameters["MIN_OCC"]

    units_by_cluster = (
        UnitsByCluster()
        #
        # ANALYSIS UNIT:
        .with_analysis_unit(AnalysisUnit.CONCEPT)
        #
        .having_top_n_units(TOP_N_UNITS)
        .having_units_ordered_by(UnitOrderBy.OCC)
        .having_unit_occurrence_between(min_occ, None)
        .having_unit_global_citation_between(None, None)
        .having_units_in(None)
        #
        .using_minimum_pair_co_occurrence(1)
        #
        # COUNTERS:
        .using_counters(False)
        #
        # NETWORK:
        .using_association_index(ASSOCIATION_INDEX)
        #
        # CLUSTERING:
        .using_clustering(CLUSTERING)
        .using_max_recursive_clustering_depth(MAX_RECURSIVE_CLUSTERING_DEPTH)
        .using_min_recursive_cluster_size(MIN_RECURSIVE_CLUSTER_SIZE)
        #
        # DATABASE:
        .where_root_directory(ROOT_DIRECTORY)
        .where_record_years_range(year_start, year_end)
        .where_record_global_citations_range(None, None)
        .where_records_match(None)
        #
        .run()
    )

    filename = (
        Path("outputs") / f"units_by_isolated_cluster_{year_start}_{year_end}.txt"
    )

    units_by_cluster.to_string(index=False, buf=filename, encoding="utf-8")

    filename = filename.with_suffix(".tsv")
    units_by_cluster.to_csv(
        index=False, path_or_buf=filename, encoding="utf-8", sep="\t"
    )


if __name__ == "__main__":
    main()
