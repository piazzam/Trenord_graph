import os
import sys
import subprocess

subprocess.check_call([sys.executable, '-m', 'pip', 'install',
    'pandas'])
reqs = subprocess.check_output([sys.executable, '-m', 'pip',
        'freeze'])
installed_packages = [r.decode().split('==')[0] for r in reqs.split()]
print(installed_packages)
import pandas as pd

subprocess.check_call([sys.executable, '-m', 'pip', 'install',
    'python-igraph'])
reqs = subprocess.check_output([sys.executable, '-m', 'pip',
        'freeze'])
installed_packages = [r.decode().split('==')[0] for r in reqs.split()]
print(installed_packages)
import igraph as ig

subprocess.check_call([sys.executable, '-m', 'pip', 'install',
    'numpy'])
reqs = subprocess.check_output([sys.executable, '-m', 'pip',
        'freeze'])
installed_packages = [r.decode().split('==')[0] for r in reqs.split()]
print(installed_packages)
import numpy as np

import random
import csv



# -------- I/O FUNCTIONS ----------    
    

def convert():
    dire = os.listdir("gtfs")
    
    for el in dire:
        file = open("gtfs/"+el, "r", encoding = "utf-8")
        file_name = el.split('.')
        file_com = file_name[0] + ".csv"
        file_write = open(file_com, "w", encoding = "utf-8",delimiter=';')
        for el in file:
            file_write.write(el)
        file.close()
        file_write.close()

def import_csv(file_name):
    return pd.read_csv (r'csv/'+file_name)

def read_graph(directed, nodes_filename, edges_filename, names_filename):
    df_nodes = pd.read_csv(nodes_filename)
    df_edges = pd.read_csv(edges_filename)
    #print(df_nodes)
    G = ig.Graph.DictList(
          vertices=df_nodes.to_dict('records'),
          edges=df_edges.to_dict('records'),
          directed=directed,
          vertex_name_attr='stop_id',
          edge_foreign_keys=('source', 'target'))

    df_name = pd.read_csv(names_filename)

    i = 0
    for el in G.vs:
        rows = df_name.loc[df_nodes['stop_id'] == el["stop_id"]]
        el["name"] = rows.at[i,"stop_name"]
        #el['lat'] = rows.at[i,"stop_lat"]
        #el['lon'] = rows.at[i,"stop_lon"]
        i += 1

    return G



def create_csv_network_station(file_name_zero, file_name_dist, df_stop_times):
    trips = df_stop_times['trip_id']
    x = np.array(np.unique(trips))
    file_write = open(file_name_zero, "w", newline='', encoding = "utf-8")
    writer = csv.writer(file_write, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    writer.writerow(["source", "target", "dist"])
    edges = []
    edges_dist = []
    for el in x:
        rows = df_stop_times.loc[df_stop_times['trip_id'] == el]
        rows.sort_values(by=["stop_sequence"], ascending=True, inplace=True)
        for i in range(len(rows)) :
            #print(rows.iloc[i])
            #print(rows.iloc[i]['stop_id'])
            #print('\n')
            if i>0:
                if rows.iloc[i]['stop_sequence'] == rows.iloc[i-1]['stop_sequence']+1:
                    if [rows.iloc[i-1]['stop_id'], rows.iloc[i]['stop_id'], 0] not in edges and [rows.iloc[i]['stop_id'], rows.iloc[i-1]['stop_id'], 0] not in edges:
                        edges.append([rows.iloc[i-1]['stop_id'], rows.iloc[i]['stop_id'], 0])
                else:
                    dist = rows.iloc[i]['stop_sequence'] - rows.iloc[i-1]['stop_sequence']-1
                    edges_dist.append([rows.iloc[i-1]['stop_id'], rows.iloc[i]['stop_id'], dist])
    print(edges)
    print('\n')
    print(edges_dist)
    res = []
    for i in edges_dist:
        if i not in res:
            res.append(i)
    
    edges_univ = []
    for i in edges:
        if i not in edges_univ:
            edges_univ.append(i)
    
    
    for el in edges_univ:
        print(el)
        writer.writerow(el)
        
    file_write.close()


    file_write = open(file_name_dist, "w", newline='', encoding = "utf-8")
    writer = csv.writer(file_write, delimiter=';', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    writer.writerow(["source", "target", "dist"])
    
    for el in res:
        print(el)
        writer.writerow(el)
        
    file_write.close()



#---------- CENTRALITY MEASURE --------
def calcolate_degree(G, mode):
    return  G.degree(G.vs, mode=mode)

    
def calcolate_betweenness(G, directed, weights):
    G.vs['betweenness'] = G.betweenness(G.vs, directed=directed,  weights = weights)
    return [node['betweenness']/((G.vcount()-1)*(G.vcount()-2)/2) for node in G.vs()]

def calcolate_betweenness_directed(G, directed, weights):
    G.vs['betweenness'] = G.betweenness(G.vs, directed=directed,  weights = weights)
    return [node['betweenness']/((G.vcount()-1)*(G.vcount()-2)) for node in G.vs()]

def calcolate_closeness(G, mode, weights):
    return G.closeness(G.vs, weights = weights, mode=mode)
    

def calcolate_eigenvector(G, directed, weights):
    return G.eigenvector_centrality(directed=directed, weights = weights)

def calcolate_pagerank(G, directed, weights):
    return G.pagerank(G.vs, directed=directed, weights = weights)

def save_centrality_csv(g, file_name):
    
    file_write = open(file_name, "w",  encoding='utf-8')

    file_write.write("stop_id;name;degree_all;degree_out;degree_in;betweenness;closeness_all;closeness_out;closeness_in;eigenvector;pagerank\n")
   
    for node in g.vs():
        print(str(node['stop_id'])+";"+str(node['name'])+";"+str(node['degree_all'])+";"+str(node['degree_out'])+";"+str(node['degree_in']) + ";"+str(node['betweenness'])+ ";"+str(node['closeness_all'])+ ";"+str(node['closeness_out'])+ ";"+str(node['closeness_in'])+ ";"+str(node['eigenvector'])+ ";"+str(node['pagerank']))
        file_write.write(str(node['stop_id'])+";"+str(node['name'])+";"+str(node['degree_all'])+";"+str(node['degree_out'])+";"+str(node['degree_in']) + ";"+str(node['betweenness'])+ ";"+str(node['closeness_all'])+ ";"+str(node['closeness_out'])+ ";"+str(node['closeness_in'])+ ";"+str(node['eigenvector'])+ ";"+str(node['pagerank']))
        file_write.write("\n")
    file_write.close()
    
#---------- OTHER MEASURES ---------
#Calcola e ritorna il valore di efficiency (Latora and Marchiori 2001)
def efficiency(g):
    N = len(g.vs)
    somma = 0
    for el in g.vs:
        for el_due in g.vs:
            if el != el_due:
                sp = len(g.get_shortest_paths(el, to = el_due, mode="all")[0])
                if sp != 0:
                    e = 1/sp
                else:
                    e = 0
                somma += e
    efficiency = somma / (N * (N-1))
    return efficiency

def calculate_load(g, directed, weights):
    g.vs['load'] = g.betweenness(g.vs, directed=directed,  weights = weights)
    return [node['load']/((g.vcount()-1)*(g.vcount()-2)) for node in g.vs()]
    
def calculate_capacity(g, alpha):
    for v in g.vs:
        v['capacity'] = (1 + alpha) * v['load0']
    return g

def delete_cascade(g, radio):
    d = []
    Er = []
    Sr = []

    delete = True
    while delete == True:
        g.vs['load'] = calculate_load(g, False, None)
        delete = False
        #print('\n')
        for v in g.vs:
            
            if v['load'] > v['capacity']:
                print(v)
                d.append(v['stop_id'])
                g.delete_vertices(v)
                if radio:
                    Er.append(efficiency(g))
                    Sr.append(large_component_size(g))
                delete = True
                
    return [g, d, Er, Sr]



def failure_cascade(g, radio):
    alpha = 0.01
    Er = []
    Sr = []
    g.vs['load0'] = calculate_load(g, False, None)
    g = calculate_capacity(g, alpha)
    g.vs['load'] = g.vs['load0'].copy()
    delete = []
    max_measure = max(g.vs['load'])
    print(max_measure)
    v = g.vs.select(load=max_measure)
    print(v[0])
    delete.append(v[0]['stop_id'])
    g.delete_vertices(v[0])
    if radio:
        Er.append(efficiency(g))
        Sr.append(large_component_size(g))
    [g, d, E, S] = delete_cascade(g, radio)
    delete = delete + d
    Er = Er + E
    Sr = Sr + S
    print(delete)
    return [g, delete, Er, Sr]

def failure_cascade_random(g, radio):
    alpha = 0.01
    Er = []
    Sr = []
    g.vs['load0'] = calculate_load(g, False, None)
    g = calculate_capacity(g, alpha)
    g.vs['load'] = g.vs['load0'].copy()
    delete = []
    v = random.choice(g.vs)
    print(v)
    delete.append(v['stop_id'])
    g.delete_vertices(v)
    if radio:
        Er.append(efficiency(g))
        Sr.append(large_component_size(g))

    [g, d, E, S] = delete_cascade(g, radio)
    delete = delete + d
    Er = Er + E
    Sr = Sr + S
    print(delete)
    return [g, delete, Er, Sr]
        
        
    

def large_component_size(g):
    largest = g.clusters(mode="weak").giant()
    return len(largest.vs) / len(g.vs)

def fall_of_effciency(g, gi):
    eff_g = efficiency(g)
    eff_gi = efficiency(gi)
    foe = (eff_g - eff_gi) / eff_g
    return foe     

def is_symmetric(matrix):
    return matrix.transpose() == matrix.all()
    
def eigen(g):
    a = g.get_adjacency()
    m = a._get_data()
    matrix = np.matrix(m)
    w,v = np.linalg.eig(matrix)
    return w

def spectral_gap(g):
    w = eigen(g)
    w.sort()
    radius = w[-1]
    mu_uno = w[-2]
    return radius - mu_uno
    

def spectral_radius(g):
    w = eigen(g)
    return max(abs(w))

def algebraic_connectivity(g):
    degree = []    
    for v in g.vs:
        degree.append(v.degree())
    
    adj_matrix = g.get_adjacency()
    adj_matrix = adj_matrix._get_data()
    A = np.matrix(adj_matrix)    
    D = np.diag(degree)
    L = D - A

    w,v = np.linalg.eig(L)

    w.sort()

    return w[1]



def node_load(g):
    g.vs["betweennes_cal"] = calcolate_betweenness(g, True, g.es["size"])
    g.vs["degree_cal"] = calcolate_degree(g, mode="all")
    i = 0
    treni_in = {}
    for el in g.vs:
        weight_in = 0
        weight_out = 0
        for e in el.in_edges():
            weight_in += e["size"]
        for e in el.out_edges():
            weight_out += e["size"]
        dicti = {}
        dicti["id"] = el["stop_id"]
        dicti["nome"] = el["name"]
        dicti["out"] = weight_out
        dicti["in"] = weight_in
        dicti['load'] = weight_out + weight_in
        dicti["betweennes"] = el["betweennes_cal"]
        dicti["degree"] = el["degree_cal"]
        treni_in[i] = dicti
        i+=1


    df_in = pd.DataFrame.from_dict(treni_in, orient = 'index')
    return df_in

def route_load(g):
    peso_tratte = {}
    peso_tratte_list = []
    for el in g.es:
        if el["route"] in peso_tratte:
            peso_tratte[el["route"]] += el["size"]
        else:
            peso_tratte[el["route"]] = el["size"]

    df_tratte = pd.DataFrame.from_dict(peso_tratte, orient="index")
    return df_tratte



#---------- ATTACK STRATEGY ---------
    
# Ritorna un nuovo grafo identico a quello passato, ma con un vertice casuale e 
# i risettivi archi rimossi
def random_attack(g,n,radio):
    Er = []
    Sr = []
    vertex_del = []
    g_att = g.copy()
    for i in range(int(n)):
        v = random.choice(g_att.vs)
        print(v)
        vertex_del.append(v['stop_id'])
        g_att.delete_vertices(v)
        if radio:
            Er.append(efficiency(g_att))
            Sr.append(large_component_size(g_att))


    return [g_att, vertex_del, Er, Sr]

# Ritorna un nuovo grafo identico a quello passato, ma con il vertice con la 
# misura di degree maggiore e i risettivi archi rimossi
def target_attack_degree(g, n, radio):
    Et = []
    St = []
    vertex_del = []
    g_att = g.copy()
    for i in range(int(n)):
        # Selezionare vertice con misura più alta
        max_measure = max(g_att.vs['degree_all'])
        v = g_att.vs.select(degree_all=max_measure)
        print(v[0])
        vertex_del.append(v[0]['stop_id'])
        g_att.delete_vertices(v[0])
        if radio:
            Et.append(efficiency(g_att))
            St.append(large_component_size(g_att))
    print(vertex_del)

    return [g_att, vertex_del, Et, St]

# Ritorna un nuovo grafo identico a quello passato, ma con il vertice con la 
# misura di betweenness maggiore e i risettivi archi rimossi
def target_attack_betweenness(g, n, radio):
    E_bet = []
    S_bet = []
    vertex_del = []
    g_att = g.copy()
    for i in range(int(n)):
        # Selezionare vertice con misura più alta
        max_measure = max(g_att.vs['betweenness'])
        v = g_att.vs.select(betweenness=max_measure)
        print(v[0])
        vertex_del.append(v[0]['stop_id'])
        g_att.delete_vertices(v[0])
        if radio:
            E_bet.append(efficiency(g_att))
            S_bet.append(large_component_size(g_att))
    print(vertex_del)

    return [g_att, vertex_del, E_bet, S_bet]

