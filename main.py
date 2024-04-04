"""
i wrote this copyright stuff csc111
"""

from read_data import *

from graph_construction import load_user_product_graph
from load_graph2 import get_all_pairs, counting_pairs, load_graph2
from recommend_byg2 import recommend
import plotly.graph_objects as go
import networkx as nx


def visualize_weighted_graph(G_nx: nx.Graph, title: str):
    """
    Visualize a weighted graph using Plotly, specifically tailored for the
    network graph built from the WeightedGraph class.
    """
    pos = nx.spring_layout(G_nx, seed=42)  # Position nodes using the spring layout

    # Prepare edge traces with edge weights influencing line width
    edge_x = []
    edge_y = []
    edge_trace = []
    for edge in G_nx.edges(data=True):
        x0, y0 = pos[edge[0]]
        x1, y1 = pos[edge[1]]
        weight = edge[2]['weight'] if 'weight' in edge[2] else 1  # Use edge weight if available
        edge_trace.append(go.Scatter(x=[x0, x1, None], y=[y0, y1, None],
                                     mode='lines',
                                     line=dict(width=0.5, color='black'),  # Scale weight for visualization
                                     hoverinfo='text',
                                     text=[f'Weight: {weight}']))

    # Prepare node traces
    node_x = []
    node_y = []
    for node in G_nx.nodes():
        x, y = pos[node]
        node_x.append(x)
        node_y.append(y)

    node_trace = go.Scatter(x=node_x, y=node_y,
                            mode='markers',
                            hoverinfo='text',
                            marker=dict(showscale=True,
                                        colorscale='Viridis',
                                        size=10,
                                        color=list(dict(G_nx.degree).values()),
                                        colorbar=dict(title='Degree'),
                                        line_width=0.5))

    # Add node labels based on the node's attribute (assuming 'kind' attribute exists)
    node_text = [f'{node}' for node in G_nx.nodes()]
    node_trace.text = node_text

    # Create the figure
    fig = go.Figure(data=edge_trace + [node_trace],
                    layout=go.Layout(title=title,
                                     showlegend=False,
                                     hovermode='closest',
                                     margin=dict(b=0, l=0, r=0, t=40),
                                     xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                                     yaxis=dict(showgrid=False, zeroline=False, showticklabels=False)))

    fig.show()


def main():
    """
    main
    """


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
    visualize_weighted_graph(G_user_product, 'User-Product Graph')

    visualize_weighted_graph(G_product_product, 'Product-Product Graph')

    # results = recommend(g2, 'Plastic Ointment Jars With Lids 1 Oz 10/pkg', 10)
    # print(results)
    results = recommend(g2, the_product, 10)
    for result in results:
        print(result)
    ##################################
    # the following are test cases( the product newly bought)
    # '16 oz, Pink - Bargz Perfume - Pink Friday By Nikki Minaj Body Oil For Women Scented Fragrance', 10)
    # SALUX Nylon Japanese Beauty Skin Bath Wash cloth Towel Yellow'
    # Nurbo Handmade Love Owl wings Multilayer Knit Leather Rope Chain Bracelet
