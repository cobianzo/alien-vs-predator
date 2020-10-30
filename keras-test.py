# This works. Just run the scripts. 
# Shows as output the result of the analysis of 3 selected images
# TODO: convert it into a script with params, able to read imgs from a folder

# common to keras and pytorch
# import numpy as np

# %%
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
# architecture from JSON, weights from HDF5
with open('models/keras/architecture.json') as f:
    model = model_from_json(f.read())
model.load_weights('models/keras/weights.h5')

# %%
# imgs to test
validation_img_paths = ["data/validation/alien/11.jpg",
                        "data/validation/alien/22.jpg",
                        "data/validation/predator/33.jpg"]
img_list = [Image.open(img_path) for img_path in validation_img_paths]

# %%
# perfrom test
img_size = 250
validation_batch = np.stack([preprocess_input(np.array(img.resize((img_size, img_size))))
                             for img in img_list])

pred_probs = model.predict(validation_batch)

# %%
fig, axs = plt.subplots(1, len(img_list), figsize=(20, 5))
for i, img in enumerate(img_list):
    ax = axs[i]
    ax.axis('off')
    title = "{:.0f}% Alien, {:.0f}% Predator".format(100*pred_probs[i,0],
                                                          100*pred_probs[i,1])
    ax.set_title(title)
    ax.imshow(img)
    print(title)
# %%
