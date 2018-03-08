#!/usr/bin/python3
import pymongo
import pickle
import os
from datetime import date, timedelta
from Score_Calculation import scores, sentence_scores
# -----------------------------------------
from NER_Tools import entity_detection, entity_cleaning
from Main_Files import graph_creation


def detect_relate_graph_entities(today, current_week):
    # Getting data from the mongo database
    client = pymongo.MongoClient()
    # Database name is minedNews
    db = client.minedArticles
    project_path = "/home/iraklis/PycharmProjects/newsMiningVol3/"

    # List of dictionaries with the entities of all
    # the articles. Each dictionary has 3 keys:
    # PERSON, LOCATION and ORGANIZATION the value
    # for each key is a list with all the detected
    # entities. (It is uncommented to be easier seen
    # below it is being reinitialized.
    articles_entity_list = list()
    articles_id_list = list()

    # We will get the entities for the stored articles
    # This for loop will take a lot of time and the cursor
    # is going to timeout. So we deactivate this functionality.
    # Old version ------------------------------------------------------------
    count = 0
    for document in db[current_week].find({"date": today}, no_cursor_timeout=True):
        entity_dict = entity_detection.detection(document["text"])
        articles_entity_list.append(entity_dict)
        articles_id_list.append(document["_id"])
        # if count == 2:
        #     break
        # count += 1

    # Cleaning all entities.
    articles_entity_list = entity_cleaning.clean(articles_entity_list)

    if not os.path.exists(project_path + "Pivot_Files/Article_Entity_Structure/" + current_week):
        os.makedirs(project_path + "Pivot_Files/Article_Entity_Structure/" + current_week)

    if not os.path.exists(project_path + "Pivot_Files/Document_ids/" + current_week):
        os.makedirs(project_path + "Pivot_Files/Document_ids/" + current_week)

    # entity dict list must be saved for future usage (NER classifier takes time)
    save_entity_dict_list = open(project_path + "Pivot_Files/Article_Entity_Structure/" + current_week + "/"
                                 + today + "_DictArticlesList.pickle", "wb")
    pickle.dump(articles_entity_list, save_entity_dict_list)
    save_entity_dict_list.close()

    # saving the document id list
    save_doc_list = open(project_path + "Pivot_Files/Document_ids/" + current_week + "/"
                         + today + "_doc_ids.pickle", "wb")
    pickle.dump(articles_id_list, save_doc_list)
    save_doc_list.close()

    relation_types = ["PLO", "PL", "PO", "LO", "P", "L", "O"]

    for rel_type in relation_types:
        # Creating article level graphs
        articles_rel_weights = dict()

        art_entry_ids = graph_creation.assign_ids(articles_entity_list, rel_type)

        # Calculating the weight for all entities for all articles
        for ent_list, article_id in zip(articles_entity_list, articles_id_list):
            articles_rel_weights = scores.article_level_score(articles_rel_weights, ent_list, rel_type, article_id)
        # Creating gephi CSV files
        graph_creation.create_article_graph(articles_rel_weights, art_entry_ids, rel_type,
                                            project_path, today, current_week, "Graphs")
        # ------------------------------
        # Creating sentence level graphs
        sentences_rel_weights = dict()

        # Calculating the weight for all entities for all sentences of all articles
        # In this dictionary we will keep the score regarding
        # the occurrences of two entities in a sentence and also
        # the document ID and the index number of the sentence that
        # this occurrence happened.
        # The score will be accumulated for each pair.
        for ent_list, article_id in zip(articles_entity_list, articles_id_list):
            sentences_rel_weights = sentence_scores.sentence_level_score(sentences_rel_weights, ent_list,
                                                                         rel_type, article_id)
        sent_entry_ids = graph_creation.assign_sentence_ids(sentences_rel_weights)

        # Creting gephi CSV file
        graph_creation.create_sentence_graph(sentences_rel_weights, sent_entry_ids, rel_type,
                                             project_path, today, current_week, "Graphs")
        # --------------------------------------
        # Creating article-sentence level graphs
        merged_rel_weights = scores.merge_scores(articles_rel_weights, sentences_rel_weights)
        # Creating gephi CSV file
        graph_creation.create_merged_graph(merged_rel_weights, art_entry_ids, rel_type,
                                           project_path, today, current_week, "Graphs")

    # n_date = date.today()
    # s_date = n_date - timedelta(6)
    # window = 7
    # graph_window.moving_window_graphs(s_date, n_date, window)


if __name__ == "__main__":
    current_day = date(2018, 1, 13)
    current_date = str(current_day.year) + "-" + str(current_day.month) + "-" + \
                   str(current_day.day)
    current_week = str(current_day.isocalendar()[1]) + "-" + str(current_day.isocalendar()[0])
    while current_day != date(2018, 1, 15):
        current_date = str(current_day.year) + "-" + str(current_day.month) + "-" + \
                       str(current_day.day)
        current_week = str(current_day.isocalendar()[1]) + "-" + str(current_day.isocalendar()[0])
        print("Working on " + current_date)
        detect_relate_graph_entities(current_date, current_week)
        current_day += timedelta(1)
        # break
