from load_functions import *

path="/.../ALL_till_31_8_2018/" # folder with downloaded .json files
assert path[-1] == '/'

# will filter for articles with at least ONE word from keywords_find
# and at the same time NONE of the words from keywords_exclude
# demo=True loads only 100 articles
# force_cleanup=True eliminates special utf characters

### DATASETS:

# Example dataset
keywords_find = ['selected', 'keywords']
keywords_exclude = []
key_files, key_texts, key_title = load(path, keywords_find, keywords_exclude, demo=False)
file_texts = "example_texts_"+str(len(key_files))+".txt"
file_titles = "example_titles_"+str(len(key_files))+".txt"
join_into_file(key_texts, key_title, file_texts, file_titles, force_cleanup=False)


