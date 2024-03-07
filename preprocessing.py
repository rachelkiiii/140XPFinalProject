import numpy as np
import nltk
import pandas as pd

from nltk.tag import pos_tag
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.linear_model import LogisticRegression
from spellchecker import SpellChecker
import string
import time
from nltk.corpus import words


nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')
nltk.download('stopwords')
nltk.download('words')

start = time.time()
df = pd.read_csv("~/Downloads/tweets_01-08-2021.csv")

# Convert the 'date' column to datetime format
df['date'] = pd.to_datetime(df['date'])

# Define the conditions for each time block
conditions = [
    (df['date'] > "2015-06-14") & (df['date'] < "2016-07-19"),
    (df['date'] > "2016-07-18") & (df['date'] < "2016-11-08"),
    (df['date'] > "2016-11-07") & (df['date'] < "2016-11-09"),
    (df['date'] > "2016-11-08") & (df['date'] < "2017-01-21"),
    (df['date'] > "2020-08-23") & (df['date'] < "2020-11-03"),
    (df['date'] > "2020-11-02") & (df['date'] < "2020-11-04"),
    (df['date'] > "2020-11-03")
]

# Define the values for each time block
values = ['Trump_primary_2016', 'Trump_elec_2016', 'Trump_elecday_2016', 'Trump_post_2016',
          'Trump_elec_2020', 'Trump_elecday_2020', 'Trump_post_2020']

# Add a new column 'time_block' based on the conditions and values
df['time_block'] = np.select(conditions, values, default='Other')
df = df[df['time_block'] != 'Other']

# Tokenize the 'review' column
df['text'] = df['text'].apply(lambda review: word_tokenize(review))

# Define stop words and punctuation characters
stop_words = set(stopwords.words('english'))
punctuation_chars = set(string.punctuation)


# Remove stop words and punctuation from tokenized reviews

df['text'] = df['text'].apply(lambda tokens: [word for word in tokens if word.isalpha() and word.lower() not in stop_words and word not in punctuation_chars and word.lower() not in {'br','\'\'','\'s', '``', 'oz', 'rt', 'https'}])


english_words = set(words.words())

# Filter out non-English words
df['text'] = df['text'].apply(lambda tokens: [word for word in tokens if word in english_words])

'''
spell = SpellChecker()

# Spell check and convert to lowercase
def spell_check_and_lower(tokens):
    corrected_tokens = [spell.correction(word.lower()) for word in tokens]
    return corrected_tokens

# Apply spell check and lowercase conversion to 'text' column
df['text'] = df['text'].apply(spell_check_and_lower)
'''

df['text'] = df['text'].apply(lambda tokens: [word.lower() for word in tokens])

# Drop rows where 'Text' column has empty [] values
df = df[df['text'].apply(lambda x: x != [])]

end = time.time()

elapsed_time = end-start
print(elapsed_time)



# Specify the file path and name for the CSV file
csv_file_path = '~/Downloads/trump_preprocessed.csv'

# Save the DataFrame to a CSV file
df.to_csv(csv_file_path, index=False)
