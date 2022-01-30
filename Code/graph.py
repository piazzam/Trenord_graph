from my_library import *

g = read_graph(True, 'dataV2/nodes.csv', 'dataV2/edges.csv', 'csv/stops.csv')



print(g.summary())
print(g.assortativity_degree())
print(g.density())
print(g.reciprocity())

d = g.degree_distribution(mode="out")
print(d)

count = 0
for el in g.vs:
    if g.degree(el, mode="in") != g.degree(el, mode="out"):
        count += 1
print(count)

df_load = node_load(g)
df_tratte = route_load(g)

dire = os.listdir("dataV2/fasce")
  
graphs = []  
for el in dire:
    g_ext = read_graph(True, 'dataV2/nodes.csv', 'dataV2/fasce/'+el, 'csv/stops.csv')
    graphs.append(g_ext)

df_loads = []
df_tratte_fasce = []    
for el in graphs:
    print(el.summary())
    print(el.assortativity_degree())
    print(el.density())
    print(el.reciprocity())

    d = el.degree_distribution(mode="out")
    print(d)
    
    df_loads.append(node_load(el))
    df_tratte_fasce.append(route_load(el))
    




