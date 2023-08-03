import json
import torch
import random
from model import NLPEngine
from nltkUtils import tokenize, bagOfWords

device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

with open('intents.json', 'r') as f:
    intents = json.load(f)
FILE = "data.pth"
data = torch.load(FILE)
input_size = data["input_size"]
hidden_size = data["hidden_size"]
output_size = data["output_size"]
allWords = data["all_words"]
tags = data["tags"]
model_state = data["model_state"]

model = NLPEngine(input_size, hidden_size, output_size).to(device)
model.load_state_dict(model_state)

model.eval()

def chatFunction(sentence):
    
    sentence = tokenize(sentence)
    x = bagOfWords(sentence, allWords)
    x = x.reshape(1, x.shape[0])
    x = torch.from_numpy(x)

    output = model(x)
    _, predicted = torch.max(output, dim=1)
    tag = tags[predicted.item()]

    probs = torch.softmax(output, dim=1)
    prob = probs[0][predicted.item()]

    if prob > 0.9:
        for intent in intents["intents"]:
            if tag == intent["tag"]:
                return random.choice(intent["responses"])

    else:
        return ("No appropriate response")
        

