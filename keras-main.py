# This works ok: The model was trained and saved already into models/keras.

# %% 

# common to keras and pytorch
# import numpy as np
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image

# keras and dependencies
import keras
from keras.preprocessing.image import ImageDataGenerator
from keras.applications import ResNet50
from keras.applications.resnet50 import preprocess_input
from keras import Model, layers
from keras.models import load_model, model_from_json
import os
# Undesiderable fix of a bug. But so far it's the only way.
os.environ['KMP_DUPLICATE_LIB_OK']='True'

# %%
train_datagen = ImageDataGenerator(
    shear_range=10,
    zoom_range=0.2,
    horizontal_flip=True,
    preprocessing_function=preprocess_input)
# %%
train_generator = train_datagen.flow_from_directory(
    'data/train',
    batch_size=32,
    class_mode='binary',
    target_size=(224,224))

# %%
validation_datagen = ImageDataGenerator(
    preprocessing_function=preprocess_input)

# %%
validation_generator = validation_datagen.flow_from_directory(
    'data/validation',
    shuffle=False,
    class_mode='binary',
    target_size=(224,224))

# %% CREATE THE  ResNet50 Network model

# load pre-trained network, cut off its head and freeze its weights,
conv_base = ResNet50(include_top=False,
                     weights='imagenet')

# add custom dense layers (we pick 128 neurons for the hidden layer),
for layer in conv_base.layers:
    layer.trainable = False

x = conv_base.output
x = layers.GlobalAveragePooling2D()(x)
x = layers.Dense(128, activation='relu')(x)
predictions = layers.Dense(2, activation='softmax')(x)
model = Model(conv_base.input, predictions)

# set the optimizer and loss function.
optimizer = keras.optimizers.Adam()
model.compile(loss='sparse_categorical_crossentropy',
              optimizer=optimizer,
              metrics=['accuracy'])

# %% TRAIN the model we created
history = model.fit_generator(
    generator=train_generator,
    epochs=3,
    validation_data=validation_generator)

# save the model: architecture to JSON, weights to HDF5
model.save_weights('models/keras/weights.h5')
with open('models/keras/architecture.json', 'w') as f:
    f.write(model.to_json())