from datetime import *

months = ["unk","jan","feb","mar","apr","may","jun","jul","aug","sep","oct","nov","dec"]
month = (months[datetime.now().month])
day = str(datetime.now().day)

import argparse

parser = argparse.ArgumentParser(description='Analyze generated text dataset with the original input text.')
parser.add_argument('-input', help='path to the original input text (input.txt).',
                    default="input.txt")
parser.add_argument('-generated', help='path to the generated text.',
                    default="gnerated.txt")
parser.add_argument('-outputname', help='Output file name', default='Test-'+day+month+'.txt')

# do once:
#import nltk
#nltk.download('punkt')

import numpy as np
from tqdm import tqdm
from fuzzywuzzy import fuzz
import os
import re, string
import matplotlib

if not('DISPLAY' in os.environ):
    matplotlib.use("Agg")

import matplotlib.pyplot as plt


import nltk.data
tokenizer = nltk.data.load('tokenizers/punkt/english.pickle')

def string_to_sentences(paragraph):
    return tokenizer.tokenize(paragraph)
    # 106 481 sentences

def string_to_words(s):
    return [re.sub('^[{0}]+|[{0}]+$'.format(string.punctuation), '', w) for w in s.split()]


def ls(path):
    ls = [f for f in os.listdir(path)]
    print(ls)
    return ls


def cd(path):
    os.chdir(path)
    cwd = os.getcwd()
    print("In directory:", cwd)


if __name__ == '__main__':
    args = parser.parse_args()

    FAST_DEMO = False

    # GENERATED

    file = args.generated
    with open(file) as f:
        content = f.readlines()
    # you may also want to remove whitespace characters like `\n` at the end of each line
    content = [x.strip() for x in content]
    content = "\n".join(content)

    #content = content.decode('utf-8')

    print("Generated", len(content), "letters....")
    print(content[0:500])

    # ORIGINAL INPUT

    whole_text_path = args.input
    with open(whole_text_path, 'r') as content_file:
        whole_text = content_file.read()

    print("Loaded input", len(whole_text), "chars", whole_text[0:50])

    if FAST_DEMO:
        whole_text = whole_text[0:1000]

    # whole_text = whole_text.decode('utf-8')

    full_word_list = string_to_words(whole_text)
    full_sentence_list = string_to_sentences(whole_text)
    # unique_words = list(set(word_list))
    print(len(full_word_list), "words in input")
    print(len(full_sentence_list), "sentences in input")
    # print(len(unique_words),"unique", unique_words[0:100])

    print("Showing a random sample from the input set:")
    idx = np.random.randint(1, len(full_sentence_list), size=3)
    for i in idx:
        print(full_sentence_list[i])
        print("===")

    print("Working with file", file, "now...")
    sample_paragraph = content

    sample_sentences = string_to_sentences(sample_paragraph)
    print("parsed generated text as", len(sample_sentences), " sentences.")

    if FAST_DEMO:
        sample_sentences = sample_sentences[100:200]

    closest_sentences = {}

    similarities = []

    with open(args.outputname, 'w') as f:

        i = 0
        # for sentence in tqdm(sample_sentences):
        for sentence in sample_sentences:
            print(i,"/",len(sample_sentences))

            closest_sentences[i] = []

            max_so_far = -1.0
            closest_sentence = ""

            for close_sentence in full_sentence_list:
                r = float(fuzz.ratio(sentence, close_sentence)) / 100.0
                # SUPER SLOW >> r = (difflib.SequenceMatcher(None, sentence, close_sentence).ratio())
                if r >= max_so_far:
                    max_so_far = r
                    closest_sentence = close_sentence

                    closest_sentences[i].append([r, closest_sentence])
            similarities.append(max_so_far)

            ###
            """
            if max_so_far > 0.8:
                print(i)
                print("Generated sentence ",i," \"", sentence, "\" has closest:")
                print(max_so_far,":",closest_sentence)
                print("-----------------")
            """
            if max_so_far < 0.7:
                # print "good enough" sentences
                print(sentence)
                f.write(sentence)

            # for close in closest_sentences[i]:
            #    print(close[0],":", close[1])

            i = i + 1


    fig = plt.figure()
    plt.plot(similarities)
    plt.ylim(0.0, 1.0)
    plt.title("Levenstein distance to nearest sentence in the real dataset.")
    # Two layer model with 256 neurons, beam search width 16
    plt.xlabel("Default model and sampling.")
    #plt.show()
    fig.savefig(args.outputname+"last_distances.pdf", bbox_inches='tight')

    f.close()

    ### What are the best generated sentences?

    tmp_scores = []
    tmp_sentences = []
    tmp_close_sentences = []
    for i, sentence in enumerate(sample_sentences):

        max_so_far = -1.0
        maximum_sentence = ""
        # print("Sentence ",i," \"", sentence, "\" has closest:")
        for close in closest_sentences[i]:
            # print(close[0],":", close[1])
            if close[0] > max_so_far:
                max_so_far = close[0]
                maximum_sentence = sentence
                closest_sentence = close[1]

        tmp_scores.append(max_so_far)
        tmp_sentences.append(maximum_sentence)
        tmp_close_sentences.append(closest_sentence)
        # print("-----------------")

    sort_order = np.argsort(tmp_scores)
    tmp_scores = [tmp_scores[i] for i in sort_order]
    tmp_sentences = [tmp_sentences[i] for i in sort_order]
    tmp_close_sentences = [tmp_close_sentences[i] for i in sort_order]

    print("Most innovative sentences are: (sorted)")
    for i in range(len(tmp_scores)):
        print(tmp_scores[i], ":", tmp_sentences[i])
        print("~~~", tmp_close_sentences[i])
        print("")
