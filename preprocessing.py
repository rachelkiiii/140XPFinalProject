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


nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')
nltk.download('stopwords')

start = time.time()
df = pd.read_csv("~/Downloads/tweets_01-08-2021.csv")
#df= df.iloc[0:1000]

# Tokenize the 'review' column
df['text'] = df['text'].apply(lambda review: word_tokenize(review))

# Define stop words and punctuation characters
stop_words = set(stopwords.words('english'))
punctuation_chars = set(string.punctuation)


# Remove stop words and punctuation from tokenized reviews

df['text'] = df['text'].apply(lambda tokens: [word for word in tokens if word.isalpha() and word.lower() not in stop_words and word not in punctuation_chars and word.lower() not in {'br','\'\'','\'s', '``', 'oz', 'rt', 'https'}])



# Initialize spellchecker
spell = SpellChecker()

def process_review(tokens):
    new_sentence = []
    for word, tag in pos_tag(tokens):
        word = word.lower()
        if tag == 'RB':  # Checking if the word is an adverb
            # Perform adverb to adjective conversion
            if word.endswith('ly'):  # Check if the adverb ends with 'ly'
                new_word = word[:-2]  # Remove 'ly' and add 'e' for demonstration
                new_sentence.append(spell.correction(new_word))  # Spell check the new word
            else:
                new_sentence.append(spell.correction(word))  # Spell check the word as is
        else:
            new_sentence.append(spell.correction(word))  # Spell check non-adverbs

    # Remove None values after spell checking
    filtered_list = [value for value in new_sentence if value is not None]

    return filtered_list

# Apply the processing function to each row
df['text'] = df['text'].apply(process_review)
# Drop rows where 'Text' column has empty [] values
df = df[df['text'].apply(lambda x: x != [])]

end = time.time()

elapsed_time = end-start
print(elapsed_time)



# Specify the file path and name for the CSV file
csv_file_path = '~/Downloads/trump_preprocessed.csv'

# Save the DataFrame to a CSV file
df.to_csv(csv_file_path, index=False)
