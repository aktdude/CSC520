import numpy as np
import pandas as pd
import string
import re
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import WhitespaceTokenizer
nltk.download('stopwords')

#List of stopwords
stopwords = nltk.corpus.stopwords.words('english')

def main():
    filename = "SMSSpamCollection" # name of the file to be read
    messages = [] # empty list to store the lines
    actual_value = [] # empty list to store the first words of each line


    with open(filename, "r") as file:
        for line in file:
            words = line.strip().split() # split the line into words
            first_word = words[0] # extract the spam or ham value

            remaining = " ".join(words[1:]) # join the remaining words after the first word

            actual_value.append(first_word)
            messages.append(remaining)

    ## Convert to pandas dataframe
    df = pd.DataFrame({
    "Label": actual_value,
    "Message": messages
    })

    ## Preprocessing
    #Lowercase
    df['Message'] = df['Message'].apply(lambda x: x.lower())
    #Punctuation Removal
    df['Message']= df['Message'].apply(lambda x:remove_punctuation(x))
    #Replace WWW
    df['Message']= df['Message'].apply(lambda x:replace_www(x))
    #Replace URLs
    df['Message']= df['Message'].apply(lambda x:replace_urls(x))
    # Break into tokens
    df['Tokens']= df['Message'].apply(lambda x: tokenization(x))
    #Remove stop words
    df['Tokens']= df['Tokens'].apply(lambda x:remove_stopwords(x))

    # Randomize and split into a 75/25 train test split
    shuffled_df = df.sample(frac=1)
    train_df = shuffled_df.iloc[:4181]
    train_rows, train_cols = train_df.shape
    test_df = shuffled_df.iloc[4181:]

    # Get spam and ham training data
    train_df_spam = train_df[train_df['Label'] == 'spam']
    train_s_rows, train_s_cols = train_df_spam.shape
    train_df_ham = train_df[train_df['Label'] == 'ham']
    train_h_rows, train_h_cols = train_df_ham.shape

    #Get percent of spam and ham based on the training data
    spam_percent = train_s_rows/train_rows
    ham_percent = train_h_rows/train_rows

    ## Add words to dictionaries for spam and ham
    spam_dictionary = {}
    ham_dictionary = {}
    # iterate through each row in the spam tokens
    for row in train_df_spam['Tokens']:
        # iterate through each token in the list
        for token in row:
            # update the word count dictionary
            if token in spam_dictionary:
                spam_dictionary[token] += 1
            else:
                spam_dictionary[token] = 1
    # iterate through each row in the column
    for row in train_df_ham['Tokens']:
        # iterate through each token in the list
        for token in row:
            # update the word count dictionary
            if token in ham_dictionary:
                ham_dictionary[token] += 1
            else:
                ham_dictionary[token] = 1


    ## Reformat the testing dataframe
    test_df = test_df.rename(columns={'Label': 'Actual'})
    test_df = test_df.drop('Message', axis=1)
    predictions = []
    for index, row in test_df.iterrows():
        current_tokens = row['Tokens']
        spam_prob = spam_percent
        ham_prob = ham_percent
        for token in current_tokens:
            if token in spam_dictionary:
                spam_prob = spam_prob * ((spam_dictionary[token] + .00001))
            else:
                spam_prob = spam_prob * (.00001)
            if token in ham_dictionary:
                ham_prob = ham_prob * ((ham_dictionary[token] + .00001))
            else:
                ham_prob = ham_prob * (.00001)
        if(spam_prob >= ham_prob):
            predictions.append('spam')
        else:
            predictions.append('ham')


    test_df.insert(1, 'Expected', predictions)
    # get the number of matches between column 1 and column 2
    num_matches = sum(test_df['Actual'] == test_df['Expected'])

    # get the total number of rows
    num_rows = len(test_df)

    # calculate the percentage of matches
    percentage_matches = (num_matches / num_rows) * 100
    print("Percent Correctly Predicted: " + str(percentage_matches) + '\n')



# Function to remove all punctuation
def remove_punctuation(text):
    punctuationfree="".join([i for i in text if i not in string.punctuation])
    return punctuationfree

# Function to remove stopwords
def remove_stopwords(text):
    output= [i for i in text if i not in stopwords]
    return output

# Function to replace URLs with WWW
def replace_www(text):
    return re.sub(r'www\S+', 'WWW', text)

# Function to replace URLs with HTTP
def replace_urls(text):
    return re.sub(r'http\S+', 'HTTP', text)

# Function to convert lines into tokens
def tokenization(text):
    tk = WhitespaceTokenizer()
    return tk.tokenize(text)

if __name__ == "__main__":
    main()