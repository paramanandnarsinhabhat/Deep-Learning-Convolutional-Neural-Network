'''
# Steps to Follow
1. Load Data and Import Libraries
2. Text Cleaning
3. Merge Tags with Questions
4. Dataset Prepartion
5. Text Representation
6. Model Building
    1. Define Model Architecture
    2. Train the Model
7. Model Predictions
8. Model Evaluation
9. Inference
'''

# Load Data and Import Libraries
#string matching
import re 

#reading files
import pandas as pd
import numpy as np
#handling html data
from bs4 import BeautifulSoup

#visualization
import matplotlib.pyplot as plt  

pd.set_option('display.max_colwidth', 200)
import zipfile
import os
# load the stackoverflow questions dataset
# Specify the path to the zip file
zip_file_path = 'data/archive (2).zip'

# Specify the directory to extract to
extract_to_dir = 'data/unzipped_contents'

# Open the zip file
with zipfile.ZipFile(zip_file_path, 'r') as zip_ref:
    # Extract all the contents into the directory
    zip_ref.extractall(extract_to_dir)
    
    # List the contents of the extracted folder
    print(f"Contents of the zip file '{zip_file_path}':")
    for file_name in zip_ref.namelist():
        print(file_name)

questions_df = pd.read_csv('data/unzipped_contents/Questions.csv',encoding='latin-1')

print(questions_df.head())
# load the tags dataset
tags_df = pd.read_csv('data/unzipped_contents/Tags.csv')

print(tags_df.head())

#print first 5 rows
questions_df.head()

print(questions_df.head())

print(questions_df.columns)

# Text Cleaning

#Let's define a function to clean the text data.
def cleaner(text):

#   text = BeautifulSoup(text).get_text()
  text = BeautifulSoup(text, features="html.parser").get_text()

  # fetch alphabetic characters
  text = re.sub("[^a-zA-Z]", " ", text)

  # convert text to lower case
  text = text.lower()

  # split text into tokens to remove whitespaces
  tokens = text.split()

  return " ".join(tokens)

# call preprocessing function
questions_df['cleaned_text'] = questions_df['Body'].apply(cleaner)

print(questions_df['Body'][1])

# Merge Tags with Questions
#Let's now explore the tags data.
tags_df.head()

print(tags_df.head())

# count of unique tags
len(tags_df['Tag'].unique())

print(
len(tags_df['Tag'].unique()))

print(tags_df['Tag'].value_counts())

# remove "-" from the tags
tags_df['Tag']= tags_df['Tag'].apply(lambda x:re.sub("-"," ",x))

# group tags Id wise
tags_df = tags_df.groupby('Id').apply(lambda x:x['Tag'].values).reset_index(name='tags')
tags_df.head()

print(tags_df.head())

# merge tags and questions
df = pd.merge(questions_df,tags_df,how='inner',on='Id')

df = df[['Id','Body','cleaned_text','tags']]
print(df.head())

print(df.shape)

# Dataset Preparation
# check frequency of occurence of each tag
freq= {}
for i in df['tags']:
  for j in i:
    if j in freq.keys():
      freq[j] = freq[j] + 1
    else:
      freq[j] = 1

# sort the dictionary in descending order
freq = dict(sorted(freq.items(), key=lambda x:x[1],reverse=True))

print(freq.items())

# Top 10 most frequent tags
common_tags = list(freq.keys())[:10]
print(common_tags)

#We will use only those questions/queries that have the above 10 tags associated with it.
x=[]
y=[]

for i in range(len(df['tags'])):
  
  temp=[]
  for j in df['tags'][i]:
    if j in common_tags:
      temp.append(j)

  if(len(temp)>1):
    x.append(df['cleaned_text'][i])
    y.append(temp)

# number of questions left
len(x)

print(len(x))

print(y[:10])

#We will the input sequences to our model to the length of 100
from sklearn.preprocessing import MultiLabelBinarizer
mlb = MultiLabelBinarizer()
 
y = mlb.fit_transform(y)
y.shape

print(y.shape
)

print(y[0,:])

print(mlb.classes_)
#We can now split the dataset into training set and validation set. 

from sklearn.model_selection import train_test_split
x_tr,x_val,y_tr,y_val=train_test_split(x, y, test_size=0.2, random_state=0,shuffle=True)

# Text Representation
from keras.preprocessing.text import Tokenizer
from keras.preprocessing.sequence import pad_sequences 

#prepare a tokenizer
x_tokenizer = Tokenizer() 

#prepare vocabulary
x_tokenizer.fit_on_texts(x_tr)

print(x_tokenizer.word_index)

print(len(x_tokenizer.word_index))

#There are around 25,000 tokens in the training dataset. 
#Let's see how many tokens appear at least 5 times in the dataset.
thresh = 3

cnt=0
for key,value in x_tokenizer.word_counts.items():
  if value>=thresh:
    cnt=cnt+1

print(cnt)

#Over 12,000 tokens have appeared three times or more
#in the training set.
# prepare the tokenizer again
x_tokenizer = Tokenizer(num_words=cnt,oov_token='unk')

#prepare vocabulary
x_tokenizer.fit_on_texts(x_tr)

'''
Now that we have encoded every token to an integer, let's convert the text sequences to integer sequences. After that we will pad the integer sequences to the maximum sequence length, i.e., 100.


'''

#define threshold for maximum length of a setence
max_len=100

#convert text sequences into integer sequences
x_tr_seq = x_tokenizer.texts_to_sequences(x_tr) 
x_val_seq = x_tokenizer.texts_to_sequences(x_val)

#padding up with zero 
x_tr_seq = pad_sequences(x_tr_seq,  padding='post', maxlen=max_len)
x_val_seq = pad_sequences(x_val_seq, padding='post', maxlen=max_len)

#Since we are padding the sequences with zeros, 
#we must increment the vocabulary size by one.
#no. of unique words
x_voc_size = x_tokenizer.num_words + 1

print(x_voc_size)

print(x_tr_seq[0])

# Model Building
from keras.models import *
from keras.layers import *
from keras.callbacks import *
import keras.backend as k

### Define Model Architecture
# define model architecture
k.clear_session()
model =  Sequential()
model.add(Embedding(x_voc_size, 50, trainable=True, input_shape=(max_len,)))  #embedding layer
  
model.add(Conv1D(64,3,padding='same'))  #conv1d layer
model.add(Dropout(0.1))

model.add(GlobalMaxPooling1D()) 
  
model.add(Dense(128,activation='relu'))  #dense layer

model.add(Dense(10,activation='sigmoid')) #output layer
model.summary() #summary) of model

#define optimizer and loss
model.compile(optimizer='adam',loss='binary_crossentropy')

#checkpoint to save best model during training
mc = ModelCheckpoint("weights.best.hdf5", monitor='val_loss', verbose=1, save_best_only=True, mode='min')

### Train the Model
#train the model 
model.fit(x_tr_seq, y_tr, batch_size=128, epochs=10, verbose=1, validation_data=(x_val_seq, y_val), callbacks=[mc])

# Model Predictions 
# load weights into new model
model.load_weights("weights.best.hdf5")

#predict probabilities
pred_prob = model.predict(x_val_seq)

print(pred_prob[0])

'''
The predictions are in terms of probabilities for each of the 10 tags. Hence we need to have a threshold value to convert these probabilities to 0 or 1.

Let's specify a set of candidate threshold values. We will select the threshold value that performs the best for the validation set.

'''

#define candidate threshold values
threshold  = np.arange(0,0.5,0.01)
print(threshold)

'''
Let's define a function that takes a threshold value and uses it to convert probabilities into 1 or 0.

'''

# convert probabilities into classes or tags based on a threshold value
def classify(pred_prob,thresh):
  y_pred_seq = []

  for i in pred_prob:
    temp=[]
    for j in i:
      if j>=thresh:
        temp.append(1)
      else:
        temp.append(0)
    y_pred_seq.append(temp)

  return y_pred_seq

from sklearn import metrics
score=[]

#convert to 1 array
y_true = np.array(y_val).ravel() 

for thresh in threshold:
    
    #classes for each threshold
    y_pred_seq = classify(pred_prob,thresh) 

    #convert to 1d array
    y_pred = np.array(y_pred_seq).ravel()

    score.append(metrics.f1_score(y_true,y_pred))

 # find the optimal threshold
opt = threshold[score.index(max(score))]
print(opt)

# Model Evaluation
#predictions for optimal threshold
y_pred_seq = classify(pred_prob,opt)
y_pred = np.array(y_pred_seq).ravel()

print(metrics.classification_report(y_true,y_pred))

y_pred = mlb.inverse_transform(np.array(y_pred_seq))
y_true = mlb.inverse_transform(np.array(y_val))

df = pd.DataFrame({'comment':x_val,'actual':y_true,'predictions':y_pred})

print(df.sample(10))

# Inference
def predict_tag(comment):  
  text=[]

  #preprocess  
  text = [cleaner(comment)]

  #convert to integer sequences
  seq = x_tokenizer.texts_to_sequences(text)

  #pad the sequence
  pad_seq = pad_sequences(seq,  padding='post', maxlen=max_len)

  #make predictions
  pred_prob = model.predict(pad_seq)
  classes = classify(pred_prob,opt)[0]
  
  classes = np.array([classes])
  classes = mlb.inverse_transform(classes)  
  return classes

comment = "For example, in the case of logistic regression, the learning function is a Sigmoid function that tries to separate the 2 classes"

print("Comment:",comment)
print("Predicted Tags:",predict_tag(comment))

