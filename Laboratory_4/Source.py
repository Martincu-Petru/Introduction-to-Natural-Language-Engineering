import nltk
import re
import string
import pandas
import math
import operator

from nltk.stem import WordNetLemmatizer
from nltk.corpus import wordnet

nltk.download('punkt')
nltk.download('wordnet')
nltk.download('averaged_perceptron_tagger')

lemmatizer = WordNetLemmatizer()


def get_wordnet_pos(word):
    tag = nltk.pos_tag([word])[0][1][0].upper()
    tag_dict = {"J": wordnet.ADJ,
                "N": wordnet.NOUN,
                "V": wordnet.VERB,
                "R": wordnet.ADV}

    return tag_dict.get(tag, wordnet.NOUN)


def get_pos_name(name):
    if name == "n":
        return "noun"
    elif name == "j":
        return "adjective"
    elif name == "v":
        return "verb"
    else:
        return "adverb"


def read_data(files):
    word_set = set()
    document_words = []
    number_of_files = 0

    for file in files:
        current_document_data = open(file).read().translate(str.maketrans('', '', string.punctuation))
        current_document_data = re.sub(r"\n", "", current_document_data)
        # current_document_data = current_document_data.split(" ")

        tokens = nltk.word_tokenize(current_document_data, language="english")
        tagged_tokens = nltk.pos_tag(tokens)

        current_document_data = []

        for item in tagged_tokens:
            current_document_data.append(lemmatizer.lemmatize(item[0], pos=get_wordnet_pos(item[0])))

        document_words.append(current_document_data)

        current_document_set = set(current_document_data)
        word_set = word_set.union(current_document_set)
        number_of_files = number_of_files + 1

    return word_set, document_words, number_of_files


def build_dictionaries():
    dictionaries = []

    word_set, documents_words, number_of_files = read_data(["data/document_1.txt",
                                                            "data/document_2.txt",
                                                            "data/document_3.txt",
                                                            "data/document_4.txt",
                                                            "data/document_5.txt"])

    for i in range(0, number_of_files):
        dictionaries.append(dict.fromkeys(word_set, 0))

    current_document = 0

    for document_words in documents_words:
        for word in document_words:
            dictionaries[current_document][word] = dictionaries[current_document][word] + 1

        current_document = current_document + 1

    tf_bows = []
    for i in range(0, number_of_files):
        tf_bows.append(computeTF(dictionaries[i], document_words[i]))

    idfs = computeIDF(dictionaries)

    tfidfs = []

    for i in range(0, number_of_files):
        tfidfs.append(computeTFIDF(tf_bows[i], idfs))


    print(tfidfs)

    for dictionary in tfidfs:
        sorted_d = sorted(dictionary.items(), key=operator.itemgetter(1))
        # print(sorted_d)
        cuv = sorted_d[-1][0]

        try:
            synonyms = []
            for syn in wordnet.synsets(cuv, get_wordnet_pos(cuv)):
                for l in syn.lemmas():
                    synonyms.append(l.name())

            for word in synonyms:
                if word != cuv:
                    print(cuv + " are sinonimul: " + word)
                    break

            hypers = wordnet.synset(cuv + "." + get_wordnet_pos(cuv) + "." + "01")
            hyper = hypers.hypernyms()
            hypo = hypers.hyponyms()
            # hypernims = set (hyper)
            print(cuv + " are hipernimele: ", hyper[0].lemma_names())
            print(cuv + " are hiponimele: ", hypo[0].lemma_names())
        except:
            pass




    #print(tfidfs)


def computeTF(word_dict, bow):
    tfDict = {}
    bowCount = len(bow)
    for word, count in word_dict.items():
        tfDict[word] = count/float(bowCount)
    return tfDict


def computeIDF(docList):
    idfDict = {}
    N = len(docList)

    idfDict = dict.fromkeys(docList[0].keys(), 0)
    for doc in docList:
        for word, val in doc.items():
            if val > 0:
                idfDict[word] += 1

    for word, val in idfDict.items():
        idfDict[word] = math.log10(N / float(val))

    return idfDict


def computeTFIDF(tfBow, idfs):
    tfidf = {}
    for word, val in tfBow.items():
        tfidf[word] = val*idfs[word]
    return tfidf

build_dictionaries()

'''lemmatizer = WordNetLemmatizer()
data = open("training_data.txt", "r").read()

tokens = nltk.word_tokenize(data, language="english")
tagged_tokens = nltk.pos_tag(tokens)

for item in tagged_tokens:
    print(item[0] + " -> " + lemmatizer.lemmatize(item[0], pos=get_wordnet_pos(item[0])) + ": " + get_pos_name(get_wordnet_pos(item[0])))
'''
