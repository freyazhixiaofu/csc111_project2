"""we already have the graph with product to product vertices. now a user just bought a product.
we need to recommend <limit> number of product to them"""
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
            if subnb != nb and subnb != ver_newly:  # before adding the subnb != ver_newly, \
                # why can the neighbour of nb be vernewly's neighbour??
                # potential bug: the same product has the product itself being its neighbour?
                rec_tuple.append(((g.get_weight(nb, ver_newly) + g.get_weight(nb, subnb)) / 2, subnb.name))

    rec_tuple.sort(key=lambda x: (x[0], x[1]), reverse=True)
    return [p[1] for p in rec_tuple[:limit]]
