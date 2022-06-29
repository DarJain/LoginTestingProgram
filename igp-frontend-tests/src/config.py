import json

from mergedeep import merge

from response import error


def load_config(file_name):
    try:
        with open(f"./configuration/{file_name}.json") as config_file:
            return json.load(config_file)
    except FileNotFoundError as e:
        error(e)
        return {}


configuration = load_config("configuration")
credentials = load_config("credentials")

portals = merge(configuration, credentials)
