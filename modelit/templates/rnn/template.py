# =========================================================
# SIMPLE RNN FOR SENTIMENT ANALYSIS
# Implementation on Custom Dataset & Built-in IMDB Dataset
# No Kaggle Download Needed
# =========================================================


# =========================================================
# IMPORTS
# =========================================================

import random
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from sklearn.model_selection import train_test_split
from sklearn.metrics import (
    accuracy_score, 
    precision_score, 
    recall_score, 
    f1_score
)

from tensorflow.keras.models import Sequential

from tensorflow.keras.layers import (
    Embedding, 
    SimpleRNN, 
    Dense
)

from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.datasets import imdb


# =========================================================
# CUSTOM DATASET GENERATION
# =========================================================

positive_sentences = [
    "I love this product",
    "This movie was amazing",
    "The service was excellent",
    "I am very happy",
    "Fantastic experience",
    "Great quality",
    "Absolutely wonderful",
    "I enjoyed it",
    "Highly recommended",
    "Best purchase",
    "Very satisfying",
    "This made my day",
    "Superb performance",
    "I really like it",
    "Outstanding work",
    "It works perfectly",
    "Great support",
    "Very impressive",
    "Loved it",
    "Worth the money"
]

negative_sentences = [
    "I hate this product",
    "This movie was terrible",
    "The service was awful",
    "I am very disappointed",
    "Worst experience",
    "Poor quality",
    "Absolutely horrible",
    "I regret buying this",
    "Not recommended",
    "Waste of money",
    "Very unsatisfying",
    "This ruined my day",
    "Bad performance",
    "I dislike it",
    "Terrible work",
    "It does not work",
    "Very bad support",
    "Not impressive",
    "I hated it",
    "Totally useless"
]

data = []

for _ in range(300):

    data.append([random.choice(positive_sentences), "positive"])

    data.append([random.choice(negative_sentences), "negative"])


df = pd.DataFrame(data, columns=["text", "sentiment"])

print("\n=================================================")
print("Custom Dataset Sample Head:")
print("=================================================")
print(df.head())


# =========================================================
# PREPROCESSING CUSTOM DATASET
# =========================================================

df["sentiment"] = df["sentiment"].map({
    "positive": 1,
    "negative": 0
})

labels = df["sentiment"].values

tokenizer = Tokenizer(num_words=1000)

tokenizer.fit_on_texts(df["text"])

sequences = tokenizer.texts_to_sequences(df["text"])

X_custom = pad_sequences(sequences, maxlen=10)

y_custom = labels


# =========================================================
# TRAIN TEST SPLIT (CUSTOM DATASET)
# =========================================================

X_train_custom, X_test_custom, y_train_custom, y_test_custom = train_test_split(

    X_custom,
    y_custom,

    test_size=0.25,

    random_state=42

)

print("\nCustom Train Samples:", X_train_custom.shape)

print("Custom Test Samples:", X_test_custom.shape)


# =========================================================
# CREATE SIMPLE RNN MODEL (CUSTOM DATASET)
# =========================================================

rnn_custom = Sequential([

    Embedding(
        4000,
        32,
        input_length=10
    ),

    SimpleRNN(
        128,
        activation="tanh"
    ),

    Dense(
        1,
        activation="sigmoid"
    )

])


# =========================================================
# COMPILE & TRAIN RNN (CUSTOM DATASET)
# =========================================================

rnn_custom.compile(

    optimizer="adam",

    loss="binary_crossentropy",

    metrics=["accuracy"]

)

print("\n=================================================")
print("RNN Custom Model Architecture:")
print("=================================================")
rnn_custom.summary()

history_rnn_custom = rnn_custom.fit(

    X_train_custom,
    y_train_custom,

    epochs=20,

    validation_data=(X_test_custom, y_test_custom),

    verbose=1

)


# =========================================================
# EVALUATION UTILITIES
# =========================================================

def evaluate_model(model, X_test, y_test, model_name):

    y_pred_prob = model.predict(X_test)

    y_pred = (y_pred_prob > 0.5).astype(int)

    accuracy = accuracy_score(y_test, y_pred)

    precision = precision_score(y_test, y_pred)

    recall = recall_score(y_test, y_pred)

    f1 = f1_score(y_test, y_pred)

    print(f"\n--- {model_name} Performance ---")

    print(f"Accuracy:  {accuracy:.4f}")

    print(f"Precision: {precision:.4f}")

    print(f"Recall:    {recall:.4f}")

    print(f"F1 Score:  {f1:.4f}")

    return y_pred


def predict_samples(model, tokenizer, texts):

    seqs = tokenizer.texts_to_sequences(texts)

    padded = pad_sequences(seqs, maxlen=10)

    preds = model.predict(padded)

    for text, score in zip(texts, preds):

        sentiment = "Positive" if score > 0.5 else "Negative"

        print(f"Text: '{text}' -> Sentiment: {sentiment} ({score[0]:.4f})")

    print()


# =========================================================
# CUSTOM DATASET PREDICTIONS & EVALUATION
# =========================================================

sample_texts = [
    "This is a fantastic product",
    "I really hated the service",
    "It was an okay experience"
]

print("\n=================================================")
print("Evaluating Sample Text Predictions:")
print("=================================================")

print("RNN Model Predictions:")
predict_samples(rnn_custom, tokenizer, sample_texts)

print("\n=================================================")
print("Custom Dataset Simple RNN Performance:")
print("=================================================")

y_pred_rnn_custom = evaluate_model(
    rnn_custom, 
    X_test_custom, 
    y_test_custom, 
    "Simple RNN"
)


# =========================================================
# LOAD IMDB DATASET
# =========================================================

print("\n=================================================")
print("LOADING NATIVE IMDB DATASET")
print("=================================================")

vocab_size = 10000

(X_train_imdb, y_train_imdb), (X_test_imdb, y_test_imdb) = imdb.load_data(
    num_words=vocab_size
)

print("\nIMDb Training samples:", len(X_train_imdb))

print("IMDb Testing samples:", len(X_test_imdb))


# =========================================================
# PREPROCESSING IMDB DATASET
# =========================================================

max_len = 200

X_train_imdb = pad_sequences(X_train_imdb, maxlen=max_len)

X_test_imdb = pad_sequences(X_test_imdb, maxlen=max_len)

print("\nShape of training data after padding:", X_train_imdb.shape)

print("Shape of testing data after padding:", X_test_imdb.shape)


# =========================================================
# CREATE SIMPLE RNN MODEL (IMDB)
# =========================================================

rnn_imdb = Sequential([

    Embedding(
        input_dim=vocab_size,
        output_dim=32,
        input_length=max_len
    ),

    SimpleRNN(
        64,
        activation='tanh'
    ),

    Dense(
        1,
        activation='sigmoid'
    )

])


# =========================================================
# COMPILE & TRAIN RNN (IMDB)
# =========================================================

rnn_imdb.compile(

    optimizer='adam',

    loss='binary_crossentropy',

    metrics=['accuracy']

)

print("\n=================================================")
print("RNN IMDb Model Architecture:")
print("=================================================")
rnn_imdb.summary()

history_rnn_imdb = rnn_imdb.fit(

    X_train_imdb,
    y_train_imdb,

    epochs=5,

    batch_size=64,

    validation_split=0.2,

    verbose=1

)


# =========================================================
# EVALUATE RNN (IMDB)
# =========================================================

rnn_loss, rnn_acc = rnn_imdb.evaluate(
    X_test_imdb, 
    y_test_imdb,
    verbose=0
)

print("\n=================================================")
print("FINAL RESULTS")
print("=================================================")

print(f"Simple RNN Test Accuracy on IMDb: {rnn_acc:.4f}")

print("=================================================")