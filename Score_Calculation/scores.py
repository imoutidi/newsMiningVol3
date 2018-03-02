

# Creating a nested dictionary with depth 2 which will
# contain the relation score between two entities that
# are detected in the parsed articles.
def article_level_score(entity_nested_dict, entity_list, r_type):

    frequencies = entity_article_frequency(entity_list)
    relations_weights = calculate_relations_weights(frequencies, r_type)

    return entity_nested_dict


def calculate_relations_weights(freqs, rel_type):
    frequency_sum = calculate_frequency_sum(freqs, rel_type)


    return 0


def calculate_frequency_sum(freqs, r_type):
    values = []
    for r_t in r_type:
        values += list(freqs["P"].values())
        values += list(freqs["L"].values())
        values += list(freqs["O"].values())

    return sum(values)


# This will probably be deleted
def calculate_product_sum(freqs):
    values = list(freqs["P"].values())
    values += list(freqs["L"].values())
    values += list(freqs["O"].values())

    temp_product = 0
    for idx, out_val in enumerate(values):
        for in_val in values[idx+1:]:
            temp_product += out_val * in_val

    return temp_product


def entity_article_frequency(ent_list):
    all_persons = dict()
    all_locations = dict()
    all_organizations = dict()
    entity_frequencies = dict()

    for sent_dict in ent_list:
        # all_persons = all_persons.union(set(sub_list["PERSON"]))
        # all_locations = all_locations.union(set(sub_list["LOCATION"]))
        # all_organizations = all_organizations.union(set(sub_list["ORGANIZATION"]))
        for entity in sent_dict["P"]:
            if entity in all_persons:
                all_persons[entity] += 1
            else:
                all_persons[entity] = 1
        for entity in sent_dict["L"]:
            if entity in all_locations:
                all_locations[entity] += 1
            else:
                all_locations[entity] = 1
        for entity in sent_dict["O"]:
            if entity in all_organizations:
                all_organizations[entity] += 1
            else:
                all_organizations[entity] = 1
    entity_frequencies["P"] = all_persons
    entity_frequencies["L"] = all_locations
    entity_frequencies["O"] = all_organizations

    return entity_frequencies
