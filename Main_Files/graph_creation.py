import os
from Score_Calculation import scores


def assign_ids(art_ent_list, rel_type):
    index_dict = dict()
    entry_id = 0
    for ent_list in art_ent_list:
        frequencies = scores.entity_article_frequency(ent_list)
        for r_t in rel_type:
            for ent_key in frequencies[r_t]:
                if ent_key not in index_dict:
                    index_dict[ent_key] = entry_id
                    entry_id += 1
    return index_dict


def create_article_graph(art_rel_weights, ids, r_type, path, day, week):
    date_dir = path + "Graphs/Article/" + week
    if not os.path.exists(date_dir):
        os.makedirs(date_dir)
    if not os.path.exists(date_dir + "/" + day):
        os.makedirs(date_dir + "/" + day)

    # Creating gephi node CSV file
    with open(date_dir + '/' + day + '/politicsNodes' + r_type + '.csv', 'w') as node_file:
        node_file.write('id,label\n')
        for i_d in ids:
            node_file.write(str(ids[i_d]) + "," + i_d + "\n")

    # Creating gephi edge CSV file
    with open(date_dir + '/' + day + '/politicsEdges' + r_type + '.csv', 'w') as edge_file:
        edge_file.write('Source,Target,Weight,sentence_appearance\n')
        for rel_weight in art_rel_weights:
            splited_pair = rel_weight.split("**")
            edge_file.write(str(ids[splited_pair[0]]) + ","
                            + str(ids[splited_pair[1]]) + ","
                            + str(art_rel_weights[rel_weight][0]) + ","
                            + "\"" + str(art_rel_weights[rel_weight][1]) + "\"\n")
