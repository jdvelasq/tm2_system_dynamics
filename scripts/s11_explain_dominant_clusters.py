from pathlib import Path  # type: ignore

from tm2p.enum import AnalysisUnit  # type: ignore
from tm2p.enum import AssociationIndex  # type: ignore
from tm2p.enum import GraphClusteringAlgorithm  # type: ignore
from tm2p.enum import UnitOrderBy  # type: ignore
from tm2p.portfolio.thematic_struct.co_occur.direct import (
    ClusterDefinition,
)  # type: ignore

ASSOCIATION_INDEX = AssociationIndex.ASSOCIATION_STRENGTH
CLUSTERING = GraphClusteringAlgorithm.LOUVAIN
ROOT_DIRECTORY = "./scopus/"

MAX_RECURSIVE_CLUSTERING_DEPTH = 3
MIN_RECURSIVE_CLUSTER_SIZE = 8
MINIMUM_PAIR_CO_OCCURRENCE = 1


PARAMETERS = [
    ((1991, 2011), 5),
    # ((2012, 2016), 4),
    # ((2017, 2020), 4),
    # ((2021, 2024), 4),
    # ((2025, 2026), 3),
]


def main():
    for year_range, occ in PARAMETERS:
        explain_clusters_per_period(year_range, occ)


def explain_clusters_per_period(year_range, occ):

    year_start, year_end = year_range

    (
        ClusterDefinition()
        #
        # ANALYSIS UNIT:
        .with_analysis_unit(AnalysisUnit.CONCEPT)
        #
        .having_top_n_units(None)
        .having_units_ordered_by(UnitOrderBy.OCC)
        .having_unit_occurrence_between(occ, None)
        .having_unit_global_citation_between(None, None)
        .having_units_in(None)
        .using_minimum_pair_co_occurrence(MINIMUM_PAIR_CO_OCCURRENCE)
        #
        # COUNTERS:
        .using_counters(False)
        #
        # NORMALIZATION:
        .using_association_index(ASSOCIATION_INDEX)
        #
        # CLUSTERING:
        .using_clustering(CLUSTERING)
        .using_max_recursive_clustering_depth(MAX_RECURSIVE_CLUSTERING_DEPTH)
        .using_min_recursive_cluster_size(MIN_RECURSIVE_CLUSTER_SIZE)
        #
        # TEXT:
        .with_core_area("SYSTEM DYNAMICS")
        .using_gpt_model("gpt-4.1")
        .using_word_length(300)
        .using_cluster_names([f"C_{i}" for i in range(20)])
        #
        # DATABASE:
        .where_root_directory(ROOT_DIRECTORY)
        .where_record_years_range(year_start, year_end)
        .where_record_global_citations_range(None, None)
        .where_records_match(None)
        #
        .run()
    )


if __name__ == "__main__":
    main()
