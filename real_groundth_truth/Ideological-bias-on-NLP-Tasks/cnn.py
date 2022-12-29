# -*- coding: utf-8 -*-
"""cnnkaggle.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1mXRHWPWSJWMzGmqBN7Wo5yz82RBQOPug
"""

import sys
import numpy as np
import tensorflow 
import keras
from keras.preprocessing.text import Tokenizer
from keras.utils import to_categorical
from keras_preprocessing.sequence import pad_sequences
from keras.layers import Activation, Conv2D, Input, Embedding, Reshape, MaxPool2D, Concatenate, Flatten, Dropout, Dense, Conv1D
from keras.layers import MaxPool1D
from keras.models import Model
from keras.callbacks import ModelCheckpoint
from keras.optimizers import Adam
import pandas as pd

import os
import zipfile

# TEXT_DATA_DIR = r'../input/20-newsgroup-original/20_newsgroup/20_newsgroup/'
#the path for Glove embeddings
GLOVE_DIR = r'./tmp/glove/'
# make the max word length to be constant
MAX_WORDS = 10000
MAX_SEQUENCE_LENGTH = 1000
# the percentage of train test split to be applied
VALIDATION_SPLIT = 0.50
# the dimension of vectors to be used
EMBEDDING_DIM = 100
# filter sizes of the different conv layers 
filter_sizes = [3,4,5]
num_filters = 512
embedding_dim = 100
# dropout probability
drop = 0.5
batch_size = 30
epochs = 50

df_cnn=pd.read_csv('./data/preprocessed_nov_23_df_cnn_topic_combined.csv')
texts_cnn=df_cnn["clean_text"].tolist()
labels_cnn=df_cnn["topicEncoded"].to_list()

print(len(texts_cnn))
print(len(labels_cnn))

tokenizer  = Tokenizer(num_words = MAX_WORDS)
tokenizer.fit_on_texts(texts_cnn)
sequences =  tokenizer.texts_to_sequences(texts_cnn)

word_index = tokenizer.word_index
print("unique words : {}".format(len(word_index)))

data = pad_sequences(sequences, maxlen=MAX_SEQUENCE_LENGTH)

labels_cnn = to_categorical(np.asarray(labels_cnn))
print('Shape of data tensor:', data.shape)
print('Shape of label tensor:', labels_cnn.shape)
print(labels_cnn)

indices = np.arange(data.shape[0])
print(indices)
np.random.shuffle(indices)
data = data[indices]
labels = labels_cnn[indices]

from sklearn.model_selection import train_test_split
X_train, X_rem, y_train, y_rem = train_test_split(data,labels, train_size=0.7)

nb_validation_samples = int(VALIDATION_SPLIT * X_rem.shape[0])
x_test = X_rem[:-nb_validation_samples]
y_test = y_rem[:-nb_validation_samples]
x_val = X_rem[-nb_validation_samples:]
y_val = y_rem[-nb_validation_samples:]

print(X_train.shape)
print(y_train.shape)
print(x_test.shape)
print(y_test.shape)
print(x_val.shape)
print(y_val.shape)


with zipfile.ZipFile('glove.6B.zip', 'r') as zip_ref:
    zip_ref.extractall('.//tmp/glove')

embeddings_index = {}
f = open(os.path.join(GLOVE_DIR, 'glove.6B.100d.txt'),encoding="utf8")
for line in f:
    values = line.split()
    word = values[0]
    coefs = np.asarray(values[1:], dtype='float32')
    embeddings_index[word] = coefs
f.close()

print('Found %s word vectors.' % len(embeddings_index))

embedding_matrix = np.zeros((len(word_index) + 1, EMBEDDING_DIM))
for word, i in word_index.items():
    embedding_vector = embeddings_index.get(word)
    if embedding_vector is not None:
        # words not found in embedding index will be all-zeros.
        embedding_matrix[i] = embedding_vector

from keras.layers import Embedding

embedding_layer = Embedding(len(word_index) + 1,
                            EMBEDDING_DIM,
                            weights=[embedding_matrix],
                            input_length=MAX_SEQUENCE_LENGTH,
                            trainable=False)

inputs = Input(shape=(MAX_SEQUENCE_LENGTH,), dtype='int32')
embedding = embedding_layer(inputs)

print(embedding.shape)
reshape = Reshape((MAX_SEQUENCE_LENGTH,EMBEDDING_DIM,1))(embedding)
print(reshape.shape)

conv_0 = Conv2D(num_filters, kernel_size=(filter_sizes[0], embedding_dim), padding='valid', kernel_initializer='normal', activation='relu')(reshape)
conv_1 = Conv2D(num_filters, kernel_size=(filter_sizes[1], embedding_dim), padding='valid', kernel_initializer='normal', activation='relu')(reshape)
conv_2 = Conv2D(num_filters, kernel_size=(filter_sizes[2], embedding_dim), padding='valid', kernel_initializer='normal', activation='relu')(reshape)

maxpool_0 = MaxPool2D(pool_size=(MAX_SEQUENCE_LENGTH - filter_sizes[0] + 1, 1), strides=(1,1), padding='valid')(conv_0)
maxpool_1 = MaxPool2D(pool_size=(MAX_SEQUENCE_LENGTH - filter_sizes[1] + 1, 1), strides=(1,1), padding='valid')(conv_1)
maxpool_2 = MaxPool2D(pool_size=(MAX_SEQUENCE_LENGTH - filter_sizes[2] + 1, 1), strides=(1,1), padding='valid')(conv_2)

concatenated_tensor = Concatenate(axis=1)([maxpool_0, maxpool_1, maxpool_2])
flatten = Flatten()(concatenated_tensor)
dropout = Dropout(drop)(flatten)
output = Dense(units=5, activation='softmax')(dropout)

# this creates a model that includes
model = Model(inputs=inputs, outputs=output)

checkpoint = ModelCheckpoint('weights_cnn_sentece.hdf5', monitor='val_acc', verbose=1, save_best_only=True, mode='auto')
adam = Adam(lr=1e-4, beta_1=0.9, beta_2=0.999, epsilon=1e-08, decay=0.0)

model.compile(optimizer=adam, loss='categorical_crossentropy', metrics=['accuracy'])
model.summary()

print("Traning Model...")
model.fit(X_train, y_train, batch_size=batch_size, epochs=epochs, verbose=1, callbacks=[checkpoint], validation_data=(x_val, y_val))

"""# Training and Testing on Left"""

test_loss, test_acc = model.evaluate(x_test,  y_test, verbose=2)
print('Test Accuracy for training and testing on the cnn dataset: %f' % (test_acc*100))

"""# Training on left and testing it on right"""

df_fox=pd.read_csv('./data/preprocessed_nov_23_df_fox_topic_combined.csv')
texts_fox=df_fox["clean_text"].tolist()
labels_fox=df_fox["topicEncoded"].to_list()

df_reuters=pd.read_csv('./data/preprocessed_nov_23_df_reuters_topic_combined.csv')
texts_reuters=df_reuters["clean_text"].tolist()
labels_reuters=df_reuters["topicEncoded"].to_list()

tokenizer  = Tokenizer(num_words = MAX_WORDS)
tokenizer.fit_on_texts(texts_fox)
sequences =  tokenizer.texts_to_sequences(texts_fox)

word_index = tokenizer.word_index
print("unique words : {}".format(len(word_index)))

data = pad_sequences(sequences, maxlen=MAX_SEQUENCE_LENGTH)

labels_fox = to_categorical(np.asarray(labels_fox))
print('Shape of data tensor:', data.shape)
print('Shape of label tensor:', labels_fox.shape)
print(labels_fox)

x_test=data
y_test=labels_fox

test_loss, test_acc = model.evaluate(x_test,  y_test, verbose=2)

"""# Training and testing on right data"""

df_fox=pd.read_csv('./data/preprocessed_nov_23_df_fox_topic_combined.csv')
texts_fox=df_fox["clean_text"].tolist()
labels_fox=df_fox["topicEncoded"].to_list()

tokenizer  = Tokenizer(num_words = MAX_WORDS)
tokenizer.fit_on_texts(texts_fox)
sequences =  tokenizer.texts_to_sequences(texts_fox)

word_index = tokenizer.word_index
print("unique words : {}".format(len(word_index)))

data = pad_sequences(sequences, maxlen=MAX_SEQUENCE_LENGTH)

labels_fox = to_categorical(np.asarray(labels_fox))
print('Shape of data tensor:', data.shape)
print('Shape of label tensor:', labels_fox.shape)
print(labels_fox)

indices = np.arange(data.shape[0])
print(indices)
np.random.shuffle(indices)
data = data[indices]
labels = labels_fox[indices]

from sklearn.model_selection import train_test_split
X_train, X_rem, y_train, y_rem = train_test_split(data,labels, train_size=0.7)

nb_validation_samples = int(VALIDATION_SPLIT * X_rem.shape[0])
x_test = X_rem[:-nb_validation_samples]
y_test = y_rem[:-nb_validation_samples]
x_val = X_rem[-nb_validation_samples:]
y_val = y_rem[-nb_validation_samples:]

print(X_train.shape)
print(y_train.shape)
print(x_test.shape)
print(y_test.shape)
print(x_val.shape)
print(y_val.shape)

embeddings_index = {}
f = open(os.path.join(GLOVE_DIR, 'glove.6B.100d.txt'),encoding="utf8")
for line in f:
    values = line.split()
    word = values[0]
    coefs = np.asarray(values[1:], dtype='float32')
    embeddings_index[word] = coefs
f.close()

print('Found %s word vectors.' % len(embeddings_index))

embedding_matrix = np.zeros((len(word_index) + 1, EMBEDDING_DIM))
for word, i in word_index.items():
    embedding_vector = embeddings_index.get(word)
    if embedding_vector is not None:
        # words not found in embedding index will be all-zeros.
        embedding_matrix[i] = embedding_vector

from keras.layers import Embedding

embedding_layer = Embedding(len(word_index) + 1,
                            EMBEDDING_DIM,
                            weights=[embedding_matrix],
                            input_length=MAX_SEQUENCE_LENGTH,
                            trainable=False)

inputs = Input(shape=(MAX_SEQUENCE_LENGTH,), dtype='int32')
embedding = embedding_layer(inputs)

print(embedding.shape)
reshape = Reshape((MAX_SEQUENCE_LENGTH,EMBEDDING_DIM,1))(embedding)
print(reshape.shape)

conv_0 = Conv2D(num_filters, kernel_size=(filter_sizes[0], embedding_dim), padding='valid', kernel_initializer='normal', activation='relu')(reshape)
conv_1 = Conv2D(num_filters, kernel_size=(filter_sizes[1], embedding_dim), padding='valid', kernel_initializer='normal', activation='relu')(reshape)
conv_2 = Conv2D(num_filters, kernel_size=(filter_sizes[2], embedding_dim), padding='valid', kernel_initializer='normal', activation='relu')(reshape)

maxpool_0 = MaxPool2D(pool_size=(MAX_SEQUENCE_LENGTH - filter_sizes[0] + 1, 1), strides=(1,1), padding='valid')(conv_0)
maxpool_1 = MaxPool2D(pool_size=(MAX_SEQUENCE_LENGTH - filter_sizes[1] + 1, 1), strides=(1,1), padding='valid')(conv_1)
maxpool_2 = MaxPool2D(pool_size=(MAX_SEQUENCE_LENGTH - filter_sizes[2] + 1, 1), strides=(1,1), padding='valid')(conv_2)

concatenated_tensor = Concatenate(axis=1)([maxpool_0, maxpool_1, maxpool_2])
flatten = Flatten()(concatenated_tensor)
dropout = Dropout(drop)(flatten)
output = Dense(units=5, activation='softmax')(dropout)

# this creates a model that includes
model = Model(inputs=inputs, outputs=output)

checkpoint = ModelCheckpoint('weights_cnn_sentece.hdf5', monitor='val_acc', verbose=1, save_best_only=True, mode='auto')
adam = Adam(lr=1e-4, beta_1=0.9, beta_2=0.999, epsilon=1e-08, decay=0.0)

model.compile(optimizer=adam, loss='categorical_crossentropy', metrics=['accuracy'])
model.summary()

print("Traning Model...")
model.fit(X_train, y_train, batch_size=batch_size, epochs=epochs, verbose=1, callbacks=[checkpoint], validation_data=(x_val, y_val))

test_loss, test_acc = model.evaluate(x_test,  y_test, verbose=2)
print('Test Accuracy for training and testing on the cnn dataset: %f' % (test_acc*100))

"""# Training on Right Data and Testing it on left data"""

df_cnn=pd.read_csv('./data/preprocessed_nov_23_df_cnn_topic_combined.csv')
texts_cnn=df_cnn["clean_text"].tolist()
labels_cnn=df_cnn["topicEncoded"].to_list()

tokenizer  = Tokenizer(num_words = MAX_WORDS)
tokenizer.fit_on_texts(texts_cnn)
sequences =  tokenizer.texts_to_sequences(texts_cnn)

word_index = tokenizer.word_index
print("unique words : {}".format(len(word_index)))

data = pad_sequences(sequences, maxlen=MAX_SEQUENCE_LENGTH)

labels_cnn = to_categorical(np.asarray(labels_cnn))
print('Shape of data tensor:', data.shape)
print('Shape of label tensor:', labels_cnn.shape)
print(labels_cnn)

indices = np.arange(data.shape[0])
print(indices)
np.random.shuffle(indices)
data = data[indices]
labels = labels_cnn[indices]

x_test=data
y_test=labels

test_loss, test_acc = model.evaluate(x_test,  y_test, verbose=2)
print('Test Accuracy for training on the fox dataset and testing on the cnn dataset: %f' % (test_acc*100))

