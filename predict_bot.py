# import wikipedia
from keras.models import load_model
import tensorflow
import random
import numpy as np
import pickle
import json
import nltk
from nltk.stem import WordNetLemmatizer
import re
from Sastrawi.Stemmer.StemmerFactory import StemmerFactory

# lemmatizer = WordNetLemmatizer()
# wikipedia.set_lang("ID")
factory = StemmerFactory()
stemmer = factory.create_stemmer()

ANNmodel = load_model('./dataset/annmodel.h5')
JSONanswer = json.loads(open('./dataset/main-dataset.json').read())

pattern = pickle.load(open('./dataset/pattern.pkl', 'rb'))
classes = pickle.load(open('./dataset/class.pkl', 'rb'))


def clear_sentence(userInput):
    regex_pattern = "[^0-9a-zA-Z\s+]"

    clean_string = re.sub(regex_pattern, "", userInput)
    arr_tokenize = nltk.word_tokenize(clean_string)

    input_tokenized = [
        stemmer.stem(a.lower()) for a in arr_tokenize
    ]
    return input_tokenized


def matrixBag(userInput, pattern, show_details=True):

    input_tokenized = clear_sentence(userInput)

    bag = [0] * len(pattern)
    for b in input_tokenized:
        for c, d in enumerate(pattern):
            if d == b:
                # match vocab position in matrix
                bag[c] = 1
    return (np.array(bag))


def msgPredict(userInput, ANNmodel):
    bag = matrixBag(userInput, pattern, show_details=False)

    predict_array = ANNmodel.predict(np.array([bag]))[0]

    results = [[i, r] for i, r in enumerate(predict_array) if r > 0.1]

    # sort by strength of probability
    results.sort(key=lambda x: x[1], reverse=True)
    result_list = []
    for r in results:
        result_list.append(
            {"class": classes[r[0]], "probability": float(r[1])})

    return result_list


def botAnswer(ints, intents_json, userInput):
    tag = ints[0]['class']
    probability = ints[0]['probability']
    print(probability)
    print(tag)
    list_of_intents = intents_json['intents']

    for i in list_of_intents:
        if (i['class'] == tag):
            if (probability) < 0.3:
                result = 'Maaf, Tolong Lebih Perjelas Pertanyaan Atau Keyword'
                break
            else:
                result = random.choice(i['responses'])
                break

    return result


def botResponse(userInput):
    predict = msgPredict(userInput, ANNmodel)
    answer = botAnswer(predict, JSONanswer, userInput)

    return answer
