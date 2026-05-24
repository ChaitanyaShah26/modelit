# =========================================================
# VARIATIONAL AUTOENCODER (VAE) ON MNIST
# Latent Space Exploration and Reconstruction
# No Kaggle Download Needed
# =========================================================


# =========================================================
# IMPORTS
# =========================================================

import numpy as np
import matplotlib.pyplot as plt
import tensorflow as tf

from tensorflow.keras import layers, Model
from tensorflow.keras.datasets import mnist

from sklearn.metrics import mean_squared_error


# =========================================================
# LOAD MNIST DATASET
# =========================================================

(x_train_mnist, _), (x_test_mnist, _) = mnist.load_data()


# =========================================================
# RESHAPE & NORMALIZE IMAGES
# =========================================================

x_train_mnist = x_train_mnist.astype("float32") / 255.0

x_test_mnist = x_test_mnist.astype("float32") / 255.0

x_train_mnist = x_train_mnist.reshape(-1, 784)

x_test_mnist = x_test_mnist.reshape(-1, 784)


print("\n=================================================")
print("MNIST Dataset Dimensionality Shape:")
print("=================================================")

print("MNIST Training Data Shape:", x_train_mnist.shape)

print("MNIST Testing Data Shape: ", x_test_mnist.shape)


# =========================================================
# MODEL HYPERPARAMETERS
# =========================================================

input_dim_mnist = 784

hidden_dim1_mnist = 64

hidden_dim2_mnist = 4

latent_dim_mnist = 2


# =========================================================
# REPARAMETERIZATION TRICK (SAMPLING LAYER)
# =========================================================

def sampling_mnist(args):

    z_mean, z_log_var = args

    batch = tf.shape(z_mean)[0]

    dim = tf.shape(z_mean)[1]

    epsilon = tf.random.normal(shape=(batch, dim))

    return z_mean + tf.exp(0.5 * z_log_var) * epsilon


# =========================================================
# ENCODER ARCHITECTURE
# =========================================================

encoder_inputs_mnist = layers.Input(shape=(input_dim_mnist,))

h1_mnist = layers.Dense(
    hidden_dim1_mnist, 
    activation='relu'
)(encoder_inputs_mnist)

h2_mnist = layers.Dense(
    hidden_dim2_mnist, 
    activation='relu'
)(h1_mnist)

z_mean_mnist = layers.Dense(
    latent_dim_mnist, 
    name="z_mean"
)(h2_mnist)

z_log_var_mnist = layers.Dense(
    latent_dim_mnist, 
    name="z_log_var"
)(h2_mnist)

z_mnist = layers.Lambda(
    sampling_mnist, 
    name="z"
)([z_mean_mnist, z_log_var_mnist])


# =========================================================
# BUILD ENCODER MODEL
# =========================================================

encoder_mnist = Model(
    encoder_inputs_mnist, 
    [z_mean_mnist, z_log_var_mnist, z_mnist], 
    name="encoder_mnist"
)

print("\n=================================================")
print("Encoder Model Summary:")
print("=================================================")

encoder_mnist.summary()


# =========================================================
# DECODER ARCHITECTURE
# =========================================================

latent_inputs_mnist = layers.Input(shape=(latent_dim_mnist,))

d1_mnist = layers.Dense(
    hidden_dim2_mnist, 
    activation='relu'
)(latent_inputs_mnist)

d2_mnist = layers.Dense(
    hidden_dim1_mnist, 
    activation='relu'
)(d1_mnist)

decoder_outputs_mnist = layers.Dense(
    input_dim_mnist, 
    activation='sigmoid'
)(d2_mnist)


# =========================================================
# BUILD DECODER MODEL
# =========================================================

decoder_mnist = Model(
    latent_inputs_mnist, 
    decoder_outputs_mnist, 
    name="decoder_mnist"
)

print("\n=================================================")
print("Decoder Model Summary:")
print("=================================================")

decoder_mnist.summary()


# =========================================================
# VARIATIONAL AUTOENCODER (VAE) CUSTOM MODEL CLASS
# =========================================================

class VAE_MNIST(Model):

    def __init__(self, encoder, decoder, **kwargs):

        super(VAE_MNIST, self).__init__(**kwargs)

        self.encoder = encoder

        self.decoder = decoder


    def call(self, inputs):

        z_mean, z_log_var, z = self.encoder(inputs)

        reconstructed = self.decoder(z)

        reconstruction_loss = tf.reduce_mean(
            tf.keras.losses.binary_crossentropy(inputs, reconstructed)
        ) * input_dim_mnist

        kl_loss = -0.5 * tf.reduce_mean(
            1 + z_log_var - tf.square(z_mean) - tf.exp(z_log_var)
        )

        total_loss = reconstruction_loss + kl_loss

        self.add_loss(total_loss)

        return reconstructed


# =========================================================
# INITIALIZE AND COMPILE VAE MODEL
# =========================================================

vae_mnist = VAE_MNIST(encoder_mnist, decoder_mnist)

vae_mnist.compile(optimizer='adam')


# =========================================================
# TRAIN VAE MODEL
# =========================================================

print("\nTraining VAE on MNIST dataset...")

history_mnist = vae_mnist.fit(
    x_train_mnist, 
    x_train_mnist,
    epochs=10,
    batch_size=128,
    validation_data=(x_test_mnist, x_test_mnist),
    verbose=0
)

print("VAE training complete.")


# =========================================================
# RECONSTRUCT IMAGES
# =========================================================

x_test_reconstructed_mnist = vae_mnist.predict(
    x_test_mnist[:5]
)


# =========================================================
# RECONSTRUCTION PERFORMANCE METRICS (RMSE & MSE)
# =========================================================

rmse_mnist = np.sqrt(
    mean_squared_error(
        x_test_mnist[:5].flatten(), 
        x_test_reconstructed_mnist.flatten()
    )
)

mse_mnist = rmse_mnist ** 2


print("\n=================================================")
print("VAE RECONSTRUCTION RESULTS")
print("=================================================")

print(f"Reconstructed VAE Test Images RMSE: {rmse_mnist:.6f}")

print(f"Reconstructed VAE Test Images MSE:  {mse_mnist:.6f}")


# =========================================================
# SAMPLE FROM LATENT SPACE (GENERATION)
# =========================================================

random_latent_vector_mnist = np.random.normal(
    size=(1, latent_dim_mnist)
)

print("\nRandom Latent Vector Input: ", random_latent_vector_mnist)


# =========================================================
# GENERATE IMAGE
# =========================================================

generated_image_mnist = decoder_mnist.predict(
    random_latent_vector_mnist
)

generated_image_mnist = generated_image_mnist.reshape(28, 28)


# =========================================================
# VISUALIZE ORIGINAL VS RECONSTRUCTED IMAGES
# =========================================================

plt.figure(figsize=(12, 6))

for i in range(5):

    plt.subplot(3, 5, i + 1)

    plt.imshow(
        x_test_mnist[i].reshape(28, 28), 
        cmap='gray'
    )

    plt.axis('off')

    plt.title("Original")


for i in range(5):

    plt.subplot(3, 5, i + 6)

    plt.imshow(
        x_test_reconstructed_mnist[i].reshape(28, 28), 
        cmap='gray'
    )

    plt.axis('off')

    plt.title("Reconstructed")


plt.tight_layout()

plt.show()