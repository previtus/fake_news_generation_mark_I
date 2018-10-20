from load_functions import *

path="/media/vitek/Data/Vitek/Projects/FakeNewsWebpage/all data assembly here next maybe/EVERYTHING/ALL_till_31_8_2018/"
assert path[-1] == '/'

# will filter for articles with at least ONE word from keywords_find
# and at the same time NONE of the words from keywords_exclude
# demo=True loads only 100 articles
# force_cleanup=True eliminates special utf characters


### DATASETS:
"""
# AI
keywords_find = ['ai', 'artificial', 'machine', 'machinelearning', 'ml']
# ai = 279 x
# artificial = 136 x ???
# machine : 360 ???
# machinelearning : 4
# ml : 23
# 
# intelligence : 1424 (careful...)
# data : 3849
# database : 114
keywords_exclude = []
key_files, key_texts, key_title = load(path, keywords_find, keywords_exclude, demo=False)
file_texts = "ai_texts_"+str(len(key_files))+".txt"
file_titles = "ai_titles_"+str(len(key_files))+".txt"
join_into_file(key_texts, key_title, file_texts, file_titles, force_cleanup=False)
"""

# New functions:

urls = get_urls(path, demo=False)
print("loaded", len(urls), "urls")


for u in urls:
    print(u)

"""
# Testing with URL
urls_find = ['abcnews']
key_files, key_texts, key_title = load_from_urls(path, urls_find, demo=False)
file_texts = "urltest_texts_"+str(len(key_files))+".txt"
file_titles = "urltest_titles_"+str(len(key_files))+".txt"
join_into_file(key_texts, key_title, file_texts, file_titles, force_cleanup=False)
"""