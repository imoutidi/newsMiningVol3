


# Creating a nested dictionary with depth 2 which will
# contain the relation score between two entities that
# are detected in the parsed articles.
def article_level_score(entity_nested_dict, entity_list, entity_key):
    all_persons = set()
    all_locations = set()
    all_organizations = set()

    for sub_list in entity_list:
        all_persons = all_persons.union(set(sub_list[entity_key]))

    return entity_nested_dict
