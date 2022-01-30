import igraph as ig

from my_library import create_csv_network_station, read_graph, import_csv



df_calendar = import_csv('calendar.csv')
df_calendar_dates = import_csv('calendar_dates.csv')
df_routes = import_csv('routes.csv')
df_stops = import_csv('stops.csv')
df_stop_times = import_csv('stop_times.csv')
df_trips = import_csv('trips.csv')


#rows = df_stop_times.loc[df_stop_times['trip_id'] == 13497685]
#rows.sort_values(by=["stop_sequence"], ascending=True, inplace=True)

create_csv_network_station("data/edges_station_completo.csv", "data/edges_station_distanti.csv", df_stop_times)



g = read_graph(False, 'csv/stops.csv', 'data/edges_station_completo.csv', 'data/names.csv')
print(g.summary())
print(g)

ig.plot(g)

