import random
import json
import pickle
import numpy as np
import nltk
from sklearn.metrics.pairwise import cosine_similarity
from nltk.stem import WordNetLemmatizer
from keras.models import load_model
import speech_recognition as sr


def listen_to_microphone():
    recognizer = sr.Recognizer()
    mic = sr.Microphone()

    with mic as source:
        print("Listening... (say something)")
        recognizer.adjust_for_ambient_noise(source)  # reduce noise
        audio = recognizer.listen(source)

    try:
        print("Recognizing...")
        text = recognizer.recognize_google(audio)
        print(f"You said: {text}")
        return text
    except sr.UnknownValueError:
        print("Sorry, I could not understand your speech.")
        return None
    except sr.RequestError as e:
        print(f"Could not request results; {e}")
        return None


# Download NLTK data if not already present
nltk.download('punkt')
nltk.download('wordnet')

lemmatizer = WordNetLemmatizer()
intents = json.loads(open('intents.json').read())

words = pickle.load(open('words.pkl', 'rb'))
classes = pickle.load(open('classes.pkl', 'rb'))
model = load_model('chatbot_model.h5')

def clean_up_sentence(sentence):
    sentence_words = nltk.word_tokenize(sentence)
    sentence_words = [lemmatizer.lemmatize(word.lower()) for word in sentence_words]
    return sentence_words

def bag_of_words(sentence):
    sentence_words = clean_up_sentence(sentence)
    bag = [0] * len(words)
    for w in sentence_words:
        for i, word in enumerate(words):
            if word == w:
                bag[i] = 1
    return np.array(bag)

def predict_class(sentence):
    bow = bag_of_words(sentence)
    res = model.predict(np.array([bow]))[0]
    ERROR_THRESHOLD = 0.25
    # print(bow)
    # print(res)
    results = [[i, r] for i, r in enumerate(res) if r > ERROR_THRESHOLD]
    results.sort(key=lambda x: x[1], reverse=True)
    # print(results)
    return_list = []
    for r in results:
        return_list.append({'intent': classes[r[0]], 'probability': str(r[1])})
    # print(return_list)
    return return_list

def get_response(intents_list, intents_json):
    tag = intents_list[0]['intent']
    list_of_intents = intents_json['intents']
    for i in list_of_intents:
        if i['tag'] == tag:
            result = random.choice(i['responses'])
            break
    return result

def cosine_intent(sentence, intents_json, words):
    sentence_vec = bag_of_words(sentence)
    if np.sum(sentence_vec) == 0:
        return None, 0  # No overlap, skip cosine similarity
    max_sim = 0
    best_tag = None
    for intent in intents_json['intents']:
        for pattern in intent['patterns']:
            pattern_vec = bag_of_words(pattern)
            sim = cosine_similarity([sentence_vec], [pattern_vec])[0][0]
            if sim > max_sim:
                max_sim = sim
                best_tag = intent['tag']
    return best_tag, max_sim

# print("GO! Bot is running!")
#
# while True:
#     # mode = input("Type 'voice' to talk or 'text' to type: ").strip().lower()
#     # if mode == "voice":
#     #     message = listen_to_microphone()
#     #     if not message:
#     #         continue  # if no speech recognized, skip to next loop
#     # else:
#     message = input("You: ")
#
#     ints = predict_class(message)
#     if ints:
#         res = get_response(ints, intents)
#         print(res)
#     else:
#         tag, sim = cosine_intent(message, intents, words)
#         if tag is not None and sim > 0.7:  # Lowered threshold
#             for i in intents['intents']:
#                 if i['tag'] == tag:
#                     print(random.choice(i['responses']))
#                     break
#         else:
#             print("Sorry, I didn't understand that.")