"""CSC111 Winter 2024 Project2: main

Overview
===============================

This Python module contains a function responsible for visualization of a Plotly graph,
and the 'main' code responsible for computing the result of the entire program.

Copyright and Usage Information
===============================

This file is provided solely for grading by instructors and TAs of CSC111.
at the University of Toronto St. George campus. All forms of distribution
of this code, whether as given or with any changes, are expressly prohibited.

This file is Copyright (c) 2024 Ying Zhang, Zhixiao Fu, Yufei Chen, Julie Sun
"""

import plotly.graph_objects as go
import networkx as nx
import read_data
from graph_construction import load_user_product_graph
from load_graph2 import get_all_pairs, counting_pairs, load_graph2
from recommend_byg2 import recommend


def generate_edge_traces(g_nx: nx.Graph, pos: dict) -> list[go.Scatter]:
    """
    Generates edge traces for a networkx graph visualization.

    Parameters:
    - g_nx (nx.Graph): The networkx graph.
    - pos (dict): A dictionary specifying the positions of nodes in the graph.

    Returns:
    - List[go.Scatter]: A list of plotly Scatter objects representing the graph edges.
    """
    edge_trace = []
    for edge in g_nx.edges(data=True):
        x0, y0 = pos[edge[0]]
        x1, y1 = pos[edge[1]]
        weight = edge[2].get('weight', 1)
        edge_trace.append(go.Scatter(x=[x0, x1, None], y=[y0, y1, None],
                                     mode='lines',
                                     line={"width": 0.5, "color": "black"},
                                     hoverinfo='text',
                                     text=[f'Weight: {weight}']))
    return edge_trace


def generate_node_traces(g_nx: nx.Graph, pos: dict) -> go.Scatter:
    """
    Generates node traces for a networkx graph visualization, including a color bar
    to represent node degree.

    Parameters:
    - g_nx (nx.Graph): The networkx graph.
    - pos (dict): A dictionary specifying the positions of nodes in the graph.

    Returns:
    - go.Scatter: A plotly Scatter object representing the graph nodes, with a color bar
                  indicating the degree of each node.
    """
    node_x, node_y, node_color = [], [], []
    for node in g_nx.nodes():
        x, y = pos[node]
        node_x.append(x)
        node_y.append(y)
        # Use node degree as a proxy for color intensity
        node_color.append(g_nx.degree[node])

    node_trace = go.Scatter(x=node_x, y=node_y,
                            mode='markers',
                            hoverinfo='text',
                            marker={"size": 10,
                                    "color": node_color,
                                    "colorscale": "Viridis",
                                    "showscale": True,
                                    "colorbar": {"title": "Degree"},
                                    "line": {"width": 0.5}})

    node_text = []
    for node in g_nx.nodes(data=True):
        if node[1].get('kind') != 'product':
            label = f'User ID: {node[0]}'
        else:
            label = f'Product : {node[0]}'
        node_text.append(label)
    node_trace.text = node_text

    return node_trace


def visualize_graph(g_nx: nx.Graph, title: str) -> None:
    """
    Visualizes a weighted graph using Plotly, specifically tailored for the
    network graph built from the networkx Graph class. This function utilizes
    helper functions to generate edge and node traces for the visualization.

    Parameters:
    - g_nx (nx.Graph): The networkx graph to visualize.
    - title (str): The title of the graph visualization.
    """
    pos = nx.spring_layout(g_nx, seed=42)

    edge_trace = generate_edge_traces(g_nx, pos)
    node_trace = generate_node_traces(g_nx, pos)

    fig = go.Figure(data=edge_trace + [node_trace],
                    layout=go.Layout(title=title,
                                     showlegend=False,
                                     hovermode='closest',
                                     margin={"b": 0, "l": 0, "r": 0, "t": 40},
                                     xaxis={"showgrid": False, "zeroline": False, "showticklabels": False},
                                     yaxis={"showgrid": False, "zeroline": False, "showticklabels": False}))

    fig.show()


if __name__ == "__main__":
    the_product = input("What product would you like a recommendation for?")
    product_data1 = load_clean_product_data("meta_All_Beauty.jsonl")
    product_data2 = load_clean_product_data("meta_Gift_Cards.jsonl")
    product_data = product_data1 + product_data2

    product_category = ""
    for product in product_data:
        if product["title"] == the_product:
            product_category = product["main_category"]
    while product_category == "":
        the_product = input("What product would you like a recommendation for?")
        for product in product_data:
            if product["title"] == the_product:
                product_category = product["main_category"]

    review_data = load_clean_review_data(f"{product_category.replace(" ", "_")}.jsonl")
    product_datas = {"All Beauty": product_data1, "Gift Cards": product_data2}

    g1 = load_user_product_graph(review_data, product_datas[product_category])
    pairs_lst = get_all_pairs(g1)
    pairs_dict = counting_pairs(pairs_lst)
    g2 = load_graph2(g1, pairs_dict)
    G_user_product = g1.to_networkx()
    pairs_list = get_all_pairs(g1)
    G_product_product = g2.to_networkx()

    # For interactive visualization using Plotly
    visualize_graph(G_user_product, 'User-Product Graph')

    visualize_graph(G_product_product, 'Product-Product Graph')

    # results = recommend(g2, 'Plastic Ointment Jars With Lids 1 Oz 10/pkg', 10)
    # print(results)
    results = recommend(g2, the_product, 10)
    for result in results:
        print(result)
    ##################################
    # the following are test cases( the product newly bought)
    # 16 oz, Pink - Bargz Perfume - Pink Friday By Nikki Minaj Body Oil For Women Scented Fragrance
    # SALUX Nylon Japanese Beauty Skin Bath Wash cloth Towel Yellow
    # Nurbo Handmade Love Owl wings Multilayer Knit Leather Rope Chain Bracelet
