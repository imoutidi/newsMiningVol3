#!/usr/bin/python3
import pymongo
import pickle
import os
from datetime import date, timedelta
from collections import defaultdict
from Score_Calculation import scores, sentence_scores
# -----------------------------------------
from NER_Tools import entity_detection, entity_cleaning
from Main_Files import graph_creation


# Better than lambda
def create_nested_dict():
    return defaultdict(create_nested_dict)


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
        # if count == 1:
        #     break
        # count += 1

    # Cleaning all entities.
    articles_entity_list = entity_cleaning.clean(articles_entity_list)

    if not os.path.exists(project_path + "Pivot_Files/Article_Entity_Structure/" + current_week):
        os.makedirs(project_path + "Pivot_Files/Article_Entity_Structure/" + current_week)

    # entity dict list must be saved for future usage (NER classifier takes time)
    save_entity_dict_list = open(project_path + "Pivot_Files/Article_Entity_Structure/" + current_week + "/"
                                 + today + "_DictArticlesList.pickle", "wb")
    pickle.dump(articles_entity_list, save_entity_dict_list)
    save_entity_dict_list.close()

    relation_types = ["PLO", "PL", "PO", "LO", "P", "L", "O"]

    # Creating article level graphs
    for rel_type in relation_types:
        articles_rel_weights = dict()

        entry_ids = graph_creation.assign_ids(articles_entity_list, rel_type)

        # Calculating the weight for all entities for all articles
        for ent_list, article_id in zip(articles_entity_list, articles_id_list):
            articles_rel_weights = scores.article_level_score(articles_rel_weights, ent_list, rel_type, article_id)
        # Creating gephi CSV files
        graph_creation.create_graph(articles_rel_weights, entry_ids, rel_type,
                                    project_path, today, current_week, "Article")

    # Creating sentence level graphs
    for rel_type in relation_types:
        sentences_rel_weights = dict()

        # Calculating the weight for all entities for all sentences of all articles
        for ent_list, article_id in zip(articles_entity_list, articles_id_list):
            sentences_rel_weights = sentence_scores.sentence_level_score(sentences_rel_weights, ent_list,
                                                                         rel_type, article_id)
        entry_ids = graph_creation.assign_sentence_ids(sentences_rel_weights)

        # Creting gephi CSV file
        graph_creation.create_graph(sentences_rel_weights, entry_ids, rel_type,
                                    project_path, today, current_week, "Sentence")

    # Creating article-sentence level graphs
    # for rel_type in relation_types:





    # # In this dictionary we will keep the score regarding
    # # the occurrences of two entities in a sentence and also
    # # the document ID and the index number of the sentence that
    # # this occurrence happened.
    # # A score of 2 is accumulated for each pair only once per
    # # document so if two entities appear more than one sentence
    # # in the same document only a score of 2 will be added.
    # sentence_rel_weights = create_nested_dict()
    # # current_day_articles = db[current_week].find({"date": today}, no_cursor_timeout=True)
    # # Calculating the scores
    # for document, entity_list_doc in zip(current_day_articles, article_entity_dict_list):
    #     sentences = p_sent_tokenizer.sentences_from_text(document["text"])
    #     sentence_rel_weights = entityScore.sent_level_score(sentence_rel_weights, sentences,
    #                                                         entity_list_doc, document["_id"])
    #
    # total_rel_weights = create_nested_dict()
    # entityScore.final_score_of_entity_pairs(article_rel_weights,
    #                                         sentence_rel_weights, total_rel_weights)
    #
    # # Creating the Gephi files P stands for Person, L for Location and O for Organization
    # # so we can change what kind of nodes we can have in our graph.
    # types = ["PLO", "PL", "PO", "LO", "P", "L", "O"]
    # for tp in types:
    #     entityTools.createGraphFiles(total_rel_weights, tp, "Graphs/Article_Sentence",
    #                                  sentence_rel_weights, current_week, today)
    #     entityTools.createGraphFiles(article_rel_weights, tp, "Graphs/Article",
    #                                  sentence_rel_weights, current_week, today)
    #     entityTools.createSentGraphFiles(sentence_rel_weights, tp, "Graphs/Sentence",
    #                                      current_week, today)
    #
    # n_date = date.today()
    # s_date = n_date - timedelta(6)
    # window = 7
    # graph_window.moving_window_graphs(s_date, n_date, window)


if __name__ == "__main__":
    current_day = date(2018, 1, 9)
    current_date = str(current_day.year) + "-" + str(current_day.month) + "-" + \
                   str(current_day.day)
    current_week = str(current_day.isocalendar()[1]) + "-" + str(current_day.isocalendar()[0])
    while current_day != date(2018, 2, 19):
        current_date = str(current_day.year) + "-" + str(current_day.month) + "-" + \
                       str(current_day.day)
        current_week = str(current_day.isocalendar()[1]) + "-" + str(current_day.isocalendar()[0])
        print("Working on " + current_date)
        detect_relate_graph_entities(current_date, current_week)
        current_day += timedelta(1)
        break
