#!/usr/bin/env python

##  text_classification_with_TEXTnet_word2vec.py

"""
Now we use word embeddings for modeling the words in the sentiment
analysis dataset.

This script shows how you can use a neural network with feedback for
the classification of a variable-length sequence.  The main idea is to
represent a variable-length input with a fixed-length hidden state 
vector.  
"""

import random
import numpy
import torch
import os, sys


seed = 0           
random.seed(seed)
torch.manual_seed(seed)
torch.cuda.manual_seed(seed)
numpy.random.seed(seed)
torch.backends.cudnn.deterministic=True
torch.backends.cudnn.benchmarks=False
os.environ['PYTHONHASHSEED'] = str(seed)


##  watch -d -n 0.5 nvidia-smi

from DLStudio import *

dls = DLStudio(
#                  dataroot = "/home/kak/TextDatasets/sentiment_dataset/",
                  dataroot = "/data/TextDatasets/sentiment_dataset/",
                  path_saved_model = "./saved_model",
                  momentum = 0.9,
                  learning_rate =  1e-5,  
                  epochs = 1,
                  batch_size = 1,
                  classes = ('negative','positive'),
                  use_gpu = True,
              )


text_cl = DLStudio.TextClassificationWithEmbeddings( dl_studio = dls )

dataserver_train = DLStudio.TextClassificationWithEmbeddings.SentimentAnalysisDataset(
                                 train_or_test = 'train',
                                 dl_studio = dls,
                                 dataset_file = "sentiment_dataset_train_40.tar.gz",
#                                 dataset_file = "sentiment_dataset_train_200.tar.gz",
#                                 path_to_saved_embeddings = "/home/kak/TextDatasets/word2vec/",
                                 path_to_saved_embeddings = "/data/TextDatasets/word2vec/",
                   )
dataserver_test = DLStudio.TextClassificationWithEmbeddings.SentimentAnalysisDataset(
                                 train_or_test = 'test',
                                 dl_studio = dls,
                                 dataset_file = "sentiment_dataset_test_40.tar.gz",
#                                 dataset_file = "sentiment_dataset_test_200.tar.gz",
#                                 path_to_saved_embeddings = "/home/kak/TextDatasets/word2vec/",
                                 path_to_saved_embeddings = "/data/TextDatasets/word2vec/",
                  )
text_cl.dataserver_train = dataserver_train
text_cl.dataserver_test = dataserver_test

text_cl.load_SentimentAnalysisDataset(dataserver_train, dataserver_test)

model = text_cl.TEXTnetWithEmbeddings(hidden_size = 512, output_size = 2)

number_of_learnable_params = sum(p.numel() for p in model.parameters() if p.requires_grad)
num_layers = len(list(model.parameters()))

print("\n\nThe number of layers in the model: %d" % num_layers)
print("\nThe number of learnable parameters in the model: %d\n\n" % number_of_learnable_params)

text_cl.run_code_for_training_with_TEXTnet_word2vec(model, hidden_size=512)

import pymsgbox
response = pymsgbox.confirm("Finished training.  Start testing on unseen data?")
if response == "OK": 
    text_cl.run_code_for_testing_with_TEXTnet_word2vec(model, hidden_size=512)



