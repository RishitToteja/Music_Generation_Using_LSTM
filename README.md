# Music_Generation_Using_LSTM

The AI model generates various melodies [samples](https://soundcloud.com/rishit-toteja/sets/ai-generated-music-piano?utm_source=clipboard&utm_medium=text&utm_campaign=social_sharing) was trained on famous Irish Folk Songs (Jigs), Christmas Carols, and renowned pianist John Playford.

The Dataset was obtained from the Nottingham Music Database, which contains over 1000 Folk Tunes stored in a special text format. Using NMD2ABC, a program written by Jay Glanville and some Perl scripts, the bulk of this database has been converted to ABC notation.

The ABC Notation of each song was originally in text format. However, to feed the data to our neural network, we need to convert the textual data to a numerical format.
So, first, we can create a vocabulary to store all the unique characters in all the songs and then converted the characters in the text into numbers according to their indices in the vocabulary.


# Long Short Term Memory Network (LSTM)

![alt text](https://miro.medium.com/max/1400/0*3sFqvDBejuRpjcNm.png)

What we can see in the above image is a single LSTM block. “LSTMs” is a particular type of Recurrent Neural Network.

The horizontal line running through the top of the diagram is the key to LSTM’s. The cell state functions as a conveyor belt, running straight down the entire chain. This makes the information flow very quickly across different blocks and remains unchanged.

The LSTM can remove or add information to the cell state; this process is done with the help of gates (which can be seen in the above LSTM block). Gates are a way to let information go through optionally. Gates usually comprise a sigmoid neural net layer and a pointwise multiplication operation.

To build the model, Tensorflow Sequential API was used, and the whole project was carried out in Google Colab Environment.

Finally, the model was trained for 2000 epochs and the Model Loss VS Epochs plot can be seen below:

![alt text](https://miro.medium.com/max/960/1*v88bD3oGo95wwofUiEt95A.jpeg)

# Generating Melodies

After the model was trained, to generate new music sequences we need to convert the output of the model from numerical format to their respective characters according to the vocabulary.

Then I used the mitdeeplearning module to convert the ABC Notation music to a song (WAV output).

# References:

1) The Nottingham Music Database: http://abc.sourceforge.net/NMD/

2) Article on LSTM by Christopher Olah: https://colah.github.io/posts/2015-08-Understanding-LSTMs/

3) Google Colab Project Link: https://colab.research.google.com/drive/1OgF1atThRwYwrqe-mFuXOzAi0MOBU8-4?usp=sharing

4) Medium Publication Link: https://python.plainenglish.io/challenging-beethoven-with-artificial-intelligence-927749baf9e5 
