from nltk.tag.stanford import StanfordNERTagger
from nltk.tokenize import word_tokenize

import os
import re

java_path = "C:\\Program Files\\Java\\jdk-11.0.2\\bin\\java.exe"
os.environ['JAVAHOME'] = java_path


def formatted_entities(classified_paragraphs_list):
    entities = {'persons': list(),
                'organizations': list(),
                'locations': list(), 'times': list(),
                'tokens_with_punctuation': list(),
                'tokens_without_punctuation': list(),
                'number_of_sentences': list()
                }

    entities['tokens_with_punctuation'].append(len(classified_paragraphs_list[0]))

    tokens_without_punctuation = 0
    number_of_sentences = 0

    for item in classified_paragraphs_list[0]:
        if re.match("\.", item[0]):
            number_of_sentences = number_of_sentences + 1
        if re.match("\W", item[0]):
            tokens_without_punctuation = tokens_without_punctuation + 1

    entities['tokens_without_punctuation'].append(len(classified_paragraphs_list[0]) - tokens_without_punctuation)
    entities['number_of_sentences'].append(number_of_sentences)

    for classified_paragraph in classified_paragraphs_list:
        for entry in classified_paragraph:
            entry_value = entry[0]
            entry_type = entry[1]

            if entry_type == 'PERSON':
                entities['persons'].append(entry_value)

            elif entry_type == 'ORGANIZATION':
                entities['organizations'].append(entry_value)

            elif entry_type == 'LOCATION':
                entities['locations'].append(entry_value)

            elif entry_type == 'TIME':
                entities['times'].append(entry_value)

    return entities


tagger = StanfordNERTagger('stanford-ner-2018-10-16\\classifiers\\english.muc.7class.distsim.crf.ser.gz',
                           'stanford-ner-2018-10-16\\stanford-ner.jar',
                           encoding='utf-8')

tokenized_paragraphs = list()

paragraphs = [open("training_data.txt", "r").read()]

for text in paragraphs:
    tokenized_paragraphs.append(word_tokenize(text))

classified_paragraphs_list = tagger.tag_sents(tokenized_paragraphs)

formatted_result = formatted_entities(classified_paragraphs_list)
print(formatted_result)
