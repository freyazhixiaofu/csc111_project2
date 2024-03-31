"""
i wrote this copyright and stuff csc111
"""
import json
# not currently used, can print data, copied from ucsd 2023 website
# pprint = lambda x: print(json.dumps(x, indent=2)) if isinstance(x, dict) else display(x)


def load_clean_review_data(review_data: str) -> list[dict[str, str]]:
    """
    Reads review data json file into a list of dicts without unverified purchases
    """
    with open(review_data, 'r') as file:
        data = []
        for line in file:
            line_dict = json.loads(line.strip())
            # pprint(json.loads(line.strip()))   <-- prints data nicely
            # removes unverified purchases
            if line_dict["verified_purchase"]:
                data.append(line_dict)
    return data


def load_clean_product_data(product_data: str) -> list[dict[str, str]]:
    """
    Reads product data json file into a list of dicts
    """
    with open(product_data, 'r') as file:
        data = []
        keys_to_read = ["title", "description", "asin"]  # can add more if needed
        for line in file:
            line_dict = json.loads(line.strip())
            selected_data = {key: line_dict[key] for key in keys_to_read}
            data.append(selected_data)
    return data
