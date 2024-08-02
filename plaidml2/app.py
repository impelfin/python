import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from tensorflow.keras.models import Model
from tensorflow.keras.layers import Dense, Dropout, GlobalMaxPooling2D
from keras.utils import np_utils
from sklearn.model_selection import train_test_split
from tensorflow.keras.applications.resnet_v2 import ResNet50V2
from tensorflow.keras import optimizers
from tensorflow.keras.callbacks import EarlyStopping

import os
os.environ["KERAS_BACKEND"] = "plaidml.keras.backend"

# Load data
data_train = pd.read_csv('./input/train.csv')
data_test = pd.read_csv('./input/test.csv')

# Drop label column from training data and concatenate train and test data
data_train_w = data_train.drop(['label'], axis=1)
data = data_train_w.append(data_test, ignore_index=True)

# Extract labels from training data
y_train = data_train.iloc[:, 0]
X_train = (data_train.iloc[:, 1:].values).astype('float32')
X_test = (data_test.iloc[:, 0:].values).astype('float32')

# Normalize data
scale = np.max(X_train)
X_train /= scale
X_test /= scale

mean = np.std(X_train)
X_train -= mean
X_test -= mean

# Convert labels to categorical format
y_train = np_utils.to_categorical(y_train, 10)

# Split data into training and validation sets
X_train2, X_test2, y_train2, y_test2 = train_test_split(X_train, y_train)

# Reshape data to fit ResNet model input shape
X_train2 = X_train2.reshape(-1, 28, 28, 1)
X_train2 = np.repeat(X_train2[..., np.newaxis], 3, -1)

X_test = X_test.reshape(-1, 28, 28, 1)
X_test = np.repeat(X_test[..., np.newaxis], 3, -1)

# Define ResNet model
modelo = ResNet50V2(include_top=False, weights=None)
x = modelo.output
x = GlobalMaxPooling2D()(x)
x = Dense(256, activation='relu', name='Dense_Intermediate')(x)
x = Dropout(0.3)(x)
x = Dense(256, activation='relu', name='Dense_Intermediate2')(x)
predictions = Dense(units=10, activation='softmax')(x)
modelo = Model(inputs=modelo.input, outputs=predictions)

# Compile model
opt = optimizers.Adam()
modelo.compile(optimizer=opt, loss='categorical_crossentropy', metrics=['accuracy'])

# Set up early stopping
es = EarlyStopping(patience=10, restore_best_weights=True)

# Train model
history = modelo.fit(X_train2, y_train2, epochs=100, batch_size=100, validation_split=0.2, callbacks=[es])

# Make predictions
preds = modelo.predict(X_test, verbose=0)
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
