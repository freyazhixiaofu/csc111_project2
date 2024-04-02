from __future__ import annotations
from typing import Optional, Any, Union
import networkx as nx
from graph_construction import Graph


class _WeightedVertex:  # NOT CHANGED YET DOCSTRING
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

    def __init__(self, name: Any) -> None:
        """Initialize a new vertex with the name passed in.
        This initialization initializes self with no neighbours.
        """
        self.name = name
        self.neighbours = {}


class WeightedGraph:
    """A weighted graph used to represent the connection between products.
    All the vertices in the graph are products.

    Private Instance Attributes:
    _vertices: all the vertices, or products, in the graph. It is a dictionary mapping the product name to the
      weighted vertex.
      If an edge is added between two products, that means there is a connection between the two, the weight of the edge
      between any two procuts represents how strong their connection is. """

    _vertices: dict[Any, _WeightedVertex]

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


def counting_pairs(lst) -> dict[tuple: int]:
    """Counts the number of occurrences of each pair of products, which represents double of the number of users that
    purhcased both products, in the list passed in.
    Returns a dictionary mapping the tuple with the corresponding number of occurrences in the lst passed in.
    Note that

    lst = [(1, 4), (2, 6), (3, 4), (10, 22), (1, 4), (1, 4), (3, 4), (3, 4), (10, 22), (10, 22), (3, 4)]
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

    >>>
    """
    lst = []
    products = g.get_all_vertices('product')
    for p in products:
        for user in g.get_vertex(p).neighbours:
            assert g.adjacent(user.item, p)
            for also_bought in user.neighbours:
                pair_list = sorted([p, also_bought.item])
                assert g.adjacent(user.item, also_bought.item)
                lst.append((pair_list[0], pair_list[1]))
    return lst


def calculate_weight(rating1: float, rating2: float, time1: float, time2: float, occurrences: int) -> float:
    """Calculate how strong the connection is between any two products when given their average rating, average
    time stamp, and the number of users who have purchased both products.

    A formula will be used to compute the weight.
    >>> calculate_weight(3, 4, 8232141241332, 8231231434122, 4)
    6
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


    >>> g = load_user_product_graph('All_Beauty.jsonl', 'meta_All_Beauty.jsonl')
    >>> g2 = load_graph2(g, )
    >>> len(g.get_all_vertices(kind='product'))
    108924
    >>> len(g.get_all_vertices(kind='user'))
    578813
    >>> user1_reviews = g.get_neighbours("AGKHLEW2SOWHNMFQIJGBECAF7INQ")
    >>> len(user1_reviews)
    2

    """
    g2 = WeightedGraph()
    for tup in d:
        if d[tup] // 2 >= 2:
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
    return g2
