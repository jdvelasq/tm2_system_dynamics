from tm2p.portfolio.perform_metr.annu import Metrics  # type: ignore
from tm2p.portfolio.perform_metr.annu import PerformancePlot  # type: ignore

fig = (
    PerformancePlot()
    #
    .using_line_width(1.5)
    .using_marker_size(7)
    .using_uniform_textfont_size(10)
    .using_yshift(4)
    #
    .where_root_directory("./scopus/")
    .where_record_years_range(None, None)
    .where_record_global_citations_range(None, None)
    .where_records_match(None)
    #
    .run()
)
fig.write_html("outputs/step_1_annual_perf_metr.html")

df = (
    Metrics()
    .where_root_directory("./scopus/")
    .where_record_years_range(None, None)
    .where_record_global_citations_range(None, None)
    .where_records_match(None)
    .run()
)

with open("outputs/step_1_annual_perf_metr.txt", "w", encoding="utf-8") as f:
    f.write(df.to_string())
