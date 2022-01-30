import igraph as ig
import matplotlib.pyplot as plt

from my_library import *

g = read_graph(False, 'csv/stops.csv', 'data/edges_station_completo.csv', 'data/names.csv')
print(g.summary())
ig.plot(g)


    
# --------- RANDOM ATTACK -----------
Er = []
Sr = []
g_att_r = g.copy()

n = g.vcount()/4*3
[g_att_r, vertex_del, Er, Sr] = random_attack(g_att_r,n,True)
    
fig = plt.figure()
plt.plot(Er, "b-")
fig.suptitle('Efficiency', fontsize=20)
plt.xlabel('Number of removal nodes', fontsize=14)
plt.ylabel('E', fontsize=14)
plt.show()

fig = plt.figure()
plt.plot(Sr, "b-")
fig.suptitle('Large Connected Component', fontsize=20)
plt.xlabel('Number of removal nodes', fontsize=14)
plt.ylabel('S', fontsize=14)
plt.show()



g.vs['degree_all'] = calcolate_degree(g, 'all')
g.vs['betweenness'] = calcolate_betweenness(g, False, None)


# --------- TARGET ATTACK -----------
Et = []
St = []
g_att_t = g.copy()

n = g.vcount()/4*3
[g_att_r, vertex_del, Et, St] = target_attack_degree(g_att_t,n,True)


    

Et_bet = []
St_bet = []
g_att_t_bet = g.copy()

n = g.vcount()/4*3
[g_att_r, vertex_del, Et_bet, St_bet] = target_attack_betweenness(g_att_t,n,True)

    
fig= plt.figure()
plt.plot(Et, "m-", label='Degree')
plt.plot(Et_bet, "c-", label='Betweenness')
fig.suptitle('Efficiency', fontsize=20)
plt.xlabel('Number of removal nodes', fontsize=14)
plt.ylabel('E', fontsize=14)
plt.legend(fancybox=True, framealpha=1, shadow=True, borderpad=1)
plt.show()

fig = plt.figure()
plt.plot(St, "m-", label='Degree')
plt.plot(St_bet, "c-", label='Betweenness')
fig.suptitle('Large Connected Component', fontsize=20)
plt.xlabel('Number of removal nodes', fontsize=14)
plt.ylabel('S', fontsize=14)
plt.legend(fancybox=True, framealpha=1, shadow=True, borderpad=1)
plt.show()




# --------- FAILURE CASCADE (BETWEENNESS) ---------


g_fail = g.copy()
[g_fail, vertex_del, Er, Sr] = failure_cascade(g_fail, True)
ig.plot(g_fail)
print(g_fail.summary())

fig = plt.figure()
plt.plot(Er, "b-")
fig.suptitle('Efficiency', fontsize=20)
plt.xlabel('Number of removal nodes', fontsize=14)
plt.ylabel('E', fontsize=14)
plt.show()

fig = plt.figure()
plt.plot(Sr, "b-")
fig.suptitle('Large Connected Component', fontsize=20)
plt.xlabel('Number of removal nodes', fontsize=14)
plt.ylabel('S', fontsize=14)
plt.show()

# --------- FAILURE CASCADE (RANDOM)---------
g_fail_r = g.copy()
[g_fail_r, vertex_del, Er, Sr] = failure_cascade(g_fail_r, True)
ig.plot(g_fail_r)
print(g_fail_r.summary())

fig = plt.figure()
plt.plot(Er, "b-")
fig.suptitle('Efficiency', fontsize=20)
plt.xlabel('Number of removal nodes', fontsize=14)
plt.ylabel('E', fontsize=14)
plt.show()

fig = plt.figure()
plt.plot(Sr, "b-")
fig.suptitle('Large Connected Component', fontsize=20)
plt.xlabel('Number of removal nodes', fontsize=14)
plt.ylabel('S', fontsize=14)
plt.show()
