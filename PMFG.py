# -*- coding: utf-8 -*-
"""
Created on Wed Jul 18 13:46:36 2018

@author: vttqh
"""
import networkx as nx
import planarity
#=============================================================================#
class Vertex():
    label = ''
    centrality_score = 0
    
    def __init__(self, label, centrality_score):
        self.label = label
        self.centrality_score = centrality_score
    
    def set_label(self, label):
        self.label = label
        
    def set_centrality_score(self, centrality_score):
        self.centrality_score = centrality_score
#=============================================================================#

def sort_graph_edges(G):
    sorted_edges = []
    for source, dest, data in sorted(G.edges(data=True), 
                                     key=lambda x: x[2]['weight'],
                                     reverse=True):
        sorted_edges.append({'source': source, 
                             'dest': dest,
                             'weight': data['weight']})
    
    return sorted_edges

def compute_PMFG(sorted_edges, nb_nodes):
    PMFG = nx.Graph()
    for edge in sorted_edges:
        PMFG.add_edge(edge['source'], edge['dest'], weight=edge['weight'])
        if not planarity.is_planar(PMFG):
            PMFG.remove_edge(edge['source'], edge['dest'])
            
        if len(PMFG.edges()) == 3 * (nb_nodes-2):
            break
        
    return PMFG

def build_PMFG(G):
    sorted_edges = sort_graph_edges(G)
    PMFG_graph = compute_PMFG(sorted_edges, len(G.nodes))
    return PMFG_graph
    
def build_PMFG_unweighted(PMFG_graph):
    PMFG_unweighted = nx.Graph()
    
    nodes = PMFG_graph.nodes()
    PMFG_unweighted.add_nodes_from(nodes)
    
    for edge in PMFG_graph.edges():
        PMFG_unweighted.add_edge(edge[0], edge[1], weight=1)
        
    return PMFG_unweighted

def choose_central_peripheral(PMFG_graph, nb_nodes_central, nb_nodes_peripheral):
    PMFG_weighted   = PMFG_graph
    PMFG_unweighted = build_PMFG_unweighted(PMFG_weighted)

    labels_of_nodes = PMFG_weighted.nodes()

    # Get list degree of nodes in both graph weighted and unweighted
    l_d_in_weighted    = list(PMFG_weighted.degree(labels_of_nodes))
    l_d_in_unweighted  = list(PMFG_unweighted.degree(labels_of_nodes))

    # Get list betweenness_centrality of nodes in both graph weighted and unweighted
    l_bc_in_weighted   = nx.betweenness_centrality(PMFG_weighted)
    l_bc_in_unweighted = nx.betweenness_centrality(PMFG_weighted, weight=None)

    # Get list closeness_centrality of nodes in both graph weighted and unweighted
    l_cc_in_weighted   = nx.closeness_centrality(PMFG_weighted)
    l_cc_in_unweighted = nx.closeness_centrality(PMFG_unweighted)

    # Get list eigenvector_centrality of nodes in both graph weighted and unweighted
    l_ec_in_weighted   = nx.eigenvector_centrality_numpy(PMFG_weighted)
    l_ec_in_unweighted = nx.eigenvector_centrality_numpy(PMFG_weighted, weight=None)

    # Get list eccentricity of nodes in both graph weighted and unweighted
    l_e_in_weighted    = nx.eccentricity(PMFG_weighted)
    l_e_in_unweighted  = nx.eccentricity(PMFG_unweighted)
    
    vertices = []
    
    for w, uw in zip(l_d_in_weighted, l_d_in_unweighted):
        label_w = w[0]
        degree_w = w[1]
        label_uw = uw[0]
        degree_uw = uw[1]
        
        x = (degree_w + degree_uw + l_bc_in_weighted[label_w] + l_bc_in_unweighted[label_uw]) / (4 * (len(labels_of_nodes) - 1))
        y = (l_cc_in_weighted[label_w] + l_cc_in_unweighted[label_uw] +
             l_ec_in_weighted[label_w] + l_ec_in_unweighted[label_uw] +
             l_e_in_weighted[label_w]  + l_e_in_unweighted[label_uw]) / (6 * (len(labels_of_nodes) - 1))
        centrality_score =  x / y
        
        v = Vertex(label_w, centrality_score)
        vertices.append(v)
        
    vertices = sorted(vertices, key=lambda v: (v.centrality_score), reverse=True)
    
    central     = vertices[:nb_nodes_central]
    peripheral  = vertices[-nb_nodes_peripheral:]
    
    return {'central':central, 'peripheral':peripheral}