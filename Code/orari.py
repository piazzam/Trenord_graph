import pandas as pd
from my_library import *


g = read_graph(True, 'csv/stops.csv', 'dataV2/fasce/edges_fifth.csv', 'csv/stops.csv')

print(g.summary())

g.vs["betweennes_cal"] = calcolate_betweenness(g, True, g.es["size"])
g.vs["degree_cal"] = calcolate_degree(g, mode="all")
i = 0
treni_in = {}
for el in g.vs:
    routes = []
    weight_in = 0
    weight_out = 0
    for e in el.in_edges():
        weight_in += e["size"]
        if e["route"] not in routes:
            routes.append(e["route"])
    for e in el.out_edges():
        weight_out += e["size"]
    dicti = {}
    dicti["id"] = el["stop_id"]
    dicti["nome"] = el["name"]
    dicti["out"] = weight_out
    dicti["in"] = weight_in
    dicti['load'] = weight_in + weight_out
    dicti["betweennes"] = el["betweennes_cal"]
    dicti["degree"] = el["degree_cal"]
    dicti["routes"] = routes
    treni_in[i] = dicti
    i+=1
    

df_in = pd.DataFrame.from_dict(treni_in, orient = 'index')
df_in.to_csv("orari/fifth.csv")