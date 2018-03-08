import pymongo
import pickle
import os
from datetime import date, timedelta
from Score_Calculation import scores, sentence_scores
# -----------------------------------------
from NER_Tools import entity_detection, entity_cleaning
from Main_Files import graph_creation


def date_range(start_date, end_date):
    for n in range(int((end_date - start_date).days)):
        yield start_date + timedelta(n)


def split_list(big_list, num_of_sublists):
    new_list = []
    if num_of_sublists == 0 or len(big_list) == 0:
        print("parameters multiply to zero, invalid division")
    else:
        split_size = 1.0 / num_of_sublists * len(big_list)
        for i in range(num_of_sublists):
            new_list.append(big_list[int(round(i * split_size)):int(round((i + 1) * split_size))])
    return new_list


def graph_in_date_range(start_date, end_date, window_size):
    # Getting data from the mongo database
    client = pymongo.MongoClient()
    # Database name is minedNews
    db = client.minedArticles

    project_path = "/home/iraklis/PycharmProjects/newsMiningVol3/"

    number_of_days = end_date - start_date

    if number_of_days.days % window_size != 0:
        print("Number of days are not a multiple of window.")

    number_of_windows = number_of_days.days // window_size

    date_range_list = list(date_range(start_date, end_date))
    splited_dates = split_list(date_range_list, number_of_windows)

    articles_entity_list = []
    articles_id_list = []

    for window_dates in splited_dates:
        for single_date in window_dates:
            today = str(single_date.year) + "-" + str(single_date.month) \
                          + "-" + str(single_date.day)
            current_week = str(single_date.isocalendar()[1]) + "-" \
                          + str(single_date.isocalendar()[0])
            # Loading the entities day dictionary
            # The entities in the dictionary are stored with the same
            # order that the documents are saved in the database
            # and they also retrieved from it in the same order.
            load_day_dict_list = open(project_path + "Pivot_Files/Article_Entity_Structure/" + current_week
                                      + "/" + today +
                                      "_DictArticlesList.pickle", "rb")
            day_dict_list = pickle.load(load_day_dict_list)
            load_day_dict_list.close()

            # Loading documents ids
            load_doc_list = open(project_path + "Pivot_Files/Document_ids/" + current_week + "/"
                                 + today + "_doc_ids.pickle", "rb")
            day_id_list = pickle.load(load_doc_list)
            load_doc_list.close()

            articles_entity_list += day_dict_list
            articles_id_list += day_id_list

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
                                            project_path, today, current_week, "Graphs_Window")
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
                                             project_path, today, current_week, "Graphs_Window")
        # --------------------------------------
        # Creating article-sentence level graphs
        merged_rel_weights = scores.merge_scores(articles_rel_weights, sentences_rel_weights)
        # Creating gephi CSV file
        graph_creation.create_merged_graph(merged_rel_weights, art_entry_ids, rel_type,
                                           project_path, today, current_week, "Graphs_Window")
    pass



# Calling the graph_in_date_range() function
# with proper dates and window for the current
# experiment.
def moving_window_graphs(start_date, end_date, window_size):

    date_range_list = list(date_range(start_date, end_date + timedelta(days=1)))
    for pivot_start_date in date_range_list:
        pivot_end_date = pivot_start_date + timedelta(days=window_size)
        if pivot_end_date <= end_date + timedelta(days=1):
            print("Calling: graph_in_date_range(" + str(pivot_start_date) + "," +
                  str(pivot_end_date - timedelta(days=1)) + ")")
            graph_in_date_range(pivot_start_date, pivot_end_date, window_size)


if __name__ == "__main__":
    # If you want to run it for only one graph
    # s_date = last date of the window - 6
    s_date = date(2018, 1, 7)
    e_date = date(2018, 3, 6)
    window = 7
    moving_window_graphs(s_date, e_date, window)

