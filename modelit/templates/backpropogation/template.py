# =========================================================
# BACKPROPAGATION FROM SCRATCH
# XOR using SGD
# Xavier Initialization
# Titanic Dataset using MLPClassifier
# =========================================================


# =========================================================
# IMPORTS
# =========================================================

import numpy as np
import pandas as pd

from sklearn.model_selection import train_test_split
from sklearn.neural_network import MLPClassifier
from sklearn.preprocessing import StandardScaler


# =========================================================
# ACTIVATION FUNCTION
# SIGMOID
# =========================================================

def activation_func(net):

    return 1 / (1 + np.exp(-net))


# =========================================================
# ERROR FUNCTION
# E = 1/2 (d - o)^2
# =========================================================

def calc_error(output, det_output):

    return (1 / 2) * (det_output - output) ** 2


# =========================================================
# FORWARD PASS
#
# Architecture:
# 2 Input Neurons
# 2 Hidden Neurons
# 1 Output Neuron
# =========================================================

def forward_pass(x_input, weights, biases):

    # Hidden Neuron h0
    net_h0 = (
        (x_input[0] * weights[0]) +
        (x_input[1] * weights[1]) +
        biases[0]
    )

    outh0 = activation_func(net_h0)

    # Hidden Neuron h1
    net_h1 = (
        (x_input[0] * weights[2]) +
        (x_input[1] * weights[3]) +
        biases[1]
    )

    outh1 = activation_func(net_h1)

    # Output Neuron
    net_o0 = (
        (outh0 * weights[4]) +
        (outh1 * weights[5]) +
        biases[2]
    )

    out_o0 = activation_func(net_o0)

    return outh0, outh1, out_o0


# =========================================================
# BACKWARD PASS
# =========================================================

def backward_pass(
    x_input,
    weights,
    biases,
    desired_output,
    learning_rate,
    outh0,
    outh1,
    out_o0
):

    # Output layer delta
    delta_o0 = (
        (desired_output - out_o0) *
        out_o0 *
        (1 - out_o0)
    )

    # Hidden layer deltas
    delta_h0 = (
        delta_o0 *
        weights[4] *
        outh0 *
        (1 - outh0)
    )

    delta_h1 = (
        delta_o0 *
        weights[5] *
        outh1 *
        (1 - outh1)
    )

    # Weight updates
    dw0 = learning_rate * delta_h0 * x_input[0]
    dw1 = learning_rate * delta_h0 * x_input[1]

    dw2 = learning_rate * delta_h1 * x_input[0]
    dw3 = learning_rate * delta_h1 * x_input[1]

    dw4 = learning_rate * delta_o0 * outh0
    dw5 = learning_rate * delta_o0 * outh1

    dw_values = [dw0, dw1, dw2, dw3, dw4, dw5]

    # Bias updates
    db0 = learning_rate * delta_h0
    db1 = learning_rate * delta_h1
    db2 = learning_rate * delta_o0

    db_values = [db0, db1, db2]

    return dw_values, db_values


# =========================================================
# XOR DATASET
# =========================================================

x1 = [0, 0]
x2 = [0, 1]
x3 = [1, 0]
x4 = [1, 1]

y = [0, 1, 1, 0]

X = [x1, x2, x3, x4]
d = y


# =========================================================
# INITIAL WEIGHTS AND BIASES
# =========================================================

w = [0.5, -0.3, 0.8, 0.2, 0.6, -0.5]

b = [0.2, -0.4, 0.3]

learning_rate_initial = 0.01

epochs = 2000

error_threshold = 0.001


# =========================================================
# TRAINING USING SGD
# =========================================================

def train_SGD(
    X_data,
    y_data,
    epochs_count,
    lr_val,
    initial_weights_list,
    initial_biases_list
):

    w1, w2, w3, w4, w5, w6 = (
        initial_weights_list[0],
        initial_weights_list[1],
        initial_weights_list[2],
        initial_weights_list[3],
        initial_weights_list[4],
        initial_weights_list[5]
    )

    b1, b2, b3 = (
        initial_biases_list[0],
        initial_biases_list[1],
        initial_biases_list[2]
    )

    for epoch in range(epochs_count):

        total_loss = 0

        for i in range(len(X_data)):

            x_input = X_data[i]

            target = y_data[i]

            current_weights = [w1, w2, w3, w4, w5, w6]

            current_biases = [b1, b2, b3]

            # Forward pass
            outh0, outh1, out_o0 = forward_pass(
                x_input,
                current_weights,
                current_biases
            )

            # Loss
            current_loss = calc_error(out_o0, target)

            total_loss += current_loss

            # Backpropagation
            dw_values, db_values = backward_pass(
                x_input,
                current_weights,
                current_biases,
                target,
                lr_val,
                outh0,
                outh1,
                out_o0
            )

            # Update weights
            w1 += dw_values[0]
            w2 += dw_values[1]
            w3 += dw_values[2]
            w4 += dw_values[3]
            w5 += dw_values[4]
            w6 += dw_values[5]

            # Update biases
            b1 += db_values[0]
            b2 += db_values[1]
            b3 += db_values[2]

        # Print every 100 epochs
        if epoch % 100 == 0 or total_loss < error_threshold:

            print(f"\nEpoch {epoch}")

            print(f"Total Error = {total_loss:.6f}")

            output_example = forward_pass(
                X_data[0],
                [w1, w2, w3, w4, w5, w6],
                [b1, b2, b3]
            )[2]

            print(
                f"Output for input {X_data[0]} : "
                f"{output_example:.4f}"
            )

        # Early stopping
        if total_loss < error_threshold:

            print(
                f"\nStopping condition met at epoch "
                f"{epoch + 1}"
            )

            print(
                f"Total Error ({total_loss:.6f}) "
                f"<= Threshold ({error_threshold:.6f})"
            )

            break

    updated_weights = [w1, w2, w3, w4, w5, w6]

    updated_biases = [b1, b2, b3]

    return updated_weights, updated_biases


# =========================================================
# TRAIN XOR NETWORK
# =========================================================

updated_w, updated_b = train_SGD(
    X,
    d,
    epochs,
    learning_rate_initial,
    w,
    b
)


# =========================================================
# FINAL WEIGHTS
# =========================================================

print("\nFinal Updated Weights:")

for i, weight in enumerate(updated_w):

    print(f"w{i + 1} = {weight:.4f}")


# =========================================================
# FINAL BIASES
# =========================================================

print("\nFinal Updated Biases:")

for i, bias in enumerate(updated_b):

    print(f"b{i + 1} = {bias:.4f}")


# =========================================================
# TEST XOR OUTPUTS
# =========================================================

print("\n=================================================")
print("XOR Predictions")
print("=================================================")

for i in range(len(X)):

    _, _, prediction = forward_pass(
        X[i],
        updated_w,
        updated_b
    )

    print(
        f"Input: {X[i]} "
        f"Target: {d[i]} "
        f"Prediction: {prediction:.4f}"
    )


# =========================================================
# XAVIER INITIALIZATION
# =========================================================

print("\n=================================================")
print("Xavier Initialization")
print("=================================================")

nin = 2
nhidden = 2
nout = 1


def xavier(nin, nout):

    limit = np.sqrt(6 / (nin + nout))

    return np.random.uniform(
        -limit,
        limit,
        (nin, nout)
    )


w1_xavier = xavier(nin, nhidden)

w2_xavier = xavier(nhidden, nout)

print("\nWeights between Input -> Hidden:")
print(w1_xavier)

print("\nWeights between Hidden -> Output:")
print(w2_xavier)


# =========================================================
# TITANIC DATASET USING MLPClassifier
# =========================================================

print("\n=================================================")
print("Titanic Dataset using MLPClassifier")
print("=================================================")

# Dataset loading
# Install:
# pip install kagglehub

import kagglehub

path = kagglehub.dataset_download(
    "yasserh/titanic-dataset"
)

print("\nPath to dataset files:")
print(path)


# =========================================================
# LOAD DATASET
# =========================================================

df = pd.read_csv(f"{path}/Titanic-Dataset.csv")

print("\nDataset Head:")
print(df.head())


# =========================================================
# FEATURES AND LABELS
# =========================================================

y_titanic = df["Survived"]

X_titanic = df.drop(
    columns=[
        "Survived",
        "Name",
        "Ticket",
        "Cabin"
    ]
)


# =========================================================
# ENCODE SEX COLUMN
# =========================================================

X_titanic["Sex"] = X_titanic["Sex"].map(
    {
        "male": 0,
        "female": 1
    }
)


# =========================================================
# ONE HOT ENCODING
# =========================================================

X_titanic = pd.get_dummies(
    X_titanic,
    columns=["Embarked"],
    drop_first=True
)


# =========================================================
# HANDLE MISSING VALUES
# =========================================================

X_titanic = X_titanic.fillna(
    X_titanic.mean()
)


# =========================================================
# FEATURE SCALING
# =========================================================

scaler = StandardScaler()

X_scaled = scaler.fit_transform(X_titanic)


# =========================================================
# TRAIN TEST SPLIT
# =========================================================

X_train, X_test, y_train, y_test = train_test_split(
    X_scaled,
    y_titanic,
    test_size=0.2,
    random_state=42
)


# =========================================================
# MLP MODEL
# =========================================================

mlp = MLPClassifier(
    hidden_layer_sizes=(10,),
    activation="logistic",
    solver="sgd",
    learning_rate_init=0.01,
    random_state=42,
    max_iter=2000
)


# =========================================================
# TRAIN MODEL
# =========================================================

mlp.fit(X_train, y_train)


# =========================================================
# PRINT WEIGHTS
# =========================================================

print("\nWeights (Coefficients):")

for i, coef in enumerate(mlp.coefs_):

    print(f"\nLayer {i} weights:\n")

    print(coef)


# =========================================================
# PRINT BIASES
# =========================================================

print("\nBiases (Intercepts):")

for i, intercept in enumerate(mlp.intercepts_):

    print(f"\nLayer {i} biases:\n")

    print(intercept)


# =========================================================
# MODEL ACCURACY
# =========================================================

accuracy = mlp.score(X_test, y_test)

print("\n=================================================")
print(f"Model Accuracy: {accuracy * 100:.2f}%")
print("=================================================")