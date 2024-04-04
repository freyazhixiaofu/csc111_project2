"""CSC111 Winter 2024 Project2: Graph Consrtuction

Instructions (READ THIS FIRST!)
===============================

This Python module contains...

Copyright and Usage Information
===============================

This file is provided solely ...

This file is Copyright (c) ...
"""
from __future__ import annotations
from typing import Any, Optional
import json
import networkx as nx  # Used for visualizing graphs (by convention, referred to as "nx")
from read_data import load_clean_product_data, load_clean_review_data

class _Vertex:  # self written
    """A Vertex is either a User or a Product.
    If the Vertex is a Product, then it will have a "date" attrbute that

    Instance Attributes:
        - name: The data stored in this vertex, representing a user or book.
        - kind: The type of this vertex: 'user' or 'product'.
        - neighbours: The vertices that are adjacent to this vertex.
        - all_time_stam: a list recording the time stamp upon each purchase of the product. This is only an attribute
        for products.
        - review: a list recordn the review upon each review of the product. This is only an attribute for products.

    Representation Invariants:
        - self not in self.neighbours
        - all(self in u.neighbours for u in self.neighbours)
        - self.kind in {'user', 'product'}

    """
    item: Any
    kind: str
    neighbours: set[_Vertex]
    all_time_stamp: Optional[list[int]]
    all_review: Optional[list[float]]

    def __init__(self, item: Any, kind: str) -> None:
        """Initialize a new vertex with the given item and kind.

        This vertex is initialized with no neighbours.

        Preconditions:
            - kind in {'user', 'product'}
        """
        self.item = item
        self.kind = kind
        self.neighbours = set()
        if kind == 'product':
            self.all_time_stamp = []
            self.all_review = []
        else:
            self.all_time_stamp = None
            self.all_review = None

    def degree(self) -> int:
        """Return the degree of this vertex based on how many neighbours it has."""
        return len(self.neighbours)


class Graph:
    """The User-Product Graph.
    This graph is bipartite, with one set of nodes representing users and another set representing products.
    An edge between a user node and a product node indicates that the user has purchased that product.
    """
    # Private Instance Attributes:
    #     - _vertices:
    #         A collection of the vertices contained in this graph.
    #         Maps item to _Vertex object.
    _vertices: dict[Any, _Vertex]

    def __init__(self) -> None:
        """Initialize an empty graph (no vertices or edges)."""
        self._vertices = {}

    def add_vertex(self, item: Any, kind: str) -> None:
        """Add a vertex with the given item and kind to this graph.

        The new vertex is not adjacent to any other vertices.
        Do nothing if the given item is already in this graph.

        Preconditions:
            - kind in {'user', 'book'}
        """
        if item not in self._vertices:
            self._vertices[item] = _Vertex(item, kind)

    def add_edge(self, item1: Any, item2: Any) -> None:
        """Add an edge between the two vertices with the given items in this graph.

        Raise a ValueError if item1 or item2 do not appear as vertices in this graph.

        Preconditions:
            - item1 != item2
        """
        if item1 in self._vertices and item2 in self._vertices:
            v1 = self._vertices[item1]
            v2 = self._vertices[item2]

            v1.neighbours.add(v2)
            v2.neighbours.add(v1)
        else:
            raise ValueError

    def add_user(self, user_id: str) -> None:
        """Add a user vertex to the graph.

        Raise ValueError:
        - If there's an attempt to add a user that already exists as a product.
        """
        if user_id in self._vertices:
            if self._vertices[user_id].kind != 'user':
                raise ValueError
        else:
            self.add_vertex(user_id, 'user')

    def add_product(self, product_title: str, time: int, rate: float) -> None:
        """Add a product vertex to the graph.

        Raise ValueError:
        - If there's an attempt to add a product that already exists as a user.
        """
        if product_title in self._vertices:
            if self._vertices[product_title].kind != 'product':
                raise ValueError
        else:
            self.add_vertex(product_title, 'product')
            self._vertices[product_title].all_time_stamp.append(time)
            self._vertices[product_title].all_review.append(rate)

    def add_purchase(self, user_id: str, product_id: str) -> None:
        """Add an edge to represent a purchase between a user and a product.

        Preconditions:
            - The user_id and product_id vertices have been added to the graph.
        """
        self.add_edge(user_id, product_id)

    def adjacent(self, item1: Any, item2: Any) -> bool:
        """Return whether item1 and item2 are adjacent vertices in this graph.

        Return False if item1 or item2 do not appear as vertices in this graph.
        """
        if item1 in self._vertices and item2 in self._vertices:
            v1 = self._vertices[item1]
            return any(v2.item == item2 for v2 in v1.neighbours)
        else:
            return False

    def get_neighbours(self, item: Any) -> set:
        """Return a set of the neighbours of the given item.

        Note that the *items* are returned, not the _Vertex objects themselves.

        Raise a ValueError if item does not appear as a vertex in this graph.
        """
        if item in self._vertices:
            v = self._vertices[item]
            return {neighbour.item for neighbour in v.neighbours}
        else:
            raise ValueError

    def get_all_vertices(self, kind: str = '') -> set:
        """Return a set of all vertex items in this graph.

        If kind != '', only return the items of the given vertex kind.

        Preconditions:
            - kind in {'', 'user', 'book'}
        """
        if kind != '':
            return {v.item for v in self._vertices.values() if v.kind == kind}
        else:
            return set(self._vertices.keys())

    def to_networkx(self, max_vertices: int = 5000) -> nx.Graph:
        """Convert this graph into a networkx Graph.

        max_vertices specifies the maximum number of vertices that can appear in the graph.
        (This is necessary to limit the visualization output for large graphs.)

        Note that this method is provided for you, and you shouldn't change it.
        """
        graph_nx = nx.Graph()
        for v in self._vertices.values():
            graph_nx.add_node(v.item, kind=v.kind)

            for u in v.neighbours:
                if graph_nx.number_of_nodes() < max_vertices:
                    graph_nx.add_node(u.item, kind=u.kind)

                if u.item in graph_nx.nodes:
                    graph_nx.add_edge(v.item, u.item)

            if graph_nx.number_of_nodes() >= max_vertices:
                break

        return graph_nx

    def create_co_purchase_dict(self) -> dict:
        """Create a dictionary counting the number of times each pair of products was co-purchased.
        """
        co_purchase_counts = {}
        for product in self.get_all_vertices('product'):
            for user in self.get_neighbours(product):
                for co_purchased_product in self.get_neighbours(user):
                    # Too many for loops here!
                    if co_purchased_product != product:
                        product_pair = tuple(sorted((product, co_purchased_product)))
                        co_purchase_counts[product_pair] = co_purchase_counts.get(product_pair, 0) + 1
        return co_purchase_counts

    def get_vertex(self, item: str) -> _Vertex:
        """Returns the vertex with the corresponding name of the vertex in the graph.
        Preconditions:

        item in self._Vertices"""

        return self._vertices[item]


def load_user_product_graph(review_data: list[dict[str, str]], product_data: list[dict[str, str]]) -> Graph:
    """Return a user-product graph based on the given datasets.

    The user-product graph stores information from the reviews_file as follows:
    - Create one vertex for each user and one vertex for every unique product reviewed.
    - Edges represents the existence of a review between a user and a product.

    The vertices of the 'user' kind should have the user ID as its item.
    The vertices of the 'product' kind should have the product title as its item.

    Note: Each edge only represents the existence of a review. Review scores are ignored.

    Preconditions:
        - reviews_file is the path to a JSON file corresponding to the review data.
        - products_file is the path to a JSON file corresponding to the product data.
    >>> review_data1 = load_clean_review_data("All_Beauty.jsonl")
    >>> product_data1 = load_clean_product_data("meta_All_Beauty.jsonl")
    >>> g = load_user_product_graph(review_data1, product_data1)
    >>> len(g.get_all_vertices(kind='product'))
    108924
    >>> len(g.get_all_vertices(kind='user'))
    578813
    >>> user1_reviews = g.get_neighbours("AGKHLEW2SOWHNMFQIJGBECAF7INQ")
    >>> len(user1_reviews)
    2
    """
    graph = Graph()

    product_id_to_title = {}
    for product_dict in product_data:
        product_id_to_title[product_dict["parent_asin"]] = product_dict["title"]
    for review_dict in review_data:
        user_id = review_dict['user_id']
        product_id = review_dict['parent_asin']
        timestamp = int(review_dict['timestamp'])
        rating = float(review_dict['rating'])
        if product_id in product_id_to_title:
            product_title = product_id_to_title[product_id]

            graph.add_user(user_id)
            graph.add_product(product_title, timestamp, rating)

            graph.add_edge(user_id, product_title)

    return graph

# def load_user_product_graph(reviews_file: str, products_file: str) -> Graph:
#     """Return a user-product graph based on the given datasets.
#
#     The user-product graph stores information from the reviews_file as follows:
#     - Create one vertex for each user and one vertex for every unique product reviewed.
#     - Edges represents the existence of a review between a user and a product.
#
#     The vertices of the 'user' kind should have the user ID as its item.
#     The vertices of the 'product' kind should have the product title as its item.
#
#     Note: Each edge only represents the ex    1istence of a review. Review scores are ignored.
#
#     Preconditions:
#         - reviews_file is the path to a JSON file corresponding to the review data.
#         - products_file is the path to a JSON file corresponding to the product data.
#
#     >>> g = load_user_product_graph('All_Beauty.jsonl', 'meta_All_Beauty.jsonl')
#     >>> len(g.get_all_vertices(kind='product'))
#     108924
#     >>> len(g.get_all_vertices(kind='user'))
#     578813
#     >>> user1_reviews = g.get_neighbours("AGKHLEW2SOWHNMFQIJGBECAF7INQ")
#     >>> len(user1_reviews)
#     2
#     """
#     graph = Graph()
#
#     product_id_to_title = {}
#     with open(products_file, 'r', encoding='utf-8') as file:
#         for line in file:
#             product_data = json.loads(line.strip())
#             product_id_to_title[product_data['parent_asin']] = product_data['title']
#
#     with open(reviews_file, 'r', encoding='utf-8') as file:
#         for line in file:
#             review_data = json.loads(line.strip())
#             user_id = review_data['user_id']
#             product_id = review_data['asin']
#
#             if product_id in product_id_to_title:
#                 product_title = product_id_to_title[product_id]
#
#                 graph.add_user(user_id)
#                 graph.add_product(product_title)
#
#                 graph.add_edge(user_id, product_title)
#
#     return graph


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
        'max-line-length': 100,
        'disable': ['E1136'],
        'extra-imports': ['csv', 'networkx'],
        'allowed-io': ['load_review_graph'],
        'max-nested-blocks': 4
    })
