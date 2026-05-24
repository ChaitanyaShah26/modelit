# =========================================================
# LSTM FOR SENTIMENT ANALYSIS
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
    LSTM, 
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
# CREATE LSTM MODEL (CUSTOM DATASET)
# =========================================================

lstm_custom = Sequential([

    Embedding(
        4000,
        32,
        input_length=10
    ),

    LSTM(
        64
    ),

    Dense(
        1,
        activation="sigmoid"
    )

])


# =========================================================
# COMPILE & TRAIN LSTM (CUSTOM DATASET)
# =========================================================

lstm_custom.compile(

    optimizer="adam",

    loss="binary_crossentropy",

    metrics=["accuracy"]

)

print("\n=================================================")
print("LSTM Custom Model Architecture:")
print("=================================================")
lstm_custom.summary()

history_lstm_custom = lstm_custom.fit(

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

print("LSTM Model Predictions:")
predict_samples(lstm_custom, tokenizer, sample_texts)

print("\n=================================================")
print("Custom Dataset LSTM Performance:")
print("=================================================")

y_pred_lstm_custom = evaluate_model(
    lstm_custom, 
    X_test_custom, 
    y_test_custom, 
    "LSTM"
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
# CREATE LSTM MODEL (IMDB)
# =========================================================

lstm_imdb = Sequential([

    Embedding(
        input_dim=vocab_size,
        output_dim=32,
        input_length=max_len
    ),

    LSTM(
        64
    ),

    Dense(
        1,
        activation='sigmoid'
    )

])


# =========================================================
# COMPILE & TRAIN LSTM (IMDB)
# =========================================================

lstm_imdb.compile(

    optimizer='adam',

    loss='binary_crossentropy',

    metrics=['accuracy']

)

print("\n=================================================")
print("LSTM IMDb Model Architecture:")
print("=================================================")
lstm_imdb.summary()

history_lstm_imdb = lstm_imdb.fit(

    X_train_imdb,
    y_train_imdb,

    epochs=5,

    batch_size=64,

    validation_split=0.2,

    verbose=1

)


# =========================================================
# EVALUATE LSTM (IMDB)
# =========================================================

lstm_loss, lstm_acc = lstm_imdb.evaluate(
    X_test_imdb, 
    y_test_imdb,
    verbose=0
)

print("\n=================================================")
print("FINAL RESULTS")
print("=================================================")

print(f"LSTM Test Accuracy on IMDb: {lstm_acc:.4f}")

print("=================================================")