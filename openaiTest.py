import json
from difflib import get_close_matches

def loadKnowledgeBase(pathToFile):
    
    with open(pathToFile, 'r') as jsonFile:
        jsonData = json.load(jsonFile)
        return jsonData

def saveKnowledgeBase(pathToFile, newJsonData):
    
    with open(pathToFile, 'w') as jsonFile:
        json.dump(newJsonData, jsonFile, indent=2)
        
def findBestMatchForQuery(userQuery, questions):
    
    matchedResponses = get_close_matches(userQuery, questions, n=1, cutoff=0.7)
    return matchedResponses[0] if matchedResponses else None

def getResponse(question, knowledgeBase):
    
    for q in knowledgeBase["questions"]:
        if q["question"] == question:
            return q["answer"]

def chatbot():
    
    knowledgeBase = loadKnowledgeBase('knowledgeBase.json')
    # print(knowledgeBase)
    
    while True:
        userInput = input("You: ")
        
        if userInput.lower() == "quit":
            break
        
        bestQueryMatch = findBestMatchForQuery(userInput, [q["question"] for q in knowledgeBase["questions"]])
        
        if bestQueryMatch:
            response = getResponse(bestQueryMatch, knowledgeBase)
            print("Bot: {}".format(response))
        
        else:
            print("Bot: Didnt encounter such a query before!")
            newResponse = input("Type answer or skip(s): ")
            
            if newResponse.lower() != "s":
                knowledgeBase["questions"].append({"question": userInput, "answer": newResponse})
                saveKnowledgeBase('knowledgeBase.json', knowledgeBase)
                print("Bot: Understood!")
                
    
if __name__ == "__main__":
    chatbot()
    
