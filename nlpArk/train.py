import json

from nltkUtils import tokenize, stemWords

with open('intents.json', 'r') as f:
    intents = json.load(f)
    
# print(intents)
allWords = []
tags = []
xy = []

for intent in intents['intents']:  # each intent has a tag, patterns and responses
    tag = intent['tag']
    tags.append(tag)
    for pattern in intent['patterns']:
        tokenList = tokenize(pattern)
        allWords.extend(tokenList)
        xy.append((tokenList, tag))

ignoreWords = ['?', '!', '.', ',']
allWords = [stemWords(w) for w in allWords if w not in ignoreWords]
allWords = sorted(set(allWords))
print(tags)
    
    