import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt

# Graph - initialisation
reseau_df_concat = pd.read_csv('data/dataset_RT_final.csv',sep=";")
# Création d'un graph non orienté à partir des données du dataframe
G = nx.Graph()
G.add_edges_from(zip(reseau_df_concat['t_user'], reseau_df_concat['rt_user']))

# Calcul et affichage du nombre d'arêtes et de noeuds
print("Nombre d'arêtes:", G.number_of_edges(), "Nombre de noeuds:", G.number_of_nodes())

# Calcul et affichage du degré (max & min) du grah
deg = nx.degree(G)
max_deg = max(deg, key=lambda x: x[1])
min_deg = min(deg, key=lambda x: x[1])
print("Degré maximum:", max_deg)
print("Degré minimum:", min_deg)

# Le graphe non orienté est-il connexe ?
if nx.is_connected(G):
    print("Le graphe est connecté")
else:
    print("Le graphe n'est pas connecté")
    
# Affichage du graphe non orienté
pos = nx.random_layout(G)
nx.draw(G, pos=pos, node_size=30, node_color='blue', alpha=0.8)
plt.show()

# Si le graphe est non connexe : Comptabilisation de tous les sous-graphes connectés dans le graphe
print("Il existe", nx.number_connected_components(G),"de sous-graphes connectés dans le graph")

# Création du sous graphe comportant le plus de connexions 
subgraph = max(nx.connected_components(G), key=len)
G_subgraph = G.subgraph(subgraph)
print("La plus grand sous-graphe contient", G_subgraph.number_of_nodes(), "de noeuds et", G_subgraph.number_of_edges(), "d'arêtes.")

# Le sous graphe est-il connexe ?
if nx.is_connected(G_subgraph):
    print("Le sous-graphe est connecté")
else:
    print("Le sous-graphe n'est pas connecté")

# Affichage du sous graphe
pos = nx.random_layout(G_subgraph)
nx.draw(G_subgraph, pos=pos, node_size=30, node_color='blue', alpha=0.8)
plt.show()


# Graph - Centralités
# Calcul des 3 indicateurs de centralité
degree_c = nx.degree_centrality(G_subgraph)
degree_between_c = nx.betweenness_centrality(G_subgraph, normalized=False)
degree_close_c = nx.closeness_centrality(G_subgraph)
# Affichage des 10 premiers noeuds centraux pour chaque indicateur de centralité (noeuds + valeurs)  
print("Degree centrality top 10 nodes:")
print(sorted(degree_c.items(), key=lambda x: x[1], reverse=True)[:10])
print("Betweenness centrality top 10 nodes:")
print(sorted(degree_between_c.items(), key=lambda x: x[1], reverse=True)[:10])
print("Closeness centrality top 10 nodes:")
print(sorted(degree_close_c.items(), key=lambda x: x[1], reverse=True)[:10])


# Visualisation graphique du réseau

# Calcul du degré de chaque nœud
node_and_degree = dict(G_subgraph.degree())

# Sélection des nœuds centraux
central_nodes = ['tariqkrim', 'Souveraine Tech']

# Positionnement des nœuds via l'algorithme spring layout
pos = nx.spring_layout(G_subgraph, k=0.05)

# Couleurs des nœuds
node_colors = list(node_and_degree.values())
colors_central_nodes = ['orange', 'red']

# Calcul de la centralité de betweenness des nœuds
betweenness_dict = nx.betweenness_centrality(G_subgraph)
betweenness = [betweenness_dict[n] for n in G_subgraph.nodes()]

# Création du graphique
plt.figure(figsize=(20, 20))
nodes = nx.draw_networkx_nodes(G_subgraph, pos, node_size=60, node_color=betweenness, cmap=plt.cm.PiYG, alpha=0.6)
edges = nx.draw_networkx_edges(G_subgraph, pos, edge_color='black', alpha=0.5, width=0.1)
nodes.set_norm(plt.Normalize(vmin=0, vmax=max(betweenness)))
plt.colorbar(nodes)

nx.draw_networkx_nodes(G_subgraph, pos=pos, nodelist=central_nodes, node_size=300, node_color=colors_central_nodes)

# Enregistrement et affichage du graphique
plt.axis('off')
plt.savefig('data/graphfinal.png')
plt.show()




