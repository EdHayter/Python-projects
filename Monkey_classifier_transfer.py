# -*- coding: utf-8 -*-
"""
Monkey image classifier
Data from: https://www.kaggle.com/slothkong/10-monkey-species
Transfer learning approach, using Xception

Ed Hayter 10/06/20
"""
from tensorflow import keras
import pandas as pd
from tensorflow.keras.preprocessing.image import ImageDataGenerator
import numpy as np
from sklearn.metrics import confusion_matrix

train_path = 'training'
valid_path = 'validation'
monkey_labels_path = 'C:\C Documents\Python\Monkey Classification\Monkey_labels.txt'

#import summary data, includes labels
monkey_labels = pd.read_csv(monkey_labels_path)
monkey_labels.columns = ['Label','Latin name','Common name','number train','number valid']

#make generators, include some augmentations to the train set
train_DG = ImageDataGenerator(rescale=1/255, 
                              rotation_range=30, 
                              width_shift_range=0.2, 
                              height_shift_range=0.2,
                              shear_range=0.2,
                              zoom_range=0.2,
                              horizontal_flip=True)

valid_DG = ImageDataGenerator(rescale=1/255)

#generate batches of data, shape to match Xception model
train_gen = train_DG.flow_from_directory(train_path, 
                                         target_size = (299, 299), 
                                         batch_size = 64, 
                                         shuffle = True, 
                                         class_mode = 'categorical')

valid_gen = valid_DG.flow_from_directory(valid_path, 
                                         target_size = (299, 299), 
                                         batch_size = 64,
                                         class_mode = 'categorical',
                                         shuffle=False) 
 
#take Xception model, remove final layer and replace with 10 way softmax
model = keras.models.Sequential()
model.add(keras.applications.Xception(include_top=False,
                                      weights="imagenet",
                                      pooling='max'))
                                
model.add(keras.layers.Dense(10, activation='softmax'))
#make Xception layers not trainable (weights imported from imagenet)
model.layers[0].trainable = False

#compile
model.compile(loss="categorical_crossentropy", optimizer="adam", metrics=['accuracy'])
#fit
history = model.fit(train_gen,
                    steps_per_epoch = 1098/64,
                    epochs = 5,
                    validation_data = valid_gen,
                    validation_steps = 272/64)
#plot function
def plot_epochs(history, label):
    data = pd.DataFrame()
    data[label] = history.history[label]
    data['valid_' + label] = history.history['val_'+label]
    data.plot()
    
plot_epochs(history,'accuracy')
plot_epochs(history,'loss')

#100% validation accuracy! [depends on seed]
val_pred = np.argmax(model.predict(valid_gen),axis=1)
y_val = valid_gen.classes
#See confusion matrix
confusion_matrix(val_pred,y_val)






