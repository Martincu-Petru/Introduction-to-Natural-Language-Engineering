import nltk
import re

from nltk.stem import WordNetLemmatizer
from nltk.corpus import wordnet
from nltk.wsd import lesk
from nltk.corpus import wordnet as wn

nltk.download('punkt')
nltk.download('wordnet')
nltk.download('averaged_perceptron_tagger')


number_regex = re.compile(r".?([0-9]|\.).?")
is_noun = lambda pos: pos[:2] == 'NN'
lemmatizer = WordNetLemmatizer()
data = open("training_data.txt", "r").read()
tokens = nltk.word_tokenize(data, language="english")
tagged_tokens = nltk.pos_tag(tokens)


def get_noun_list():
    noun_list = []
    for item in tagged_tokens:
        if item[1] == "NNS" or item[1] == "NN":
            if not number_regex.match(item[0]):
                noun_list.append(lemmatizer.lemmatize(item[0], pos=wordnet.NOUN))

    return noun_list


def disambiguation():
    for noun in get_noun_list():
        print(lesk(data, noun, 'n'))


disambiguation()



