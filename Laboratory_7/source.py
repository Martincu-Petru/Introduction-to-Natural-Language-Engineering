import nltk, re,os
from nltk.sentiment.vader import SentimentIntensityAnalyzer

nltk.download('vader_lexicon')
nltk.download('punkt')

sentiments = {'compound': list(),
              'negative': list(),
              'positive': list(),
              'neutral': list()}
def read():
    paragraphs = None
    try:
        for root, dirs, files in os.walk("./the_violent_corpus", topdown=False):
            for name in files:
                paragraphs = open(os.path.join(root, name), "rb").read()
                # print(os.path.join(root, name))
                paragraphs = re.sub(r"\\n", " ", str(paragraphs))
                sentences = nltk.sent_tokenize(str(paragraphs))
                sentimentAnalysis(sentences, os.path.join(root, name))
    except:
        pass


def sentimentAnalysis(sentences, nume):
    sid = SentimentIntensityAnalyzer()
    dictionar = dict()
    dictionar["neutru"] = 0
    dictionar["pozitiv"] = 0
    dictionar["negativ"] = 0

    for sentence in sentences:

        ss = sid.polarity_scores(sentence)
        for k in sorted(ss):
            # print('{0}: {1}, '.format(k, ss[k]), end='')
            # print()
            if k == 'compound':
                sentiments['compound'].append(sentence)
            elif k == 'neg':
                sentiments['negative'].append(sentence)
                dictionar["negativ"] += 1
            elif k == 'neu':
                sentiments['neutral'].append(sentence)
                dictionar["neutru"] += 1
            elif k == 'pos':
                sentiments['positive'].append(sentence)
                dictionar["pozitiv"] += 1
    print("Nume: " + nume)
    print(dictionar)


read()
