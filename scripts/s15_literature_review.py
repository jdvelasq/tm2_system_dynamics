from tm2p.enum import RecordOrderBy  # type: ignore
from tm2p.report.manuscr.literature_review import LiteratureReview  # type: ignore

ROOT_DIRECTORY = "./scopus/"


def main():

    (
        LiteratureReview()
        #
        # TEXT:
        .with_core_area("SYSTEM DYNAMICS")
        .using_word_length(250)
        #
        # DATABASE:
        .where_root_directory(ROOT_DIRECTORY)
        .where_record_years_range(None, None)
        .where_record_global_citations_range(None, None)
        .where_records_match(None)
        .where_records_ordered_by(RecordOrderBy.YEAR_NEWEST)
        #
        .run()
    )


if __name__ == "__main__":
    main()
