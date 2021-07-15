import pandas as pd
import numpy as np 
import re
import logging
import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from nltk.tag import pos_tag
from nltk.tokenize import word_tokenize

nltk.download('stopwords') #for excluding stop words
nltk.download('wordnet') #for lemmatization
nltk.download('averaged_perceptron_tagger') #for tagging
nltk.download('punkt') #for punctuations

def clean(raw, lemmatizer, stop_words = ()):

    #Remove non-alphanumeric characters
    clean = re.sub('[^a-zA-Z0-9]',' ', raw)

    #Tokenize (split the sentence into words)
    tokens = word_tokenize(clean)
    
    #pos_tag() gets the tag of each word (e.g., PRP - pronoun, NN - noun, VB - verb base form)
    cleaned_tokens = []
    for token, tag in pos_tag(tokens):
        #Lemmatize each word based on tag
        if tag.startswith("NN"):
            pos = 'n'
        elif tag.startswith('VB'):
            pos = 'v'
        else:
            pos = 'a'
        token = lemmatizer.lemmatize(token, pos)

        #Collect the clean words in a list and convert to lowercase but exclude stop words
        if len(token) > 0 and token.lower() not in stop_words:
            cleaned_tokens.append(token.lower())

    #Join words back into a clean phrase
    return ' '.join(cleaned_tokens)

#Start of Main Program
if __name__ == '__main__': 
  #Start logging
  log_file = '{}.log'.format('clean') 
  logging.basicConfig(filename=log_file, level=logging.INFO, format='%(asctime)s %(message)s')
  logging.info('| Start cleaning...')
  print('Start cleaning...')

  #Get data   
  df = pd.read_csv('../data/test_data_english.csv')

  #Get stop words
  stop_words = stopwords.words('english')

  #Create lemmatizer instance
  lemmatizer = WordNetLemmatizer()

  #Clean the answers (overwrite old values in PhraseCleaned)
  df['PhraseCleaned'] = df['Translated'].apply(lambda x: clean(x, lemmatizer, stop_words))

  #Export result to CSV
  df.to_csv('../data/test_data_english_clean.csv', index=False)
  logging.info('| Completed cleaning.')
  print('Completed cleaning.')
