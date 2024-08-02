import os
os.environ["KERAS_BACKEND"] = "plaidml.keras.backend"

import plaidml.keras
plaidml.keras.install_backend()

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from keras.models import Model
from keras.layers import Dense, Dropout, GlobalMaxPooling2D, Conv2D, MaxPooling2D, BatchNormalization, Activation, Add, Input
from keras.utils import np_utils
from sklearn.model_selection import train_test_split
from keras import optimizers
from keras.callbacks import EarlyStopping
import cv2

# PlaidML 설정 확인
print("Using PlaidML backend")

# Load data
data_train = pd.read_csv('./input/train.csv')
data_test = pd.read_csv('./input/test.csv')

# Drop label column from training data and concatenate train and test data
data_train_w = data_train.drop(['label'], axis=1)
data = pd.concat([data_train_w, data_test], ignore_index=True)

# Extract labels from training data
y_train = data_train.iloc[:, 0]
X_train = (data_train.iloc[:, 1:].values).astype('float32')
X_test = (data_test.iloc[:, 0:].values).astype('float32')

# Normalize data
scale = np.max(X_train)
X_train /= scale
X_test /= scale

mean = np.mean(X_train)
X_train -= mean
X_test -= mean

# Convert labels to categorical format
y_train = np_utils.to_categorical(y_train, 10)

# Split data into training and validation sets
X_train2, X_test2, y_train2, y_test2 = train_test_split(X_train, y_train)

# Reshape and upscale data to fit ResNet model input shape
X_train2 = X_train2.reshape(-1, 28, 28, 1)
X_train2 = np.repeat(X_train2, 3, axis=-1)  # Repeat the last dimension to create (batch_size, height, width, channels)
X_train2_resized = np.array([cv2.resize(img, (32, 32)) for img in X_train2])

X_test = X_test.reshape(-1, 28, 28, 1)
X_test = np.repeat(X_test, 3, axis=-1)  # Repeat the last dimension to create (batch_size, height, width, channels)
X_test_resized = np.array([cv2.resize(img, (32, 32)) for img in X_test])

def identity_block(X, f, filters, stage, block):
    # Define name basis
    conv_name_base = 'res' + str(stage) + block + '_branch'
    bn_name_base = 'bn' + str(stage) + block + '_branch'

    # Retrieve Filters
    F1, F2, F3 = filters

    # Save the input value
    X_shortcut = X

    # First component of main path
    X = Conv2D(filters=F1, kernel_size=(1, 1), strides=(1, 1), padding='valid', name=conv_name_base + '2a', kernel_initializer='he_normal')(X)
    X = BatchNormalization(axis=3, name=bn_name_base + '2a')(X)
    X = Activation('relu')(X)

    # Second component of main path
    X = Conv2D(filters=F2, kernel_size=(f, f), strides=(1, 1), padding='same', name=conv_name_base + '2b', kernel_initializer='he_normal')(X)
    X = BatchNormalization(axis=3, name=bn_name_base + '2b')(X)
    X = Activation('relu')(X)

    # Third component of main path
    X = Conv2D(filters=F3, kernel_size=(1, 1), strides=(1, 1), padding='valid', name=conv_name_base + '2c', kernel_initializer='he_normal')(X)
    X = BatchNormalization(axis=3, name=bn_name_base + '2c')(X)

    # Final step: Add shortcut value to main path, and pass it through a RELU activation
    X = Add()([X, X_shortcut])
    X = Activation('relu')(X)

    return X

def convolutional_block(X, f, filters, stage, block, s=2):
    # Define name basis
    conv_name_base = 'res' + str(stage) + block + '_branch'
    bn_name_base = 'bn' + str(stage) + block + '_branch'

    # Retrieve Filters
    F1, F2, F3 = filters

    # Save the input value
    X_shortcut = X

    # First component of main path
    X = Conv2D(F1, (1, 1), strides=(s, s), name=conv_name_base + '2a', kernel_initializer='he_normal')(X)
    X = BatchNormalization(axis=3, name=bn_name_base + '2a')(X)
    X = Activation('relu')(X)

    # Second component of main path
    X = Conv2D(F2, (f, f), strides=(1, 1), padding='same', name=conv_name_base + '2b', kernel_initializer='he_normal')(X)
    X = BatchNormalization(axis=3, name=bn_name_base + '2b')(X)
    X = Activation('relu')(X)

    # Third component of main path
    X = Conv2D(F3, (1, 1), strides=(1, 1), name=conv_name_base + '2c', kernel_initializer='he_normal')(X)
    X = BatchNormalization(axis=3, name=bn_name_base + '2c')(X)

    # Shortcut path
    X_shortcut = Conv2D(F3, (1, 1), strides=(s, s), name=conv_name_base + '1', kernel_initializer='he_normal')(X_shortcut)
    X_shortcut = BatchNormalization(axis=3, name=bn_name_base + '1')(X_shortcut)

    # Final step: Add shortcut value to main path, and pass it through a RELU activation
    X = Add()([X, X_shortcut])
    X = Activation('relu')(X)

    return X

def ResNet50(input_shape=(32, 32, 3), classes=10):
    # Define the input as a tensor with shape input_shape
    X_input = Input(input_shape)

    # Zero-Padding
    X = Conv2D(64, (7, 7), strides=(2, 2), name='conv1', kernel_initializer='he_normal')(X_input)
    X = BatchNormalization(axis=3, name='bn_conv1')(X)
    X = Activation('relu')(X)
    X = MaxPooling2D((3, 3), strides=(2, 2))(X)

    # Stage 2
    X = convolutional_block(X, f=3, filters=[64, 64, 256], stage=2, block='a', s=1)
    X = identity_block(X, 3, [64, 64, 256], stage=2, block='b')
    X = identity_block(X, 3, [64, 64, 256], stage=2, block='c')

    # Stage 3
    X = convolutional_block(X, f=3, filters=[128, 128, 512], stage=3, block='a', s=2)
    X = identity_block(X, 3, [128, 128, 512], stage=3, block='b')
    X = identity_block(X, 3, [128, 128, 512], stage=3, block='c')
    X = identity_block(X, 3, [128, 128, 512], stage=3, block='d')

    # Stage 4
    X = convolutional_block(X, f=3, filters=[256, 256, 1024], stage=4, block='a', s=2)
    X = identity_block(X, 3, [256, 256, 1024], stage=4, block='b')
    X = identity_block(X, 3, [256, 256, 1024], stage=4, block='c')
    X = identity_block(X, 3, [256, 256, 1024], stage=4, block='d')
    X = identity_block(X, 3, [256, 256, 1024], stage=4, block='e')
    X = identity_block(X, 3, [256, 256, 1024], stage=4, block='f')

    # Stage 5
    X = convolutional_block(X, f=3, filters=[512, 512, 2048], stage=5, block='a', s=2)
    X = identity_block(X, 3, [512, 512, 2048], stage=5, block='b')
    X = identity_block(X, 3, [512, 512, 2048], stage=5, block='c')

    # AVGPOOL
    X = GlobalMaxPooling2D(name='avg_pool')(X)

    # Output layer
    X = Dense(classes, activation='softmax', name='fc' + str(classes), kernel_initializer='he_normal')(X)

    # Create model
    model = Model(inputs=X_input, outputs=X, name='ResNet50')

    return model

# Define ResNet model
modelo = ResNet50(input_shape=(32, 32, 3), classes=10)

# Compile model
opt = optimizers.Adam()
modelo.compile(optimizer=opt, loss='categorical_crossentropy', metrics=['accuracy'])

# Set up early stopping
es = EarlyStopping(patience=10, restore_best_weights=True)

# Train model
history = modelo.fit(X_train2_resized, y_train2, epochs=5, batch_size=100, validation_split=0.2, callbacks=[es])

# Make predictions
preds = modelo.predict(X_test_resized, verbose=0)
predict_class = np.argmax(preds, axis=1)

# Save predictions to CSV
def write_preds(preds, fname):
    pd.DataFrame({"ImageId": list(range(1, len(preds) + 1)), "Label": preds}).to_csv(fname, index=False, header=True)

write_preds(predict_class, "keras-mlp.csv")

# Plot training loss
plt.plot(history.history['loss'])
plt.plot(history.history['val_loss'])
plt.title('Model Loss')
plt.ylabel('loss')
plt.xlabel('epoch')
plt.legend(['train', 'test'], loc='upper left')
plt.show()
