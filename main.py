import query_io
import sourcing
import plotting


query = query_io.get_query()
data, teams_updated = sourcing.get_data(query)
query[1] = teams_updated   # remove teams for which data is missing
plot = plotting.visualize(data, query)
query_io.export(plot, query)
