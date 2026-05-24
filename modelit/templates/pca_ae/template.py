# =========================================================
# DIMENSIONALITY REDUCTION COMPARISON: PCA VS AUTOENCODER
# Uses MNIST Dataset
# Reconstructs Data down to 32 Dimensions
# =========================================================


# =========================================================
# IMPORTS
# =========================================================

import numpy as np

from sklearn.decomposition import PCA
from sklearn.metrics import mean_squared_error

from tensorflow.keras.datasets import mnist
from tensorflow.keras.models import Model

from tensorflow.keras.layers import (
    Input, 
    Dense
)


# =========================================================
# LOAD MNIST DATASET
# =========================================================

(x_train_mnist, _), (x_test_mnist, _) = mnist.load_data()


# =========================================================
# RESHAPE & NORMALIZE IMAGES
# =========================================================

x_train_mnist = x_train_mnist.reshape(
    (len(x_train_mnist), np.prod(x_train_mnist.shape[1:]))
)

x_test_mnist = x_test_mnist.reshape(
    (len(x_test_mnist), np.prod(x_test_mnist.shape[1:]))
)

x_train_mnist = x_train_mnist.astype('float32') / 255.0

x_test_mnist = x_test_mnist.astype('float32') / 255.0


print("\n=================================================")
print("MNIST Dataset Dimensionality Shape:")
print("=================================================")

print(f"MNIST Training Data Shape: {x_train_mnist.shape}")

print(f"MNIST Testing Data Shape:  {x_test_mnist.shape}")


# =========================================================
# PRINCIPAL COMPONENT ANALYSIS (PCA)
# Reduces Dimensions from 784 down to 32
# =========================================================

pca_mnist = PCA(n_components=32)

x_train_pca_reduced = pca_mnist.fit_transform(x_train_mnist)

x_test_pca_reduced = pca_mnist.transform(x_test_mnist)


# =========================================================
# PCA INVERSE RECONSTRUCTION
# =========================================================

x_test_pca_reconstructed = pca_mnist.inverse_transform(
    x_test_pca_reduced
)


# =========================================================
# PCA EVALUATION (MEAN SQUARED ERROR)
# =========================================================

mse_pca_mnist = mean_squared_error(
    x_test_mnist, 
    x_test_pca_reconstructed
)


print("\n=================================================")
print("PCA REDUCTION & RECONSTRUCTION RESULTS")
print("=================================================")

print(f"Reduced Dimensions Shape:   {x_test_pca_reduced.shape}")

print(f"Reconstructed Data Shape:  {x_test_pca_reconstructed.shape}")

print(f"PCA Reconstruction MSE:    {mse_pca_mnist:.6f}")


# =========================================================
# AUTOENCODER MODEL ARCHITECTURE
# 784 Input -> 128 Hidden -> 32 Latent -> 128 Hidden -> 784 Output
# =========================================================

input_dim_mnist = x_train_mnist.shape[1]

input_layer_mnist = Input(shape=(input_dim_mnist,))


# =========================================================
# ENCODER STAGE
# =========================================================

hidden_enc_mnist = Dense(
    128, 
    activation='sigmoid'
)(input_layer_mnist)

latent_mnist = Dense(
    32, 
    activation='sigmoid'
)(hidden_enc_mnist)


# =========================================================
# DECODER STAGE
# =========================================================

hidden_dec_mnist = Dense(
    128, 
    activation='sigmoid'
)(latent_mnist)

output_layer_mnist = Dense(
    input_dim_mnist, 
    activation='sigmoid'
)(hidden_dec_mnist)


# =========================================================
# BUILD AUTOENCODER MODEL
# =========================================================

autoencoder_mnist = Model(
    inputs=input_layer_mnist, 
    outputs=output_layer_mnist
)


# =========================================================
# COMPILE AUTOENCODER
# =========================================================

autoencoder_mnist.compile(
    optimizer='adam',
    loss='binary_crossentropy'
)


print("\n=================================================")
print("Autoencoder Architecture Details:")
print("=================================================")

autoencoder_mnist.summary()


# =========================================================
# TRAIN AUTOENCODER
# =========================================================

print("\nTraining Autoencoder on MNIST dataset...")

history_mnist = autoencoder_mnist.fit(
    x_train_mnist, 
    x_train_mnist,
    epochs=20,
    batch_size=256,
    validation_data=(x_test_mnist, x_test_mnist),
    verbose=0
)

print("Autoencoder training complete.")


# =========================================================
# AUTOENCODER RECONSTRUCTION
# =========================================================

x_test_autoencoder_reconstructed = autoencoder_mnist.predict(
    x_test_mnist
)


# =========================================================
# AUTOENCODER EVALUATION (MEAN SQUARED ERROR)
# =========================================================

mse_autoencoder_mnist = mean_squared_error(
    x_test_mnist, 
    x_test_autoencoder_reconstructed
)


print("\n=================================================")
print("AUTOENCODER REDUCTION & RECONSTRUCTION RESULTS")
print("=================================================")

print(f"Reconstructed Data Shape:  {x_test_autoencoder_reconstructed.shape}")

print(f"Autoencoder Reconstructed MSE: {mse_autoencoder_mnist:.6f}")


# =========================================================
# FINAL COMPARISON SUMMARY
# =========================================================

print("\n=================================================")
print("FINAL DIMENSIONALITY REDUCTION COMPARISON (32 DIM)")
print("=================================================")

print(f"PCA Reconstruction MSE:         {mse_pca_mnist:.6f}")

print(f"Autoencoder Reconstruction MSE: {mse_autoencoder_mnist:.6f}")

print("=================================================")