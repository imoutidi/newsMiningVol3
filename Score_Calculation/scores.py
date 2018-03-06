

def article_level_score(all_articles_rel_weights, entity_list, r_type, art_id):
    frequencies = entity_article_frequency(entity_list)
    single_article_rel_weights = calculate_relations_weights(frequencies, r_type)
    for entity_couple in single_article_rel_weights:
        if entity_couple in all_articles_rel_weights:
            all_articles_rel_weights[entity_couple][0] += single_article_rel_weights[entity_couple]
            all_articles_rel_weights[entity_couple][1][art_id] = []
        else:
            all_articles_rel_weights[entity_couple] = [single_article_rel_weights[entity_couple], {art_id: []}]

    return all_articles_rel_weights


def calculate_relations_weights(freqs, rel_type):
    frequency_sum = calculate_frequency_sum(freqs, rel_type)
    weight_dict = dict()
    weight_list = list()
    name_list = list()
    value_list = list()
    for r_t in rel_type:
        name_list += freqs[r_t]
        value_list += freqs[r_t].values()
    # we sort the values accordingly the sorted name list and return two sorted tuples
    sorted_values = []
    sorted_names = []
    if len(name_list) != 0:
        #  This comprehension crashes if we give empty lists
        sorted_names, sorted_values = zip(*[(name, value) for name, value in sorted(zip(name_list, value_list))])
        sorted_names = list(sorted_names)
        sorted_values = list(sorted_values)

    for idx, out_value in enumerate(sorted_values[:-1]):
        weight_list.append(list())
        for in_value in sorted_values[idx+1:]:
            weight_list[idx].append((out_value + in_value) / frequency_sum)

    for out_idx, out_name in enumerate(sorted_names[:-1]):
            for in_idx, in_name in enumerate(sorted_names[out_idx+1:]):
                weight_dict[out_name + "**" + in_name] = weight_list[out_idx][in_idx]

    return weight_dict


def calculate_frequency_sum(freqs, r_type):
    values = list()
    for r_t in r_type:
        values += list(freqs[r_t].values())

    return sum(values)


def entity_article_frequency(ent_list):
    all_persons = dict()
    all_locations = dict()
    all_organizations = dict()
    entity_frequencies = dict()

    for sent_dict in ent_list:
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


def merge_scores(article_weights, sentence_weights):
    merged_weights = dict()
    for sent_key in article_weights:
        if sent_key in sentence_weights:
            merged_weights[sent_key] = [sentence_weights[sent_key][0] + article_weights[sent_key][0],
                                        sentence_weights[sent_key][1]]
        else:
            merged_weights[sent_key] = [article_weights[sent_key][0], article_weights[sent_key][1]]
    return merged_weights

