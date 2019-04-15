import nltk, re
from nltk.sentiment.vader import SentimentIntensityAnalyzer

nltk.download('vader_lexicon')
nltk.download('punkt')

sentiments = {'compound': list(),
              'negative': list(),
              'positive': list(),
              'neutral': list()}

paragraphs = [open("training_data.txt", "r").read()]
paragraphs = re.sub(r"\\n", " ", str(paragraphs))
sentences = nltk.sent_tokenize(str(paragraphs))

sid = SentimentIntensityAnalyzer()

for sentence in sentences:
    print()
    print(sentence)
    ss = sid.polarity_scores(sentence)
    for k in sorted(ss):
        print('{0}: {1}, '.format(k, ss[k]), end='')
        print()
        if k == 'compound':
            sentiments['compound'].append(sentence)
        elif k == 'neg':
            sentiments['negative'].append(sentence)
        elif k == 'neu':
            sentiments['neutral'].append(sentence)
        elif k == 'pos':
            sentiments['positive'].append(sentence)
