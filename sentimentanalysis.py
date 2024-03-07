import pandas as pd
import numpy as np
from textblob import TextBlob
import matplotlib.pyplot as plt

twt = pd.read_csv("~/Downloads/trump_preprocessed.csv")

# Assuming 'text' is the column containing the tweet text
# Calculate sentiment scores for each tweet
twt['sentiment'] = twt['text'].apply(lambda x: TextBlob(str(x)).sentiment)

# Classify sentiment for each tweet
def classify_sentiment(sentiment):
    if sentiment <= -0.5:
        return 'fear'
    elif sentiment > -0.5 and sentiment <= -0.1:
        return 'frustration'
    elif sentiment > -0.1 and sentiment <= 0.1:
        return 'neutral'
    elif sentiment > 0.1 and sentiment <= 0.5:
        return 'contentment'
    else:
        return 'anger'

twt['sentiment_class'] = twt['sentiment'].apply(lambda x: classify_sentiment(x.polarity))


# Specify the file path and name for the CSV file
csv_file_path = '~/Downloads/twt.csv'
