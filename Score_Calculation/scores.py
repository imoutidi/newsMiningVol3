


# Creating a nested dictionary with depth 2 which will
# contain the relation score between two entities that
# are detected in the parsed articles.
def article_level_score(entity_nested_dict, entity_list, art_id):

    frequencies = entity_article_frequency(entity_list)
    sum_of_products = calculate_product_sum(frequencies)

    return entity_nested_dict


def calculate_product_sum(freqs):
    pass


def entity_article_frequency(ent_list):
    all_persons = dict()
    all_locations = dict()
    all_organizations = dict()
    entity_frequencies = dict()

    for sent_dict in ent_list:
        # all_persons = all_persons.union(set(sub_list["PERSON"]))
        # all_locations = all_locations.union(set(sub_list["LOCATION"]))
        # all_organizations = all_organizations.union(set(sub_list["ORGANIZATION"]))
        for entity in sent_dict["PERSON"]:
            if entity in all_persons:
                all_persons[entity] += 1
            else:
                all_persons[entity] = 1
        for entity in sent_dict["LOCATION"]:
            if entity in all_locations:
                all_locations[entity] += 1
            else:
                all_locations[entity] = 1
        for entity in sent_dict["ORGANIZATION"]:
            if entity in all_organizations:
                all_organizations[entity] += 1
            else:
                all_organizations[entity] = 1
    entity_frequencies["PERSON"] = all_persons
    entity_frequencies["LOCATION"] = all_locations
    entity_frequencies["ORGANIZATION"] = all_organizations

    return entity_frequencies
