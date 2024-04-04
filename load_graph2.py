"""CSC111 Winter 2024 Project2: load_graph2

Overview
===============================

This python module contians the necessary classes and functions that are required to
loads our second graph, a product to product graph where the connection between the products
is being displayed.

Copyright and Usage Information
===============================

This file is provided solely for grading by instructors and TAs of CSC111.
at the University of Toronto St. George campus. All forms of distribution
of this code, whether as given or with any changes, are expressly prohibited.

This file is Copyright (c) 2024 Ying Zhang, Zhixiao Fu, Yufei Chen, Julie Sun
"""

from __future__ import annotations
from typing import Any, Union
import networkx as nx
from load_graph1 import Graph


class _WeightedVertex:
    """A vertex in a weighted product connection graph. There ar e

    Instance Attributes:

    - item: The data stored in this vertex, representing a product.
    - neighbours: The vertices that are adjacent to this vertex, and their corresponding
        edge weights, hence will be a mapping from a vertex to the weight of the edge connecting self and its
        neighour vertex.

    Representation Invariants:
    - self not in self.neighbours
    - all(self in u.neighbours for u in self.neighbours)"""

    name: Any
    neighbours: dict[_WeightedVertex, Union[int, float]]
    kind: str

    def __init__(self, name: Any) -> None:
        """Initialize a new vertex with the name passed in.
        This initialization initializes self with no neighbours.
        """
        self.name = name
        self.neighbours = {}
        self.kind = 'product'


class WeightedGraph:
    """A weighted graph used to represent the connection between products.
    All the vertices in the graph are products.

    Private Instance Attributes:
    _vertices: all the vertices, or products, in the graph. It is a dictionary mapping the product name to the
      weighted vertex.
      If an edge is added between two products, that means there is a connection between the two, the weight of the edge
      between any two procuts represents how strong their connection is. """

    _vertices: dict[str, _WeightedVertex]  # changed Any to str

    def __init__(self) -> None:
        """Initialize an empty graph with no vertices or edges."""
        self._vertices = {}

    def add_vertex(self, name: Any) -> None:
        """Add a vertex with the provided name.

        vertex initialized with no neighbours
        If the given item with the given name is already in this graph, nothing is done.
        """
        if name not in self._vertices:
            self._vertices[name] = _WeightedVertex(name)

    def add_edge(self, name1: Any, name2: Any, weight: Union[int, float]) -> None:
        """Add an edge between the two vertices with the given items in this graph,
        with the given weight.

        Raise a ValueError if name1 or name2 do not appear as vertices in this graph.

        Preconditions:
        - name1 != name2"""
        if name1 in self._vertices and name2 in self._vertices:
            v1 = self._vertices[name1]
            v2 = self._vertices[name2]

            v1.neighbours[v2] = weight
            v2.neighbours[v1] = weight
        else:
            raise ValueError

    def get_dict_vertices(self) -> dict:
        """return the dictionary of all products in weighted graph"""
        return self._vertices

    def get_weight(self, v_p1: _WeightedVertex, v_p2: _WeightedVertex) -> float:
        """given the names of the two products, return the weight on their edge."""
        return v_p1.neighbours[v_p2]

    def adjacent(self, p1: str, p2: str) -> bool:
        """If two products are adjacent in the graph"""
        if not (p1 in self._vertices and p2 in self._vertices):
            raise ValueError
        v1 = self._vertices[p1]
        return any(v2.name == p2 for v2 in v1.neighbours)

    def get_all_vertices(self) -> set[str]:
        """A set of all the product names in the graph"""
        return {v.name for v in self._vertices.values()}

    def to_networkx(self, max_vertices: int = 5000) -> nx.Graph:
        """Convert this graph into a networkx Graph.

        max_vertices specifies the maximum number of vertices that can appear in the graph.
        (This is necessary to limit the visualization output for large graphs.)

        Note that this method is provided for you, and you shouldn't change it.
        """
        graph_nx = nx.Graph()
        for v in self._vertices.values():
            graph_nx.add_node(v.name, kind='product')

            for u in v.neighbours.keys():
                if graph_nx.number_of_nodes() < max_vertices:
                    graph_nx.add_node(u.name, kind="product")

                if u.name in graph_nx.nodes:
                    graph_nx.add_edge(v.name, u.name, weight=v.neighbours[u])

            if graph_nx.number_of_nodes() >= max_vertices:
                break

        return graph_nx


def counting_pairs(lst: list) -> dict[tuple: int]:
    """Counts the number of occurrences of each pair of products, which represents double of the number of users that
    purhcased both products, in the list passed in.
    Returns a dictionary mapping the tuple with the corresponding number of occurrences in the lst passed in.
    Note that

    >>> lst = [(1, 4), (2, 6), (3, 4), (10, 22), (1, 4), (1, 4), (3, 4), (3, 4), (10, 22), (10, 22), (3, 4)]
    >>> d = counting_pairs(lst)
    >>> d
    {(1, 4): 3, (2, 6): 1, (3, 4): 4, (10, 22): 3}
    """
    d = {}
    for tup in lst:
        d[tup] = d.setdefault(tup, 0) + 1
    return d


def get_all_pairs(g: Graph) -> list[tuple]:
    """We will get the duplicate of all the occurrences of the pairs of the products that are bought by the same person.
    each pair will be represented by a tuple
    Notice that because the first grpah is a bipartite graph, every product's neighbour is a user, and every product's
    neighbour's neighbour is another product bought by the same user. Hence, this function is finding all the
    pairs of products bought by the same user.
    Essentially we will traverse through the graph each product's neighbour's neighbour and the original product.
    However, notice that each pair is traversed through twice.

    A postcondition is that all the tuples in the list must be sorted in alphabetical order.

    """
    lst = []
    products = g.get_all_vertices('product')
    for p in products:
        connected_v = get_double_nb(p, g)
        for product in connected_v:
            pair_list = sorted([product, p])
            lst.append((pair_list[0], pair_list[1]))
    return lst


def get_double_nb(v: str, g: Graph) -> list[str]:
    """Get neighbour's neighbours that are not itself"""
    s = []
    for nb in g.get_vertex(v).neighbours:
        for nb2 in nb.neighbours:
            if nb2.item != v:
                s.append(nb2.item)
    return s


def calculate_weight(rating1: float, rating2: float, time1: float, time2: float, occurrences: int) -> float:
    """Calculate how strong the connection is between any two products when given their average rating, average
    time stamp, and the number of users who have purchased both products.

    A formula will be used to compute the weight.
    >>> calculate_weight(3, 4, 8232141241332, 8231231434122, 4)
    3385
    """
    time_diff = int(pow(10, -10) * (time1 - time2))
    if time_diff == 0:
        time_weight = pow(35, 2)
    else:
        time_weight = pow(35, 2) - pow(time_diff, 2)
    return (rating1 + rating2) * 80 + time_weight + occurrences * 400


def load_graph2(g1: Graph, d: dict[tuple: int]) -> WeightedGraph:
    """Load the second grpah from the first graph.
     The second graph is a weighted graph with every vertex representing a product.
    Two products are adjacent in this graph if their connection is above a crtian threshold and there are two or more
    users who purchased both.

    the weight for each product represents how strong the connection between the two products are.

    We will divide the number of occurrences of each pair by two to get the real number of users who have purchased
    both products in the past.

    # >>> g = load_user_product_graph('All_Beauty.jsonl', 'meta_All_Beauty.jsonl')
    # >>> g2 = load_graph2(g, )
    # >>> len(g.get_all_vertices(kind='product'))
    # 108924
    # >>> len(g.get_all_vertices(kind='user'))
    # 578813
    # >>> user1_reviews = g.get_neighbours("AGKHLEW2SOWHNMFQIJGBECAF7INQ")
    # >>> len(user1_reviews)
    # 2

    """
    g2 = WeightedGraph()
    for tup in d:
        if d[tup] // 2 >= 1:
            if d[tup] // 2 >= 3:
                v1 = g1.get_vertex(tup[0])
                v2 = g1.get_vertex(tup[1])
                rating1 = sum(v1.all_review) / len(v1.all_review)
                rating2 = sum(v2.all_review) / len(v2.all_review)
                time1 = sum(v1.all_time_stamp) / len(v1.all_time_stamp)
                time2 = sum(v2.all_time_stamp) / len(v2.all_time_stamp)
                occurrences = d[tup]
                weight = calculate_weight(rating1, rating2, time1, time2, occurrences)
                g2.add_vertex(tup[0])
                g2.add_vertex(tup[1])
                g2.add_edge(tup[0], tup[1], weight)
                # if g2.adjacent(tup[0], tup[1]):
                #     print(f'...{g2.get_all_vertices()}...lol')
    return g2


if __name__ == '__main__':
    # You can uncomment the following lines for code checking/debugging purposes.
    # However, we recommend commenting out these lines when working with the large
    # datasets, as checking representation invariants and preconditions greatly
    # increases the running time of the functions/methods.
    # import python_ta.contracts
    # python_ta.contracts.check_all_contracts()

    import doctest

    doctest.testmod(verbose=True)

    import python_ta

    python_ta.check_all(config={
        'max-line-length': 120,
        'extra-imports': ['networkx', "graph_construction"],
        'max-nested-blocks': 4
    })
