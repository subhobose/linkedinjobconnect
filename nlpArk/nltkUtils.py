import nltk
from nltk.stem.porter import PorterStemmer
stemmer = PorterStemmer()

# nltk.download('punkt')
def tokenize(sentence):
    return nltk.word_tokenize(sentence)

def stemWords(word):
    return stemmer.stem(word.lower())

sample = "How are you?"

# print(tokenize(sample))
# print(stemWords("shipping"))

