from Score_Calculation import scores


def sentence_level_score(all_articles_rel_weights, entity_list, r_type, art_id):
    frequencies = scores.entity_article_frequency(entity_list)
    sentence_rel_weights = calculate_sent_relations_weights(entity_list, frequencies, r_type)

    return 0


def calculate_sent_relations_weights(ent_list, freqs, rel_type):
    frequency_sum = scores.calculate_frequency_sum(freqs, rel_type)
    weight_dict = dict()
    name_list = list()
    for r_t in rel_type:
        name_list += freqs[r_t]
    sorted_names = sorted(name_list)
    for idx, out_name in enumerate(sorted_names[:-1]):
        for in_name in sorted_names[idx + 1:]:
            weight_dict[out_name + "**" + in_name] = [0, []]

    for idx, sent in enumerate(ent_list):
        sent_ent_list = list()
        for r_t in rel_type:
            for ent in sent[r_t]:
                sent_ent_list.append((ent, freqs[r_t][ent]))
        if len(sent_ent_list) > 1:
            #  TODO Calculate sentence weight and add it in weight dict

            pass





    print("i")
