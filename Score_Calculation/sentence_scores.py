from Score_Calculation import scores


def sentence_level_score(all_articles_rel_weights, entity_list, r_type, art_id):
    frequencies = scores.entity_article_frequency(entity_list)
    sentence_rel_weights = calculate_sent_relations_weights(entity_list, frequencies, r_type)
    for entity_couple in sentence_rel_weights:
        if entity_couple in all_articles_rel_weights:
            all_articles_rel_weights[entity_couple][0] += sentence_rel_weights[entity_couple][0]
            all_articles_rel_weights[entity_couple][1][art_id] = sentence_rel_weights[entity_couple][1]
        else:
            all_articles_rel_weights[entity_couple] = [sentence_rel_weights[entity_couple][0],
                                                       {art_id: sentence_rel_weights[entity_couple][1]}]

    return all_articles_rel_weights


def calculate_sent_relations_weights(ent_list, freqs, rel_type):
    frequency_sum = scores.calculate_frequency_sum(freqs, rel_type)
    weight_dict = dict()

    for idx, sent in enumerate(ent_list):
        sent_ent_list = list()
        for r_t in rel_type:
            for ent in sent[r_t]:
                sent_ent_list.append((ent, freqs[r_t][ent]))
        if len(sent_ent_list) > 1:
            # Calculating sentence weight and add it in weight dict
            sent_ent_list = sorted(list(set(sent_ent_list)))  # I am using set to delete duplicates
            for in_idx, out_name in enumerate(sent_ent_list[:-1]):
                for in_name in sent_ent_list[in_idx + 1:]:
                    if out_name[0] + "**" + in_name[0] not in weight_dict:
                        weight_dict[out_name[0] + "**" + in_name[0]] = [(out_name[1] + in_name[1]) / frequency_sum,
                                                                        [idx]]
                    else:
                        weight_dict[out_name[0] + "**" + in_name[0]][0] += (out_name[1] + in_name[1]) / frequency_sum
                        weight_dict[out_name[0] + "**" + in_name[0]][1].append(idx)
    return weight_dict

