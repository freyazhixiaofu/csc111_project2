"""
i wrote this copyright stuff csc111
"""

from read_data import *

from graph_construction import load_user_product_graph
from load_graph2 import get_all_pairs, counting_pairs, load_graph2
from recommend_byg2 import recommend

if __name__ == "__main__":
    review_data = load_clean_review_data("All_Beauty.jsonl")
    product_data = load_clean_product_data("meta_All_Beauty.jsonl")
    g1 = load_user_product_graph(review_data, product_data)
    pairs_lst = get_all_pairs(g1)
    pairs_dict = counting_pairs(pairs_lst)
    g2 = load_graph2(g1, pairs_dict)

    results = recommend(g2, 'Plastic Ointment Jars With Lids 1 Oz 10/pkg', 10)
    print(results)
