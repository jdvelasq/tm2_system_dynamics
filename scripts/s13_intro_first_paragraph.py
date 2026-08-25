from tm2p.enum import RecordOrderBy  # type: ignore
from tm2p.report.manuscr.first_paragraph import FirstParagraph  # type: ignore

ROOT_DIRECTORY = "./scopus/"


def main():

    (
        FirstParagraph()
        #
        # TEXT:
        .having_text_matching(("system dynamics",))
        .using_word_length(200)
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
