# -*- coding: utf-8 -*-
"""MUSIC_GENERATION_USING_LSTM

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1OgF1atThRwYwrqe-mFuXOzAi0MOBU8-4
"""

# Commented out IPython magic to ensure Python compatibility.
# %tensorflow_version 2.x
import tensorflow as tf 
import numpy as np
import os
import time
import functools
from IPython import display as ipythondisplay
from tqdm import tqdm
!apt-get install abcmidi timidity > /dev/null 2>&1

!pip install mitdeeplearning
import mitdeeplearning as mdl

with open('jigs.txt') as f:
    string = f.read()
    jigs = string.split("\n\n\n")

with open('carrols.txt') as f:
    string = f.read()
    carrols = string.split("\n\n\n")

with open('hornpipes.txt') as f:
    string = f.read()
    hornpipes = string.split("\n\n\n")

with open('morris.txt') as f:
    string = f.read()
    morris = string.split("\n\n\n")

with open('playford.txt') as f:
    string = f.read()
    playford = string.split("\n\n\n")

with open('waltzes.txt') as f:
    string = f.read()
    waltzes = string.split("\n\n\n")

songs = []

for i in [jigs, carrols, hornpipes, morris, playford, waltzes]:
  for j in i:
    songs.append(j)

songs

for i in songs:
  print(i[0])

songs_new = []

for i in range(4):
  for song in songs:
    if song[0] == '\n':
      songs_new.append(song[1:])
    else:
      songs_new.append(song)

songs_new

mdl.lab1.play_song(songs_new[-1])

# CONCATENATING ALL SONGS IN SONGS_NEW LIST TOGETHER
all_songs = "\n\n".join(songs_new) 


# CREATING A VOCABULARY FOR SONGS BY FINDING ALL UNIQUE CHARACTERS
vocab = sorted(set(all_songs))

# CREATING INDEX FOR EACH UNIQUE CHARACTER 
char_ind = {i:j for j, i in enumerate(vocab)}

# CREATING INVERSE OF CHAR_IDX TO CONVERT BACK THE INDICES TO CHARACTERS LATER
ind_char = np.array(vocab)

# WE NEED TO CONVERT THE TEXTUAL DATA INTO NUMERICAL DATA IN ORDER FOR IT'S CONVERSION

text_to_numerical_songs = np.array([char_ind[char] for char in all_songs])

text_to_numerical_songs.shape

# CREATING A FUNCTION TO GENERATE INPUT AND OUTPUT BATCH SEQUENCES

def generate_batches(songs, sequence_length, batch_size):

  l = songs.shape[0] - 1
  
  # RANDOMLY ALOTTING INDICES FOR GENERATING BATCHES
  indices = np.random.choice(l-sequence_length, batch_size)

  X = [songs[i : i+sequence_length] for i in indices]

  # SHIFTING THE INPUT SEQUENCES BY ONE CHARACTER TO THE RIGHT 
  y = [songs[i+1 : i+sequence_length+1] for i in indices]

  X = np.reshape(X, [batch_size, sequence_length])
  y = np.reshape(y, [batch_size, sequence_length])

  return X, y

# SETTING UP HYPERPARAMETERS 

vocab_size = len(vocab)
batch_size = 32
lstm_units = 1024
embedding_dim = 256
sequence_length = 128
learning_rate = 5e-3
num_training_iterations = 2000

# CREATING A LSTM MODEL USING TENSORFLOW SEQUENTIAL API

model = tf.keras.Sequential([
    tf.keras.layers.Embedding(vocab_size, embedding_dim, batch_input_shape=[batch_size, None]),
    tf.keras.layers.LSTM(lstm_units, return_sequences=True, recurrent_initializer='glorot_uniform', recurrent_activation='sigmoid', stateful=True),
    tf.keras.layers.Dense(vocab_size)
  ])

# PRINTING OUT THE SUMMARY OF THE MODEL
model.summary()

# CREATING TRAINING INPUT AND OUTPUT SEQUENCES 

X, y = generate_batches(text_to_numerical_songs, sequence_length, batch_size)

# DEFINING LOSS FOR OUT LSTM MODEL

def compute_loss(labels, logits):
  loss = tf.keras.losses.sparse_categorical_crossentropy(labels, logits, from_logits=True)
 
  return loss

# CCREATING A DIRECTORY FOR STORING THE MODEL WEIGHTS
 
checkpoint_directory = './trained_weights'
weights = os.path.join(checkpoint_directory, "weights")

# SETTING OPTIMIZER AS ADAM

optimizer = tf.keras.optimizers.Adam(learning_rate)

@tf.function
def train_step(x, y): 
  
  with tf.GradientTape() as tape:
    y_hat = model(x)
    loss = compute_loss(y, y_hat)

  # PERFORMING GRADIENT DESCENT AND UPDATING THE MODEL WEIGHTS
  
  grads = tape.gradient(loss, model.trainable_variables)
  optimizer.apply_gradients(zip(grads, model.trainable_variables))

  # RETURNING THE NEW LOSS
  return loss

history = []

for i in range(num_training_iterations):

  print("Number of Iterations completed : ", i)
  X, y = generate_batches(text_to_numerical_songs, sequence_length, batch_size)
  loss = train_step(X, y)

  history.append(loss.numpy().mean())
  

model.save_weights(weights)

# PLOTTING THE LOSS VS EPOCHS GRAPH 

import matplotlib.pyplot as plt

epochs = np.array([i for i in range(num_training_iterations)])

plt.plot(epochs, history)
plt.xlabel("Epochs")
plt.ylabel("Loss")
plt.title("LOSS VS EPOCHS")

# PRE-LOADING THE WEIGHTS OF MODEL AND INITIALIZING BATCH SIZE AS 1

model = tf.keras.Sequential([
    tf.keras.layers.Embedding(vocab_size, embedding_dim, batch_input_shape=[1, None]),
    tf.keras.layers.LSTM(lstm_units, return_sequences=True, recurrent_initializer='glorot_uniform', recurrent_activation='sigmoid', stateful=True),
    tf.keras.layers.Dense(vocab_size)
  ])

model.load_weights(tf.train.latest_checkpoint(checkpoint_directory))
model.build(tf.TensorShape([1, None]))

model.summary()

def generate_text(model, start_string, generation_length=1000):
  
  # CREATING A INPUT SEQUENCE WITH THE PROVIDED STARTING STRING
  input_eval = [char_ind[s] for s in start_string]
  
  input_eval = tf.expand_dims(input_eval, 0)

  text_generated = [] 
  model.reset_states()
 

  for i in range(generation_length):
      
      # PREDICTING THE OUTPUT SEQUENCE

      predictions = model(input_eval)
      predictions = tf.squeeze(predictions, 0)
           
      predicted_id = tf.random.categorical(predictions, num_samples=1)[-1,0].numpy()     
      input_eval = tf.expand_dims([predicted_id], 0)
      
      # CONVERTING THE NUMERICAL SEQUENCE BACK TO CHARACTERS IN THE VOCABULARY
      text_generated.append(ind_char[predicted_id]) 
  
  # RETURNING THE CHARACTER SEQUENCE
  return (start_string + ''.join(text_generated))

for j in range(10):
  generated_text = generate_text(model, start_string="X", generation_length=1000)
  generated_songs = mdl.lab1.extract_song_snippet(generated_text)
  for i, song in enumerate(generated_songs): 
    waveform = mdl.lab1.play_song(song)
    ipythondisplay.display(waveform)