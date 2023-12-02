import random
import json
import pickle
import numpy as np
import spacy
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Dropout
from tensorflow.keras.optimizers import SGD

# Once you edit your intents in intents.json, run this file to retrain the model.
# This file will create a words.pkl and classes.pkl file in the core/training/intents folder.
# It will also create a squire_assistant.keras file in the same folder.

nlp = spacy.load("en_core_web_sm")

# Load intents.json file
intents = json.loads(open("core/training/intents/intents.json").read())

words = []
classes = []
documents = []
ignore_characters = ["?", "!", ".", ","]

# Tokenize and sort by tag
for intent in intents["intents"]:
    for pattern in intent["patterns"]:
        word_list = []

        for i in nlp(pattern):
            word_list.append(i.text)

        words.extend(word_list)
        documents.append((word_list, intent["tag"]))
        if intent["tag"] not in classes:
            classes.append(intent["tag"])

words = [token.lemma_ for token in nlp(
    " ".join(words)) if token.text not in ignore_characters]
words = sorted(set(words))

pickle.dump(words, open("core/training/intents/words.pkl", "wb"))
pickle.dump(classes, open("core/training/intents/classes.pkl", "wb"))

# Training
training = []
output_empty = [0] * len(classes)

for document in documents:
    bag = []
    word_patterns = document[0]
    word_patterns = [token.lemma_.lower()
                     for doc in nlp.pipe(word_patterns) for token in doc]
    for word in words:
        bag.append(1) if word in word_patterns else bag.append(0)

    output_row = list(output_empty)
    output_row[classes.index(document[1])] = 1
    training.append(bag + output_row)

random.shuffle(training)
training = np.array(training)

train_x = training[:, : len(words)]
train_y = training[:, len(words):]

model = Sequential()
model.add(Dense(128, input_shape=(len(train_x[0]),), activation="relu"))
model.add(Dropout(0.5))
model.add(Dense(64, activation="relu"))
model.add(Dropout(0.5))
model.add(Dense(len(train_y[0]), activation="softmax"))

sgd = SGD(learning_rate=0.01, momentum=0.9, nesterov=True)
model.compile(loss="categorical_crossentropy",
              optimizer=sgd, metrics=["accuracy"])

mdl = model.fit(train_x, train_y, epochs=200, batch_size=5, verbose=1)
model.save("core/training/intents/squire_assistant.keras", mdl)
