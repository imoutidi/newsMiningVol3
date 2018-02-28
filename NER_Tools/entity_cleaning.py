import pickle
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize


# Person entities that consist of only one word
# are being deleted to reduce ambiguity
def remove_single_named_persons(name_list):
    new_name_list = []
    for entity in name_list:
        if len(entity.strip().split(" ")) > 1:
            new_name_list.append(entity)
    return new_name_list


# Using the annotations dictionary to further
# remove/clean entities.
def second_phase_name_cleaning(name_list, clean_dict):
    new_name_list = []
    for entity in name_list:
        if entity in clean_dict:
            new_name_list.append(clean_dict[entity])
        else:
            new_name_list.append(entity)
    return new_name_list


# Removing stop words from each string of the given list
def remove_stop_words(list_of_strings):
    stop_words = set(stopwords.words("english"))
    for idx, entity in enumerate(list_of_strings):
        words = word_tokenize(entity)
        filtered_sentence = []
        for w in words:
            if w not in stop_words:
                filtered_sentence.append(w)
        string_entity = ""
        for w in filtered_sentence:
            string_entity += w + " "
        string_entity = string_entity[:-1]
        list_of_strings[idx] = string_entity


def person_cleaning(ent_list, clean_persons):
    ent_list = remove_single_named_persons(ent_list)
    # clean name dictionary
    ent_list = second_phase_name_cleaning(ent_list, clean_persons)
    remove_stop_words(ent_list)

    return ent_list


def clean(article_dict):
    project_path = "/home/iraklis/PycharmProjects/newsMiningVol3/"
    load_clean_persons = open(project_path + "Pivot_Files/Clean_Entity_Dictionaries/clean_persons_dict.pickle", "rb")
    clean_persons_dict = pickle.load(load_clean_persons)
    load_clean_persons.close()

    load_clean_locs = open(project_path + "Pivot_Files/Clean_Entity_Dictionaries/clean_loc_dict.pickle", "rb")
    clean_locs = pickle.load(load_clean_locs)
    load_clean_locs.close()

    load_clean_orgs = open(project_path + "Pivot_Files/Clean_Entity_Dictionaries/clean_org_dict.pickle", "rb")
    clean_orgs = pickle.load(load_clean_orgs)
    load_clean_orgs.close()

    article_dict["PERSON"] = person_cleaning(article_dict["PERSON"], clean_persons_dict)
    article_dict["LOCATION"] = second_phase_name_cleaning(article_dict["LOCATION"], clean_locs)
    article_dict["ORGANIZATION"] = second_phase_name_cleaning(article_dict["ORGANIZATION"], clean_orgs)

    return article_dict
