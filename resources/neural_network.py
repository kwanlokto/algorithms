import json
import pickle

import numpy as np


class MNISTResource(object):
    def on_post(self, req, resp):
        """
        Handles all post request
        """
        img = req.get_json()

        pickled_file = ""
        cnn = pickle.load(open(pickled_file, "rb"))  # load the pickled CNN

        digit, probability = cnn.predict(img)

        return json.dumps({
            "digit": digit,
            "probability": np.round(probability, 3),
        })
