"""CSC111 Winter 2024 Project2: read_data

Overview
===============================

This Python module contains functions responsible for loading JSONL datasets
into usable lists of dictionaries for the rest of the project.

Copyright and Usage Information
===============================

This file is provided solely for grading by instructors and TAs of CSC111.
at the University of Toronto St. George campus. All forms of distribution
of this code, whether as given or with any changes, are expressly prohibited.

This file is Copyright (c) 2024 Ying Zhang, Zhixiao Fu, Yufei Chen, Julie Sun
"""
import json


def load_clean_review_data(review_data: str) -> list[dict[str, str]]:
    """
    Reads review data json file into a list of dicts without unverified purchases
    """
    with open(review_data, 'r') as file:
        data = []
        keys_to_read = ["rating", "parent_asin", "user_id", "timestamp", "verified_purchase"]
        for line in file:
            line_dict = json.loads(line.strip())
            selected_data = {key: line_dict[key] for key in keys_to_read}
            conditions1 = line_dict["rating"] != "" and line_dict["parent_asin"] != ""
            conditions2 = line_dict["user_id"] != "" and line_dict["timestamp"] != ""
            if line_dict["verified_purchase"] and conditions1 and conditions2:
                data.append(selected_data)
    return data


def load_clean_product_data(product_data: str) -> list[dict[str, str]]:
    """
    Reads product data json file into a list of dicts
    """
    with open(product_data, 'r') as file:
        data = []
        keys_to_read = ["main_category", "title", "parent_asin", "description"]
        for line in file:
            line_dict = json.loads(line.strip())
            selected_data = {key: line_dict[key] for key in keys_to_read}
            conditions = line_dict["parent_asin"] != "" and line_dict["description"] != ""
            if line_dict["main_category"] != "" and line_dict["title"] != "" and conditions:
                data.append(selected_data)
    return data
