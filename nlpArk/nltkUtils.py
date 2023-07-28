import nltk
from nltk.stem.porter import PorterStemmer
import numpy as np

stemmer = PorterStemmer()

# nltk.download('punkt')
def tokenize(sentence):
    return nltk.word_tokenize(sentence)

def stemWords(word):
    return stemmer.stem(word.lower())

sample = "How are you?"

def bagOfWords(tokenizedSentence, allWords):
    
    tokenizedSentence = [stemWords(w) for w in tokenizedSentence]
    
    bag = np.zeros(len(allWords), dtype=np.float32)
    
    for i, w in enumerate(allWords):
        if w in tokenizedSentence:
            bag[i] = 1.0
    
    return bag

