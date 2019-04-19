import nltk, re,os
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import operator

nltk.download('vader_lexicon')
nltk.download('punkt')

sentiments = {'compound': [],
              'negative': [],
              'positive': [],
              'neutral': []}


def read():
    paragraphs = None
    try:
        for root, dirs, files in os.walk("../Training_data/the_violent_corpus", topdown=False):
            for name in files:
                paragraphs = open(os.path.join(root, name), "rb").read()
                paragraphs = re.sub(r"\\n", " ", str(paragraphs))
                sentences = nltk.sent_tokenize(str(paragraphs))
                sentimentAnalysis(sentences, os.path.join(root, name))
    except:
        pass


def sentimentAnalysis(sentences, nume):
    sid = SentimentIntensityAnalyzer()
    sentiments_statistics = {
        "negative": 0,
        "positive": 0,
        "neutral": 0,
        "compound": 0
    }

    for sentence in sentences:

        ss = sid.polarity_scores(sentence)
        overall_sentiment = max(ss.items(), key=operator.itemgetter(1))[0]
        if overall_sentiment == "neu":
            if ss["neg"] != 0 or ss["pos"] != 0:
                if ss["neg"] > 0:
                    overall_sentiment = "neg"
                else:
                    overall_sentiment = "pos"

        if overall_sentiment == "neu":
            sentiments_statistics["neutral"] += 1
        elif overall_sentiment == "compound":
            sentiments_statistics["compound"] += 1
        elif overall_sentiment == "neg":
            sentiments_statistics["negative"] += 1
        elif overall_sentiment == "pos":
            sentiments_statistics["positive"] += 1

    print("Nume: " + nume)
    print(sentiments_statistics)


if __name__ == '__main__':
    read()
