#!/usr/bin/python3

import pymongo
import pickle
import os
from datetime import date, timedelta
from collections import defaultdict
from Score_Calculation import scores
# -----------------------------------------
from NER_Tools import entity_detection, entity_cleaning


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
    article_entity_list = []

    # We will get the entities for the stored articles
    # This for loop will take a lot of time and the cursor
    # is going to timeout. So we deactivate this functionality.
    # Old version ------------------------------------------------------------
    for document in db[current_week].find({"date": today}, no_cursor_timeout=True):

        entity_dict = entity_detection.detection(document["text"])
        article_entity_list.append(entity_dict)
        # break

    # Cleaning all entities.
    article_entity_list = entity_cleaning.clean(article_entity_list)

    if not os.path.exists(project_path + "Pivot_Files/Article_Entity_Structure/" + current_week):
        os.makedirs(project_path + "Pivot_Files/Article_Entity_Structure" + current_week)

    # entity dict list must be saved for future usage (NER classifier takes time)
    save_entity_dict_list = open(project_path + "Pivot_File/Article_Entity_Structure/" + current_week + "/"
                                 + today + "_DictArticlesList.pickle", "wb")
    pickle.dump(article_entity_list, save_entity_dict_list)
    save_entity_dict_list.close()


    # There is a danger using this:
    # If we try to use (print) a key that does not exist in the
    # dictionary there will be no Key Error exception but
    # the key will be created with an empty value
    article_rel_weights = create_nested_dict()
    # getting all the article of the day
    # TODO delete it when it is not needed anymore
    # current_day_articles = db[current_week].find({"date": today}, no_cursor_timeout=True)
    # Old Version --------------------------------------------------------------
    # Initializing the entityNestedDict with
    # entities that are in the same article
    for ent_list in article_entity_list:
        article_rel_weights = scores.article_level_score(article_rel_weights, ent_list, "PERSON")
        article_rel_weights = scores.article_level_score(article_rel_weights, ent_list, "LOCATION")
        article_rel_weights = scores.article_level_score(article_rel_weights, ent_list, "ORGANIZATION")


    # # ----------------------------------------------------------
    # # New way for calculating article level weights
    # # for document, entity_list_doc in zip(current_day_articles, article_entity_dict_list):
    # #     sentences = p_sent_tokenizer.sentences_from_text(document["text"])
    # #     article_rel_weights = entityScore.article_frequency_score(article_rel_weights, sentences,
    # #                                                               "PERSON", ":PER:", entity_list_doc, document["_id"])
    # #     article_rel_weights = entityScore.article_frequency_score(article_rel_weights, sentences,
    # #                                                               "LOCATION", ":LOC:", entity_list_doc, document["_id"])
    # #     article_rel_weights = entityScore.article_frequency_score(article_rel_weights, sentences,
    # #                                                               "ORGANIZATION", ":ORG:", entity_list_doc, document["_id"])
    #
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
    current_day = date(2018, 1, 8)
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
