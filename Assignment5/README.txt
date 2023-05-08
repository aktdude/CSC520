This is the README report associated with filter.py
There is another readme that came with the data collection, so that it is not confused.

This program takes in the data set and aims to classify the data as either spam or ham.

Statistics:
Total Messages in Data Set: 5574
Total Spam Messages: 747
Total Ham Messages: 4827

Preprocessing steps:
1. Filtered the initial data into a column LABEL containing the spam/ham label, and then the attached message in a column MESSAGE
2. Lowercase all Messages
3. Remove punctuations from messages
4. Replace URLs starting with www or http with a token representing the URL
5. Tokenize the messages
6. Remove stopwords

Train/Test Split:
The model shuffles the dataset so that everytime it runs, the data is in a different order.
This ensures the model works on any order of data.
The model divides 75% of the messages into the training dataset and the remaining 25% of the messages into the testing dataset.


Calculations:
The model then goes through all of the spam and ham messages in the training dataset.
It puts together a spam dictionary and a ham dictionary based off of the tokens in the training dataset messages.
Then for each preprocessed message in the testing dataset, it checks to see which probability is more likely, spam or ham.
This probability comes from multiplying the base spam/ham probabilities from the testing set, with the specific word probabilities from the dictionary.
There is also an added .00001 to certain probabilities, just to ensure that a zero probability from an unseen word doesn't cause an entire probability to zero out.

Range of Percentage Correct:
When applying the model from the testing dataset to the training set, it correctly predicts about 95% (94-96) the messages in the testing dataset.
