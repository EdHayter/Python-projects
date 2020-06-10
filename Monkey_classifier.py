"""
Monkey image classifier
Data from: https://www.kaggle.com/slothkong/10-monkey-species

Ed Hayter 09/06/20
"""
import pandas as pd
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow import keras


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

#generate batches of data
train_gen = train_DG.flow_from_directory(train_path, 
                                         target_size = (128, 128), 
                                         batch_size = 64, 
                                         shuffle = True, 
                                         class_mode = 'categorical')

valid_gen = valid_DG.flow_from_directory(valid_path, 
                                         target_size = (128, 128), 
                                         batch_size = 64,
                                         class_mode = 'categorical') 

#build model
model = keras.models.Sequential()
model.add(keras.layers.Conv2D(32,kernel_size = 3,activation = 'selu',input_shape = (128,128,3)))
model.add(keras.layers.Conv2D(32,3,activation = 'selu'))
model.add(keras.layers.Conv2D(32,3,activation = 'selu'))
model.add(keras.layers.MaxPool2D())
model.add(keras.layers.Conv2D(64,3,activation = 'selu'))
model.add(keras.layers.Conv2D(64,3,activation = 'selu'))
model.add(keras.layers.MaxPool2D())
model.add(keras.layers.Conv2D(64,3,activation = 'selu'))
model.add(keras.layers.Conv2D(64,3,activation = 'selu'))
model.add(keras.layers.Flatten())
# model.add(keras.layers.Dropout(0.5))
model.add(keras.layers.Dense(10, activation='softmax'))
#compile 
model.compile(loss='categorical_crossentropy', optimizer='adam', metrics='accuracy')

#fit model and save history for plotting
history = model.fit(train_gen,
                    steps_per_epoch = 1098/64,
                    epochs = 50,
                    validation_data = valid_gen,
                    validation_steps = 272/64)

#function to plot accuracy or loss over time (or other metrics)
def plot_epochs(history, label):
    data = pd.DataFrame()
    data[label] = history.history[label]
    data['valid_' + label] = history.history['val_'+label]
    data.plot()
    
plot_epochs(history,'accuracy')
plot_epochs(history,'loss')

#We see high bias, most likely a model with higher capacity (and more training data) would suit.
#I don't really have the processing power for that. So i'm going to try some transfer learning!

    
