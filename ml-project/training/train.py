import pandas as pd 
import numpy as np
import pickle
import tensorflow as tf 
from sklearn.model_selection import train_test_split
from keras.models import Sequential
from keras.layers import Dense, Conv2D, MaxPooling2D, Dropout, Flatten, BatchNormalization
import imageio
import requests
from scipy.misc import imresize
from multiprocessing.pool import Pool
from functools import partial
import uuid
from pathlib import Path
from keras import backend as K


def create_model():
    model = Sequential()
    model.add(Conv2D(64, (4, 4), input_shape=(128, 128, 3)))
    model.add(MaxPooling2D((3, 3)))
    model.add(Conv2D(64, (3, 3), activation="relu"))
    model.add(MaxPooling2D((3, 3)))
    model.add(Flatten())
    model.add(Dense(128, activation="relu"))
    model.add(Dense(256))
    model.add(BatchNormalization())
    model.add(Dense(128, activation="relu"))
    model.add(Dense(1, activation="sigmoid"))
     
    return model

def train(X, y):
    y = np.array(y["y"])
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.33)
    X_train = np.array([imageio.imread(uri, as_gray=False, pilmode="RGB") for uri in X_train["uri"]])
    X_test = np.array([imageio.imread(uri, as_gray=False, pilmode="RGB") for uri in X_test["uri"]])

    model = create_model()
    model.compile(optimizer="rmsprop", loss="binary_crossentropy", metrics=["accuracy"])
    model.fit(x=X_train, y=y_train, batch_size=128, epochs=5, verbose=1)
    points = model.evaluate(X_test, y_test)
    pickle.dump(model, open('./model/kurkkumopotin.sav', 'wb'))
    return

def get_images(prefix, url):
    imgs = [] 
    uri = ""
    try:
      img = imageio.imread(url)
      img = imresize(img, (128, 128))
      identifier = str(uuid.uuid4())
      uri = "imgs/" + prefix + identifier + ".jpg"
      imageio.imwrite(uri, img)
    except (FileNotFoundError):
        raise
    except:
       return

    return uri

if __name__ == "__main__":
    K.clear_session()
    try:
        pickle.load(open("./model/kurkkumopotin.sav", "rb"))
        print("Model already exists at './model/kurkkumopotin.sav'")
    except:
        try:
            cucumbers = pd.read_csv("./data/cucumber.csv")
            mopeds = pd.read_csv('./data/moped.csv')
        except:
            print("Cant find 'data' volume with csv:s for image download ")
            exit(1)

        p = Pool(100)

        print("gathering cucumbers...")
        func = partial(get_images, "cucumber_")
        cucumber_imgs = p.map(func, cucumbers["url"])
        print("gathering mopeds...")
        func = partial(get_images, "moped_")
        moped_imgs = p.map(func, mopeds["url"])
        p.close()
        cucumbers = pd.DataFrame({"uri": cucumber_imgs, "y": 0})
        cucumbers.to_csv("./data/cucumbers2.csv")
        mopeds = pd.DataFrame({"uri": moped_imgs, "y": 1})
        mopeds.to_csv("./data/mopeds2.csv")

        merged = pd.concat([pd.read_csv("./data/cucumbers2.csv"), pd.read_csv("./data/mopeds2.csv")])
        merged = merged.dropna()
        X = merged.drop(["y"], axis=1)
        y = merged.drop(["uri"], axis=1)

        train(X, y)
        exit(0)

    

