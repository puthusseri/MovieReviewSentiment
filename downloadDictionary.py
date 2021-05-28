# python code to save the word_to_id for converting the sentence to the numbers.
# you only need to do it once to save the file. Internet is required for this. You only need to run this if the filenmaed, word_to_pkl is not found in the folder
# filename : downloadDictionary.py
import pickle
from keras.datasets import imdb

word_to_id = imdb.get_word_index()
word_to_id = {key:(value+3) for key,value in word_to_id.items()}
word_to_id["<PAD>"] = 0
word_to_id["<START>"] = 1
id_to_word = {value:key for key,value in word_to_id.items()}
f = open("word_to_id.pkl", "wb")
pickle.dump(word_to_id, f)
f.close()