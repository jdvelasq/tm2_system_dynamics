from tm2p.ingest.datasrc import Scopus  # type: ignore

Scopus().where_root_directory("./scopus/").run()
