from flask import Flask, jsonify, request

from dotenv import load_dotenv
import os
import pickle
import numpy as np
import tensorflow as tf
from PIL import Image
from scipy.misc import imresize
import imageio
from keras import backend
from flask_cors import CORS, cross_origin
from io import BytesIO
import time

app = Flask(__name__)
CORS(app)

@app.route('/ping')
def ping():
  print('someone is pinging')
  return 'pong'

@app.route('/kurkkuvaimopo', methods=["POST"])
def test():
  data = request.files.get('img', '')
  data = imageio.imread(data, pilmode="RGB")
  data = imresize(data, (128,128))
  with backend.get_session().graph.as_default() as g:
      res = model.predict(np.array(data).reshape(1, 128, 128, 3))
  return str(res[0][0])


if __name__ == '__main__':
  print("Backend starting")
  load_dotenv()
  if not os.path.isdir("./model"):
    print("NO MODEL VOLUME")
    exit(1)
  debug = os.getenv('ENV') == 'development'
  global model
  boolean_print = False
  while True:
    try:
      model = pickle.load(open('./model/kurkkumopotin.sav', 'rb'))
      break
    except:
      if not boolean_print:
        print("No 'kurkkumopotin.sav' model in the model volume. Waiting for training service to provide one.")
        boolean_print = True
      time.sleep(5)
      continue

  app.run("0.0.0.0", port=5000, debug=debug)