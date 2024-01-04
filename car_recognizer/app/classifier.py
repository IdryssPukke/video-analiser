""""
Copyright © 2019 by Spectrico
Licensed under the MIT License
"""
import os
import config

import numpy as np
import tensorflow.compat.v1 as tf
import cv2


MODEL_FILE = config.MODEL_FILE
LABEL_FILE = config.LABEL_FILE
INPUT_LAYER = config.INPUT_LAYER
OUTPUT_LAYER = config.OUTPUT_LAYER
CLASSIFIER_INPUT_SIZE = config.CLASSIFIER_INPUT_SIZE

path_of_script = os.path.dirname(os.path.realpath(__file__))


def load_graph(model_file):
    """

    :param model_file:
    :return:
    """
    graph = tf.Graph()
    graph_def = tf.GraphDef()
    to_open = os.path.join(path_of_script, model_file)
    with open(to_open, "rb") as f:
        graph_def.ParseFromString(f.read())
    with graph.as_default():
        tf.import_graph_def(graph_def)

    return graph


def load_labels(label_file):
    """

    :param label_file:
    :return:
    """
    label = []
    to_open = os.path.join(path_of_script, label_file)
    with open(to_open, "r", encoding='cp1251') as ins:
        for line in ins:
            label.append(line.rstrip())

    return label


def resize_and_pad(img, size, pad_color=0):
    """

    :param img:
    :param size:
    :param pad_color:
    :return:
    """
    height, width = img.shape[:2]
    sh, sw = size

    # interpolation method
    if height > sh or width > sw:  # shrinking image
        interp = cv2.INTER_AREA
    else:  # stretching image
        interp = cv2.INTER_CUBIC

    # aspect ratio of image
    aspect = width / height

    # compute scaling and pad sizing
    if aspect > 1:  # horizontal image
        new_w = sw
        new_h = np.round(new_w / aspect).astype(int)
        pad_vert = (sh - new_h) / 2
        pad_top, pad_bot = np.floor(pad_vert).astype(int), np.ceil(pad_vert).astype(int)
        pad_left, pad_right = 0, 0
    elif aspect < 1:  # vertical image
        new_h = sh
        new_w = np.round(new_h * aspect).astype(int)
        pad_horz = (sw - new_w) / 2
        pad_left, pad_right = np.floor(pad_horz).astype(int), np.ceil(pad_horz).astype(int)
        pad_top, pad_bot = 0, 0
    else:  # square image
        new_h, new_w = sh, sw
        pad_left, pad_right, pad_top, pad_bot = 0, 0, 0, 0

    # set pad color
    if len(img.shape) == 3 and not isinstance(pad_color,
                                              (list, tuple, np.ndarray)):  # color image but only one color provided
        pad_color = [pad_color] * 3

    # scale and pad
    scaled_img = cv2.resize(img, (new_w, new_h), interpolation=interp)
    scaled_img = cv2.copyMakeBorder(scaled_img, pad_top, pad_bot, pad_left, pad_right,
                                    borderType=cv2.BORDER_CONSTANT,
                                    value=pad_color)
    return scaled_img


class Classifier:
    """
    Class responsible for classifying objects on captured image.
    """
    def __init__(self):
        os.environ["CUDA_DEVICE_ORDER"] = "PCI_BUS_ID"
        os.environ['CUDA_VISIBLE_DEVICES'] = '-1'

        self.graph = load_graph(MODEL_FILE)
        self.labels = load_labels(LABEL_FILE)

        input_name = "import/" + INPUT_LAYER
        output_name = "import/" + OUTPUT_LAYER
        self.input_operation = self.graph.get_operation_by_name(input_name)
        self.output_operation = self.graph.get_operation_by_name(output_name)

        self.sess = tf.Session(graph=self.graph)
        self.sess.graph.finalize()  # Graph is read-only after this statement.

    def predict(self, img):
        """

        :param img: capture image
        :return:
        """
        img = img[:, :, ::-1]
        img = resize_and_pad(img, CLASSIFIER_INPUT_SIZE)

        # Add a forth dimension since Tensorflow expects a list of images
        img = np.expand_dims(img, axis=0)

        # Scale the input image to the range used in the trained network
        img = img.astype(np.float32)
        img /= 127.5
        img -= 1.

        results = self.sess.run(self.output_operation.outputs[0], {
            self.input_operation.outputs[0]: img
        })
        results = np.squeeze(results)

        top = 3
        top_indices = results.argsort()[-top:][::-1]
        classes = []
        for ix in top_indices:
            make_model = self.labels[ix].split('\t')
            classes.append({"make": make_model[0], "model": make_model[1], "prob": str(results[ix])})
        return classes
