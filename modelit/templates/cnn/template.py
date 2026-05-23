# =========================================================
# CNN FROM SCRATCH + CNN USING KERAS
# Uses Built-in MNIST Dataset
# No Kaggle Download Needed
# =========================================================


# =========================================================
# IMPORTS
# =========================================================

import cv2
import numpy as np
import matplotlib.pyplot as plt

from tensorflow.keras.datasets import mnist
from tensorflow.keras.models import Sequential

from tensorflow.keras.layers import (
    Conv2D,
    MaxPooling2D,
    Flatten,
    Dense
)

from sklearn.model_selection import train_test_split


# =========================================================
# LOAD SAMPLE IMAGE
# =========================================================

(X_train_full, y_train_full), (X_test_full, y_test_full) = mnist.load_data()

image = X_train_full[0]

print("Original Image Shape:", image.shape)

plt.imshow(image, cmap="gray")
plt.title("Original Image")
plt.axis("off")
plt.show()


# =========================================================
# CONVOLUTION FROM SCRATCH
# =========================================================

def convolution(image, kernel, strides=1):

    image_height, image_width = image.shape

    kernel_height, kernel_width = kernel.shape

    output_height = (
        (image_height - kernel_height) // strides
    ) + 1

    output_width = (
        (image_width - kernel_width) // strides
    ) + 1

    output = np.zeros((output_height, output_width))

    for i in range(1, image.shape[0] - 1, strides):

        for j in range(1, image.shape[1] - 1, strides):

            val = (

                image[i - 1, j - 1] * kernel[0, 0] +

                image[i - 1, j] * kernel[0, 1] +

                image[i - 1, j + 1] * kernel[0, 2] +

                image[i, j - 1] * kernel[1, 0] +

                image[i, j] * kernel[1, 1] +

                image[i, j + 1] * kernel[1, 2] +

                image[i + 1, j - 1] * kernel[2, 0] +

                image[i + 1, j] * kernel[2, 1] +

                image[i + 1, j + 1] * kernel[2, 2]

            )

            out_i = (i - 1) // strides

            out_j = (j - 1) // strides

            output[out_i, out_j] = val

    return output


# =========================================================
# EDGE DETECTION KERNEL
# =========================================================

kernel = np.array([
    [-1, -1, -1],
    [-1,  8, -1],
    [-1, -1, -1]
])


# =========================================================
# APPLY CONVOLUTION
# =========================================================

conv_img = convolution(image, kernel, 1)

plt.imshow(conv_img, cmap="gray")
plt.title("Convolution Output")
plt.axis("off")
plt.show()


# =========================================================
# RELU ACTIVATION
# =========================================================

def relu(image):

    for i in range(0, image.shape[0]):

        for j in range(0, image.shape[1]):

            if image[i, j] >= 0:

                image[i, j] = image[i, j]

            else:

                image[i, j] = 0

    return image


# =========================================================
# APPLY RELU
# =========================================================

relu_img = relu(conv_img)

plt.imshow(relu_img, cmap="gray")
plt.title("ReLU Output")
plt.axis("off")
plt.show()


# =========================================================
# MAX POOLING
# =========================================================

def max_pooling(image, pool_size=2, strides=2):

    image_height, image_width = image.shape

    output_height = (
        (image_height - pool_size) // strides
    ) + 1

    output_width = (
        (image_width - pool_size) // strides
    ) + 1

    output = np.zeros((output_height, output_width))

    for i in range(0, image_height - 1, strides):

        for j in range(0, image_width - 1, strides):

            val = image[i, j]

            if image[i, j + 1] > val:

                val = image[i, j + 1]

            if image[i + 1, j] > val:

                val = image[i + 1, j]

            if image[i + 1, j + 1] > val:

                val = image[i + 1, j + 1]

            out_i = i // strides

            out_j = j // strides

            if (
                out_i < output_height and
                out_j < output_width
            ):

                output[out_i, out_j] = val

    return output


# =========================================================
# APPLY MAX POOLING
# =========================================================

pool_img = max_pooling(relu_img, 2, 2)

plt.imshow(pool_img, cmap="gray")
plt.title("Max Pooling Output")
plt.axis("off")
plt.show()


# =========================================================
# FLATTEN
# =========================================================

flat_img = pool_img.flatten()

print("\n=================================================")

print("Original Image Shape:", image.shape)

print("Convolution Shape:", conv_img.shape)

print("ReLU Shape:", relu_img.shape)

print("Pooling Shape:", pool_img.shape)

print("Flatten Shape:", flat_img.shape)

print("=================================================")


# =========================================================
# DENSE LAYER
# =========================================================

weights = np.random.rand(flat_img.shape[0])

dense_output = np.dot(flat_img, weights)

print("\nDense Layer Output:", dense_output)


# =========================================================
# CNN USING KERAS
# =========================================================

print("\n=================================================")
print("CNN USING KERAS")
print("=================================================")


# =========================================================
# NORMALIZATION
# =========================================================

X_train_full = X_train_full / 255.0

X_test_full = X_test_full / 255.0


# =========================================================
# RESHAPE FOR CNN
# =========================================================

X_train_full = X_train_full.reshape(-1, 28, 28, 1)

X_test_full = X_test_full.reshape(-1, 28, 28, 1)


# =========================================================
# TRAIN TEST SPLIT
# =========================================================

X_train, X_val, y_train, y_val = train_test_split(

    X_train_full,
    y_train_full,

    test_size=0.2,

    random_state=42

)


print("\nTraining Samples:", X_train.shape[0])

print("Validation Samples:", X_val.shape[0])


# =========================================================
# CREATE CNN MODEL
# =========================================================

model = Sequential()


# =========================================================
# CONVOLUTION + RELU + POOLING
# =========================================================

model.add(

    Conv2D(
        32,
        (3, 3),
        activation="relu",
        input_shape=(28, 28, 1)
    )

)

model.add(

    MaxPooling2D((2, 2))

)


# =========================================================
# SECOND CNN BLOCK
# =========================================================

model.add(

    Conv2D(
        64,
        (3, 3),
        activation="relu"
    )

)

model.add(

    MaxPooling2D((2, 2))

)


# =========================================================
# THIRD CNN BLOCK
# =========================================================

model.add(

    Conv2D(
        128,
        (3, 3),
        activation="relu"
    )

)

model.add(

    MaxPooling2D((2, 2))

)


# =========================================================
# FLATTEN
# =========================================================

model.add(Flatten())


# =========================================================
# DENSE LAYER
# =========================================================

model.add(

    Dense(
        64,
        activation="relu"
    )

)


# =========================================================
# OUTPUT LAYER
# MNIST = 10 CLASSES
# =========================================================

model.add(

    Dense(
        10,
        activation="softmax"
    )

)


# =========================================================
# MODEL SUMMARY
# =========================================================

model.summary()


# =========================================================
# COMPILE MODEL
# =========================================================

model.compile(

    optimizer="adam",

    loss="sparse_categorical_crossentropy",

    metrics=["accuracy"]

)


# =========================================================
# TRAIN MODEL
# =========================================================

train_model = model.fit(

    X_train,
    y_train,

    epochs=5,

    validation_data=(X_val, y_val)

)


# =========================================================
# EVALUATE MODEL
# =========================================================

loss, accuracy = model.evaluate(
    X_test_full,
    y_test_full
)

print("\n=================================================")

print("Test Accuracy:", accuracy)

print("Test Loss:", loss)

print("=================================================")


# =========================================================
# PREDICTION
# =========================================================

prediction = model.predict(
    X_test_full[0].reshape(1, 28, 28, 1)
)

predicted_class = np.argmax(prediction)

print("\nPredicted Digit:", predicted_class)

print("Actual Digit:", y_test_full[0])


# =========================================================
# SHOW TEST IMAGE
# =========================================================

plt.imshow(
    X_test_full[0].reshape(28, 28),
    cmap="gray"
)

plt.title(
    f"Predicted: {predicted_class}"
)

plt.axis("off")

plt.show()