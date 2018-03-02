import os


def create_article_graph(art_rel_weights, path, day, week):
    date_dir = path + "Graphs/Article/" + week
    if not os.path.exists(date_dir):
        os.makedirs(date_dir)
    if not os.path.exists(date_dir + "/" + day):
        os.makedirs(date_dir + "/" + day)

    # Creating gephi node CSV file

    pass