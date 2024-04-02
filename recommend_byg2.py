"""we already have the graph with product to product vertices. now a user just bought a product.
we need to recommend <limit> number of product to them"""
from load_graph2 import WeightedGraph

# updated 4.1.1.11


def recommend(g: WeightedGraph, newly: str, limit: int) -> list[str]:
    """return the list of products that are closely related to the\
     newly bought product within the given limit amount

     """
    if newly not in [v.name for v in g.get_dict_vertices().values()]:
        return []
    all_product_ver = g.get_dict_vertices()[newly]  # g is a graph of dictionary with its name being "newly"
    # {productname: productVertex}
    neighbours_ver = [v for v in all_product_ver]
    subneighbour = []
    for u in neighbours_ver:
        for w in u.neighbour:
            subneighbour.append(w)
    all_possible_rec = neighbours_ver + subneighbour
    rec_tuple = [(ver.weight, ver.name) for ver in all_possible_rec]  # unsorted lst
    rec_tuple.sort(key=lambda x: (x[0], x[1]), reverse=True)
    return [p[1] for p in rec_tuple[:limit]]
