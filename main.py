"""
i wrote this copyright stuff csc111
"""

from read_data import *

from graph_construction import load_user_product_graph
from load_graph2 import get_all_pairs, counting_pairs, load_graph2
from recommend_byg2 import recommend
import matplotlib.pyplot as plt
import plotly.graph_objects as go
import networkx as nx


def visualize_plotly_graph(G_nx, title: str, node_color: str, edge_color: str, node_size: int):
    """
    //
    """
    pos = nx.spring_layout(G_nx, seed=42)

    # Set up edge trace
    edge_x = []
    edge_y = []
    for edge in G_nx.edges():
        x0, y0 = pos[edge[0]]
        x1, y1 = pos[edge[1]]
        edge_x.extend([x0, x1, None])
        edge_y.extend([y0, y1, None])

    edge_trace = go.Scatter(
        x=edge_x, y=edge_y,
        line=dict(width=0.8, color=edge_color),
        hoverinfo='none',
        mode='lines')

    # Set up node trace
    node_x = []
    node_y = []
    for node in G_nx.nodes():
        x, y = pos[node]
        node_x.append(x)
        node_y.append(y)

    node_trace = go.Scatter(
        x=node_x, y=node_y,
        mode='markers',
        hoverinfo='text',
        marker=dict(
            showscale=True,
            colorscale='YlGnBu',
            size=node_size,
            color=node_color,
            opacity=0.8,
            line=dict(width=2)))

    # Add node labels
    node_text = ['Product: {}'.format(node) for node in G_nx.nodes()]
    node_trace.text = node_text

    # Create figure
    fig = go.Figure(data=[edge_trace, node_trace],
                    layout=go.Layout(
                        title=title,
                        showlegend=False,
                        hovermode='closest',
                        margin=dict(b=20, l=5, r=5, t=40),
                        xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                        yaxis=dict(showgrid=False, zeroline=False, showticklabels=False)
                    ))
    fig.show()


def main():
    """
    main
    """


if __name__ == "__main__":
    review_data = load_clean_review_data("All_Beauty.jsonl")
    product_data = load_clean_product_data("meta_All_Beauty.jsonl")
    g1 = load_user_product_graph(review_data, product_data)
    pairs_lst = get_all_pairs(g1)
    pairs_dict = counting_pairs(pairs_lst)
    g2 = load_graph2(g1, pairs_dict)
    G_user_product = g1.to_networkx()
    pairs_list = get_all_pairs(g1)
    G_product_product = g2.to_networkx()

    # For interactive visualization using Plotly
    visualize_plotly_graph(G_user_product, 'User-Product Graph', node_color='blue', edge_color='rgba(50,50,50,0.2)',
                           node_size=10)

    visualize_plotly_graph(G_product_product, 'Product-Product Graph', node_color='lightseagreen',
                           edge_color='rgba(150,150,150,0.4)', node_size=10)

    results = recommend(g2, 'Nurbo Handmade Love Owl wings Multilayer Knit Leather Rope Chain Bracelet', 10)
    for result in results:
        print(result)
    ##################################
    # the following are test cases( the product newly bought)
    # '16 oz, Pink - Bargz Perfume - Pink Friday By Nikki Minaj Body Oil For Women Scented Fragrance', 10)
    # SALUX Nylon Japanese Beauty Skin Bath Wash cloth Towel Yellow'
    # Nurbo Handmade Love Owl wings Multilayer Knit Leather Rope Chain Bracelet
