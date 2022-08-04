import query_io
import sourcing
import plotting


query = query_io.get_query()
data = sourcing.get_data(query)
plot = plotting.visualize(data, query)
query_io.export(plot, query)
