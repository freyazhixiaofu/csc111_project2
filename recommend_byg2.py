"""CSC111 Winter 2024 Project2: recommend

Overview
===============================

This Python module imports the graph with product to product vertices. Suppose a user just bought a new product.
The function reccomend returns <limit> number of products that are closely related to the newly
bought product.

Copyright and Usage Information
===============================

This file is provided solely for grading by instructors and TAs of CSC111.
at the University of Toronto St. George campus. All forms of distribution
of this code, whether as given or with any changes, are expressly prohibited.

This file is Copyright (c) 2024 Ying Zhang, Zhixiao Fu, Yufei Chen, Julie Sun
"""

from load_graph2 import WeightedGraph

# updated 4.1.1.11


def recommend(g: WeightedGraph, newly: str, limit: int) -> list[str]:
    """return the list of products that are closely related to the\
     newly bought product within the given limit amount

     """
    if newly not in g.get_dict_vertices():  # {productname: WeightedVertices}
        return ["nothing to recommend"]

    ver_newly = g.get_dict_vertices()[newly]
    rec_tuple = []
    for nb in ver_newly.neighbours:
        rec_tuple.append((g.get_weight(nb, ver_newly), nb.name))
        for subnb in nb.neighbours:
            if subnb not in {nb, ver_newly}:  # before adding the subnb != ver_newly
                avg_weight = (g.get_weight(nb, ver_newly) + g.get_weight(nb, subnb)) / 2
                rec_tuple.append((avg_weight, subnb.name))

    rec_tuple.sort(key=lambda x: (x[0], x[1]), reverse=True)
    return [p[1] for p in rec_tuple[:limit]]


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
        'extra-imports': ['load_graph2'],
        'max-nested-blocks': 4
    })
