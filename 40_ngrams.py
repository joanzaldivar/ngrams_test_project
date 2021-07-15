import pandas as pd
import re
import nltk
import logging
import os

def sort_ngrams(ngram):
    if len(ngram) > 0:
      word_list = list(ngram)
      word_list.sort()
      return ', '.join(word_list)
    else:
      return None

#Start of Main Program
if __name__ == '__main__':    

    #Start logging
    log_file = '{}_{}.log'.format('ngrams', os.getlogin()) 
    logging.basicConfig(filename=log_file, level=logging.INFO, format='%(asctime)s %(message)s')
    logging.info('| Start ngrams...')
    print('Start ngrams...')

    #Get data from file
    data_file = '../data/test_data_english_clean.csv'
    df = pd.read_csv(data_file)
    df.dropna(subset=['PhraseCleaned'], inplace = True)

    #Get bag of words
    words = df['PhraseCleaned']
    bag_of_words = re.sub(r'[^\w\s]', '', ' '.join(words)).split()

    #Get ngrams
    trigrams_df = pd.DataFrame((pd.Series(nltk.ngrams(bag_of_words, 3)).value_counts()))
    bigrams_df = pd.DataFrame((pd.Series(nltk.ngrams(bag_of_words, 2)).value_counts()))
    word_df = pd.DataFrame((pd.Series(nltk.ngrams(bag_of_words, 1)).value_counts()))

    #Set ngrams and class columns
    trigrams_df['ngram'], bigrams_df['ngram'], word_df['ngram'] = 3, 2, 1

    #Combine dataframes
    new_df = pd.DataFrame()
    new_df = new_df.append(trigrams_df)
    new_df = new_df.append(bigrams_df)
    new_df = new_df.append(word_df)

    #Add new column with sorted ngrams
    new_df['ngram_sorted'] = new_df.index.values
    new_df['ngram_sorted'] = new_df['ngram_sorted'].apply(lambda x:sort_ngrams(x))
        
    #Export updated df to CSV
    output_fname = '../data/test_data_ngrams.csv'
    new_df['ngram_count'] = new_df[0]
    new_df.drop(columns=[0], inplace=True)
    new_df.to_csv(output_fname)
    logging.info('| Completed ngrams.')
    print('Completed ngrams.')