# Idelogical-Bias

Diclaimer: Code initially was written in ipynb files , those files are submitted with this project for the reference . Sepeated .py files are also generated, corresponding requirements.txt file is also submitted. 


# get the glove based embeddings
Just hit this url in browser

http://nlp.stanford.edu/data/glove.6B.zip

place the zip file in root directory

# Install the dependencies
python -m pip install -r requirements.txt

# Folder Strucure:
Data folder contains all the datasets we used
    it contains three different kinds of csv files , file whole tweet files scraped from twitter from a user timeline, and then topic labelled csv file and then preprocessed data files 

ipynb files with output  folder: 
    ipynb files that we used to develop is provided for the reference 

glove.6B.zip file used for embeddings for cnn

tmp folder contains the glove embeddings used for cnn.

.py files in the root directory 
    1. data collection
    2.topic labeling
    3.random forest includes preprocessing and saving to csv
    4.logistic regression
    5.cnn 
    6.support vector machines
    7.rnn 
    8.bert


# Run the .py files in order
1.python data_collection.py - already done and files are saved in data folder
2.python upgraded_strategy_for_topic_labelling_without_reuters.py - already done and files are saved in data folder
3.python random_forest.py - recommend to start from this step
4.python support_vector_machine_final_results.py
Disclaimer: since cnn and rnn_final_results are having conflicting dependencies on tensorflow, we were running it on colab, plz try to run those .py files in colab
5.python cnn.py
6.python rnn_final_results.py


//add bert 
