import os, fnmatch, random
import json
from pprint import pprint
from tqdm import tqdm

def all_keywords(path, longer_than=400, demo=False):
    # Frames to crops
    files = sorted(os.listdir(path))
    files = fnmatch.filter(files, '*.json')
    random.shuffle(files)

    print("jsons:", len(files), files[0:2], "...")

    keywords_list = {}

    if demo:
        subfiles = files[0:100]
    else:
        subfiles = files

    for i in tqdm(range(len(subfiles))):
        file = subfiles[i]
        data = json.load(open(path + file))

        text = data["body"]
        if text == '':
            continue
        if len(text) < longer_than:
            # 80 is roughly one sentence, lets say we want 3 and more
            continue

        keywords = data["features"]["content"]["keywords"]
        keywords = [key["keyword"] for key in keywords]

        for key in keywords:
            if key not in keywords_list:
                keywords_list[key] = 0
            else:
                keywords_list[key] += 1

    print("Found", len(keywords_list.keys()), "unique keywords.")
    sorted_keywords_list = sorted(keywords_list.items(), key=lambda x: -x[1])

    return sorted_keywords_list, keywords_list


def load(path, keywords_find, keywords_exclude, longer_than=400, demo=False):
    # Frames to crops
    files = sorted(os.listdir(path))
    # print("files",len(files), files[0:10])
    files = fnmatch.filter(files, '*.json')
    random.shuffle(files)

    print("jsons:", len(files), files[0:2], "...")

    key_files = []
    key_texts = []
    key_title = []

    if demo:
        subfiles = files[0:100]
    else:
        subfiles = files

    for i in tqdm(range(len(subfiles))):
        file = subfiles[i]
        data = json.load(open(path + file))
        text = data["body"]
        title = data["title"]

        # optional, limit lenght of the article - only those with len(text) > THR

        if text == '':
            continue
        if len(text) < longer_than:
            # 80 is roughly one sentence, lets say we want 3 and more
            continue

        keywords = data["features"]["content"]["keywords"]
        # pprint(keywords)
        # pprint(data)

        keywords = [key["keyword"] for key in keywords]

        contains = False

        if len(keywords_find) == 0:
            contains = True
        else:
            for key in keywords_find:
                if key in keywords:
                    contains = True
                    break

        if len(keywords_exclude) > 0:
            for key in keywords_exclude:
                if key in keywords:
                    contains = False
                    break

        if contains:
            key_files.append(file)
            key_texts.append(text)
            key_title.append(title)

            # print(keywords)

    print("Found", len(key_files), "articles with those key(s):", keywords_find)

    return key_files, key_texts, key_title


def load_from_urls(path, urls_find, longer_than=400, demo=False, debug=False):
    # Frames to crops
    files = sorted(os.listdir(path))
    # print("files",len(files), files[0:10])
    files = fnmatch.filter(files, '*.json')
    random.shuffle(files)

    print("jsons:", len(files), files[0:2], "...")

    key_files = []
    key_texts = []
    key_title = []

    if demo:
        subfiles = files[0:100]
    else:
        subfiles = files

    for i in tqdm(range(len(subfiles))):
        file = subfiles[i]
        data = json.load(open(path + file))
        text = data["body"]
        title = data["title"]
        url = data["url"]

        # optional, limit lenght of the article - only those with len(text) > THR

        if text == '':
            continue
        if len(text) < longer_than:
            # 80 is roughly one sentence, lets say we want 3 and more
            continue

        keywords = data["features"]["content"]["keywords"]
        # pprint(keywords)
        # pprint(data)

        keywords = [key["keyword"] for key in keywords]

        contains = False

        if len(urls_find) == 0:
            contains = True
        else:
            for url_find in urls_find:
                if url_find in url:
                    contains = True
                    if debug:
                        print(url)
                    break

        if contains:
            key_files.append(file)
            key_texts.append(text)
            key_title.append(title)

            # print(keywords)

    print("Found", len(key_files), "articles with those subsets of url(s):", keywords_find)

    return key_files, key_texts, key_title


def get_urls(path, demo=False):
    files = sorted(os.listdir(path))
    files = fnmatch.filter(files, '*.json')
    random.shuffle(files)

    print("jsons:", len(files), files[0:2], "...")

    if demo:
        subfiles = files[0:100]
    else:
        subfiles = files

    urls = []
    for i in tqdm(range(len(subfiles))):
        file = subfiles[i]
        data = json.load(open(path + file))
        url = data["url"]

        urls.append(url)
    urls = sorted(urls)

    # urls are in form like: http://artificialintel.blogspot.com/2004/07/
    # we could split by // and /
    return urls



def join_into_file(key_texts, key_title, file_texts, file_titles, force_cleanup=False):
    # force_cleanup has to be True with python2.7, it converts all super special unicode chars
    # it might be advantageous to keep even the special chars though
    # join texts into one string
    joined_texts = "\n".join(key_texts)
    joined_titles = "\n".join(key_title)

    print(joined_titles[0:500])

    save_to_txt_file(joined_texts, file_texts, force_cleanup)
    save_to_txt_file(joined_titles, file_titles, force_cleanup)


def save_to_txt_file(text, file, force_cleanup):
    if force_cleanup:
        # ignores any encoding errors, meaning you lose the special characters

        clean_text = text.encode('utf8').decode('ascii', 'ignore')
        with open(file, "w") as text_file:
            text_file.write(clean_text)
    else:
        with open(file, "w") as text_file:
            text_file.write(text)


