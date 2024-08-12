import json
import random
import numpy as np
import pickle
import tensorflow
from keras.optimizers import SGD
from keras.layers import Dense, Activation, Dropout
from keras.models import Sequential
import nltk
from Sastrawi.Stemmer.StemmerFactory import StemmerFactory
# from nltk.stem import WordNetLemmatizer


def update_nltk():
    # nltk.download('wordnet')
    nltk.download('popular')
    nltk.download('punkt')


def exec_training_bot():
    update_nltk()
    # lemmatizer = WordNetLemmatizer()
    factory = StemmerFactory()
    stemmer = factory.create_stemmer()

    pattern = []
    tag = []
    clasify = []

    JSON_FILE = open('dataset/main-dataset.json').read()
    intents = json.loads(JSON_FILE)

    for intent in intents['intents']:
        for JSON_Pattern in intent['patterns']:
            tokenize_pattern = nltk.word_tokenize(JSON_Pattern)
            pattern.extend(tokenize_pattern)
            clasify.append((tokenize_pattern, intent['class']))
            if intent['class'] not in tag:
                tag.append(intent['class'])

    pattern = [
        stemmer.stem(tokenize_pattern.lower()) for tokenize_pattern in pattern
    ]

    pattern = sorted(list(set(pattern)))
    tag = sorted(list(set(tag)))

    pickle.dump(pattern, open('./dataset/pattern.pkl', 'wb'))
    pickle.dump(tag, open('./dataset/class.pkl', 'wb'))
    training = []
    output_empty = [0] * len(tag)

    for b in clasify:
        bag = []
        pattern_words = b[0]
        pattern_words = [
            stemmer.stem(word.lower()) for word in pattern_words
        ]
        for c in pattern:
            bag.append(1) if c in pattern_words else bag.append(0)
        output_row = list(output_empty)
        output_row[tag.index(b[1])] = 1
        training.append([bag, output_row])

    random.shuffle(training)
    training = np.array(training, dtype=object)
    train_x = list(training[:, 0])
    train_y = list(training[:, 1])

    model = Sequential()
    model.add(Dense(160, input_shape=(len(train_x[0]), ), activation='relu'))
    model.add(Dense(80, activation='relu'))
    model.add(Dropout(0.5))
    model.add(Dense(len(train_y[0]), activation='softmax'))
    gradientDescent = SGD(learning_rate=0.01,
                          momentum=0.9)
    model.compile(loss='categorical_crossentropy',
                  optimizer=gradientDescent,
                  metrics=['accuracy'])

    # model created and save into h5 file
    model.save('./dataset/annmodel.h5', model.fit(np.array(train_x), np.array(
        train_y), epochs=200, verbose=1))


# exec_training_bot()
