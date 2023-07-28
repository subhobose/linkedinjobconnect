import json
import numpy as np
from nltkUtils import tokenize, stemWords, bagOfWords
from model import NLPEngine
import torch
import torch.nn as nn

from torch.utils.data import Dataset, DataLoader

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
tags = sorted(set(tags))

x_train = []
y_train = []

for (pattern, tag) in xy:
    bag = bagOfWords(pattern, allWords)
    x_train.append(bag)
    
    labels = tags.index(tag)
    y_train.append(labels)

x_train = np.array(x_train)
y_train = np.array(y_train)

class ChatData(Dataset):
    
    def __init__(self):
        self.numOfSamples = len(x_train)
        self.x_data = x_train
        self.y_data = y_train
    
    def __getitem__(self, index):
        return self.x_data[index], self.y_data[index]
    
    def __len__(self):
        return self.numOfSamples

dataset = ChatData()

batch_size = 8
hidden_size = 8
output_size = len(tags)
input_size = len(x_train[0])
learning_rate = 0.001
num_epochs = 1000

train_loader = DataLoader(dataset=dataset, batch_size=batch_size, shuffle=True, num_workers=0)

device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
model = NLPEngine(input_size, hidden_size, output_size).to(device)

criterion = nn.CrossEntropyLoss()
optimizer = torch.optim.Adam(model.parameters(), lr=learning_rate)

for epoch in range(num_epochs):
    
    for (words, labels) in train_loader:
        words = words.to(device)
        labels = labels.to(dtype=torch.long).to(device)
        
        outputs = model(words)
        loss = criterion(outputs, labels)
        
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()
        
    if (epoch+1) % 100 == 0:
        print(f'epoch {epoch+1}/{num_epochs}, loss={loss.item():.4f}')
        
print(f'Final Loss, loss={loss.item():.4f}')

data = {
    "model_state": model.state_dict(),
    "input_size": input_size,
    "output_size": output_size,
    "hidden_size": hidden_size,
    "all_words": allWords,
    "tags": tags
}

FILE = "data.pth"
torch.save(data, FILE)

print(f'Training Complete! File saved to {FILE}')
    
    