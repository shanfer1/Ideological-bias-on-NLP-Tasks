# -*- coding: utf-8 -*-
"""RNN - Final Results.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/11vuhoADrxBRECFjMUgCNmd4r_KM1UpFQ
"""


from keras.preprocessing.text import one_hot
import pandas as pd
import tweepy
import numpy as np
from nltk.tokenize import word_tokenize
from nltk import pos_tag
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from sklearn.preprocessing import LabelEncoder
from collections import defaultdict
from nltk.corpus import wordnet as wn
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn import model_selection, naive_bayes, svm
from sklearn.metrics import accuracy_score
from sklearn.metrics import classification_report
from sklearn.metrics import confusion_matrix
import matplotlib.pyplot as plt
import seaborn as sns
import tensorflow as tf
from nltk.stem import WordNetLemmatizer
from keras.preprocessing.text import Tokenizer
from keras.utils import to_categorical
from keras_preprocessing.sequence import pad_sequences
from tensorflow.keras import layers
from sklearn.metrics import accuracy_score
from sklearn.metrics import classification_report
from sklearn.metrics import confusion_matrix

"""# Getting preprocessed data for CNN from CSV file"""

np.random.seed(500)
preprocessedData_CNN = pd.read_csv('./data/preprocessed_nov_23_df_cnn_topic_combined.csv',delimiter=',',encoding='latin-1')
preprocessedData_CNN.head()

"""# Getting preprocessed data for FOX from CSV file"""

np.random.seed(500)
preprocessedData_Fox = pd.read_csv('./data/preprocessed_nov_23_df_fox_topic_combined.csv',delimiter=',',encoding='latin-1')
preprocessedData_Fox.head()

"""# Getting preprocessed data for REUTERS from CSV file"""

np.random.seed(500)
preprocessedData_Reuters = pd.read_csv('./data/preprocessed_nov_23_df_reuters_topic_combined.csv',delimiter=',',encoding='latin-1')
preprocessedData_Reuters.head()

sns.countplot(preprocessedData_CNN.topic)
plt.xlabel('Category')
plt.title('CountPlot')

sns.countplot(preprocessedData_Fox.topic)
plt.xlabel('Category')
plt.title('CountPlot')

sns.countplot(preprocessedData_Reuters.topic)
plt.xlabel('Category')
plt.title('CountPlot')

"""# Additional DataPreProcessing for RNN"""

vocab_size=1000

def padding(data_frame):
    MAX_WORDS = 1000
    MAX_SEQUENCE_LENGTH=1000
    encoded_docs=[one_hot(item['clean_text'],vocab_size) for i,item in data_frame.iterrows()]
    text=data_frame['clean_text'].to_list()
    labels=data_frame['topicEncoded'].to_list()

    tokenizer  = Tokenizer(num_words = MAX_WORDS)
    tokenizer.fit_on_texts(text)
    sequences =  tokenizer.texts_to_sequences(text)

    word_index = tokenizer.word_index

    data = pad_sequences(sequences, maxlen=MAX_SEQUENCE_LENGTH)

    labels = to_categorical(np.asarray(labels))
    return data, labels


"""# Training on CNN """

Train_X_CNN, Train_Y_CNN = preprocessedData_CNN['clean_text'], preprocessedData_CNN['topicEncoded']
Test_X_FOX, Test_Y_FOX = preprocessedData_Fox['clean_text'], preprocessedData_Fox['topicEncoded']
Test_X_Reuters, Test_Y_Reuters = preprocessedData_Reuters['clean_text'], preprocessedData_Reuters['topicEncoded']
x_train_cnn, y_train_cnn = padding(preprocessedData_CNN)
x_test_fox, y_test_fox = padding(preprocessedData_Fox)
x_test_reuters, y_test_reuters = padding(preprocessedData_Reuters)

word_size = 1000
embed_size = 500
imdb_model=tf.keras.Sequential()
imdb_model.add(tf.keras.layers.Embedding(word_size, embed_size, input_shape=(x_train_cnn.shape[1],)))
imdb_model.add(tf.keras.layers.LSTM(units=128, activation='tanh'))
# Output Layer
imdb_model.add(tf.keras.layers.Dense(units=5, activation='sigmoid'))
imdb_model.compile(optimizer='rmsprop', loss='binary_crossentropy', metrics=['accuracy'])

"""#### Training the model"""

imdb_model.fit(x_train_cnn, y_train_cnn, epochs=25, batch_size=128)

"""# Testing on FOX News"""

test_loss, test_acurracy = imdb_model.evaluate(x_test_fox, y_test_fox)

print("RNN Test accuracy score: {}".format(test_acurracy*100))

y_pred=imdb_model.predict(x_test_fox, batch_size=200, verbose=2)
report = classification_report(y_test_fox, y_pred.round())
print(report)
# print(classification_report(Test_Y_Reuters,test_acurracy))

"""# Testing on Reuters News"""

test_loss, test_acurracy = imdb_model.evaluate(x_test_reuters, y_test_reuters)

print("RNN Test accuracy score: {}".format(test_acurracy*100))

y_pred=imdb_model.predict(x_test_reuters, batch_size=200, verbose=2)
report = classification_report(y_test_reuters, y_pred.round())
print(report)

"""# Training on FOX News"""

Train_X_FOX, Train_Y_FOX = preprocessedData_Fox['clean_text'], preprocessedData_Fox['topicEncoded']
Test_X_CNN, Test_Y_CNN = preprocessedData_CNN['clean_text'], preprocessedData_CNN['topicEncoded']
Test_X_Reuters, Test_Y_Reuters = preprocessedData_Reuters['clean_text'], preprocessedData_Reuters['topicEncoded']
x_train_fox, y_train_fox = padding(preprocessedData_Fox)
x_test_cnn, y_test_cnn = padding(preprocessedData_CNN)
x_test_reuters, y_test_reuters = padding(preprocessedData_Reuters)

word_size = 1000
embed_size = 500
imdb_model=tf.keras.Sequential()
imdb_model.add(tf.keras.layers.Embedding(word_size, embed_size, input_shape=(x_train_fox.shape[1],)))
imdb_model.add(tf.keras.layers.LSTM(units=128, activation='tanh'))
# Output Layer
imdb_model.add(tf.keras.layers.Dense(units=5, activation='sigmoid'))
imdb_model.compile(optimizer='rmsprop', loss='binary_crossentropy', metrics=['accuracy'])

"""#### Training the model"""

imdb_model.fit(x_train_fox, y_train_fox, epochs=25, batch_size=128)

"""# Testing on CNN News"""

test_loss, test_acurracy = imdb_model.evaluate(x_test_cnn, y_test_cnn)

print("RNN Test accuracy score: {}".format(test_acurracy*100))

y_pred=imdb_model.predict(x_test_cnn, batch_size=200, verbose=2)
report = classification_report(y_test_cnn, y_pred.round())
print(report)
# print(classification_report(Test_Y_Reuters,test_acurracy))

"""# Testing on Reuters News"""

test_loss, test_acurracy = imdb_model.evaluate(x_test_reuters, y_test_reuters)

print("RNN Test accuracy score: {}".format(test_acurracy*100))

y_pred=imdb_model.predict(x_test_reuters, batch_size=200, verbose=2)
report = classification_report(y_test_reuters, y_pred.round())
print(report)
# print(classification_report(Test_Y_Reuters,test_acurracy))

"""# Training on Reuters News"""

Train_X_Reuters, Train_Y_Reuters = preprocessedData_Reuters['clean_text'], preprocessedData_Reuters['topicEncoded']
Test_X_CNN, Test_Y_CNN = preprocessedData_CNN['clean_text'], preprocessedData_CNN['topicEncoded']
Test_X_FOX, Test_Y_FOX = preprocessedData_Fox['clean_text'], preprocessedData_Fox['topicEncoded']
x_train_reuters, y_train_reuters = padding(preprocessedData_Reuters)
x_test_cnn, y_test_cnn = padding(preprocessedData_CNN)
x_test_fox, y_test_fox = padding(preprocessedData_Fox)

word_size = 1000
embed_size = 500
imdb_model=tf.keras.Sequential()
imdb_model.add(tf.keras.layers.Embedding(word_size, embed_size, input_shape=(x_train_reuters.shape[1],)))
imdb_model.add(tf.keras.layers.LSTM(units=128, activation='tanh'))
# Output Layer
imdb_model.add(tf.keras.layers.Dense(units=5, activation='sigmoid'))
imdb_model.compile(optimizer='rmsprop', loss='binary_crossentropy', metrics=['accuracy'])

"""#### Training the model"""

imdb_model.fit(x_train_reuters, y_train_reuters, epochs=25, batch_size=128)

"""# Testing on CNN News"""

test_loss, test_acurracy = imdb_model.evaluate(x_test_cnn, y_test_cnn)

print("RNN Test accuracy score: {}".format(test_acurracy*100))

y_pred=imdb_model.predict(x_test_cnn, batch_size=200, verbose=2)
report = classification_report(y_test_cnn, y_pred.round())
print(report)
# print(classification_report(Test_Y_Reuters,test_acurracy))

"""# Testing on FOX News"""

test_loss, test_acurracy = imdb_model.evaluate(x_test_fox, y_test_fox)

print("RNN Test accuracy score: {}".format(test_acurracy*100))

y_pred=imdb_model.predict(x_test_fox, batch_size=200, verbose=2)
report = classification_report(y_test_fox, y_pred.round())
print(report)

"""# Training and Testing on Reuters News"""

test_loss, test_acurracy = imdb_model.evaluate(x_train_reuters, y_train_reuters)

print("RNN Test accuracy score: {}".format(test_acurracy*100))

y_pred=imdb_model.predict(x_train_reuters, batch_size=200, verbose=2)
report = classification_report(y_train_reuters, y_pred.round())
print(report)

