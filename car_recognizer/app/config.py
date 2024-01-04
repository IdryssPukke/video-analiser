"""
Copyright © 2019 by Spectrico
# Licensed under the MIT License
"""

MODEL_FILE = "model-weights-spectrico-mmr-mobilenet-128x128-344FF72B.pb"  # path to the car make and model classifier
LABEL_FILE = "labels.txt"   # path to the text file, containing list with the supported makes and models
INPUT_LAYER = "input_1"
OUTPUT_LAYER = "softmax/Softmax"
CLASSIFIER_INPUT_SIZE = (128, 128)  # input size of the classifier
