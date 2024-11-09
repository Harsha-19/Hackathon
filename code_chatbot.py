import nltk
import numpy as np
import random
import string  # To process standard python strings

from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Download the NLTK resources
nltk.download('punkt')
nltk.download('wordnet')

# Sample text data for the chatbot to respond to
corpus = """
Hello! I am a chatbot created to assist you with your queries. 
You can ask me about cybersecurity, tech tips, or any other general questions. 
I am here to provide you with information to the best of my knowledge.
"""

# Tokenize and clean the corpus
sentence_tokens = nltk.sent_tokenize(corpus)

# Preprocess text
lemmer = nltk.WordNetLemmatizer()
def LemTokens(tokens):
    return [lemmer.lemmatize(token) for token in tokens]

remove_punct_dict = dict((ord(punct), None) for punct in string.punctuation)
def LemNormalize(text):
    return LemTokens(nltk.word_tokenize(text.lower().translate(remove_punct_dict)))

# Greeting function
GREETING_INPUTS = ("hello", "hi", "greetings", "hey")
GREETING_RESPONSES = ["Hi there!", "Hello!", "Greetings!", "Hi! How can I assist you?"]

def greeting(sentence):
    """If a user's input is a greeting, return a greeting response."""
    for word in sentence.split():
        if word.lower() in GREETING_INPUTS:
            return random.choice(GREETING_RESPONSES)

# Response generation function
def response(user_response):
    sentence_tokens.append(user_response)
    
    # Vectorize the corpus
    vectorizer = CountVectorizer(tokenizer=LemNormalize, stop_words='english')
    tfidf = vectorizer.fit_transform(sentence_tokens)
    
    # Compute similarity
    cosine_vals = cosine_similarity(tfidf[-1], tfidf)
    idx = cosine_vals.argsort()[0][-2]
    flat = cosine_vals.flatten()
    flat.sort()
    req_tfidf = flat[-2]
    
    sentence_tokens.pop(-1)
    
    if req_tfidf == 0:
        return "I am sorry! I don't understand you."
    else:
        return sentence_tokens[idx]

# Chatbot function
def chatbot():
    print("Chatbot: Hello! How can I assist you? Type 'bye' to exit.")
    
    while True:
        user_response = input("You: ")
        user_response = user_response.lower()
        
        if user_response != 'bye':
            if user_response in ['thanks', 'thank you']:
                print("Chatbot: You're welcome!")
                break
            else:
                if greeting(user_response) is not None:
                    print("Chatbot:", greeting(user_response))
                else:
                    print("Chatbot:", response(user_response))
        else:
            print("Chatbot: Goodbye! Have a great day!")
            break

# Start the chatbot
chatbot()
