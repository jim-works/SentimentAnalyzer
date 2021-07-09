import nltk.sentiment.vader as vader
import json


def score(text):
    return vader.SentimentIntensityAnalyzer().polarity_scores(text)


def filter(text, force_lower=False, common_words=[], profane_words=[]):
    if force_lower:
        text = text.lower()
    common_words.extend(profane_words)
    for ex in common_words:
        if force_lower:
            ex = ex.lower()
        text = text.replace(ex, '')
    return text

# returns -1 for negative sentiment, 0 for neutral, 1 for positive
# adds text to result_dict: 'neg', 'neu', 'pos'


def categorize(text, result_dict, neutral_threshold=0.3):
    val = score(text)['compound']
    if val < -neutral_threshold:
        if result_dict['neg'] == None:
            result_dict['neg'] = []
        result_dict['neg'].append(text)
        return -1
    if val < neutral_threshold:
        if result_dict['neu'] == None:
            result_dict['neu'] = []
        result_dict['neu'].append(text)
        return 0
    if result_dict['pos'] == None:
        result_dict['pos'] = []
    result_dict['pos'].append(text)
    return 1
