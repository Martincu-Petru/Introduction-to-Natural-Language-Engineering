import nltk
from nltk.stem import WordNetLemmatizer
from nltk.corpus import wordnet


nltk.download('punkt')
nltk.download('wordnet')
nltk.download('averaged_perceptron_tagger')


def get_wordnet_pos(word):
    """Map POS tag to first character lemmatize() accepts"""
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


lemmatizer = WordNetLemmatizer()
data = open("training_data.txt", "r").read()

tokens = nltk.word_tokenize(data, language="english")
tagged_tokens = nltk.pos_tag(tokens)

for item in tagged_tokens:
    # print(item[0] + " " + item[1])
    print(item[0] + " -> " + lemmatizer.lemmatize(item[0], pos=get_wordnet_pos(item[0])) + ": " + get_pos_name(get_wordnet_pos(item[0])))

# print(tagged_tokens)
