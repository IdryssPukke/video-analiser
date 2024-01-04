# pylint: disable=invalid-name
"""
Module to download stream, catch frame and load to database.
"""
import sys
import threading
import os
import time
import pickle
import logging

import pafy
import pymongo
import numpy as np
import yaml
import cv2
from kafka import KafkaProducer


logging.basicConfig(level=logging.INFO, format='%(message)s')

path_of_script = os.path.dirname(os.path.realpath(__file__))
config_file = os.path.join(path_of_script, "scraper_config.yaml")
with open(config_file) as yaml_file:
    config_dict = yaml.load(yaml_file)["config_dictionary"]


def init_mongo(mongo_location):
    """
    Initialize MongoDB connection.
    :param mongo_location:
    :return: None
    """
    database = pymongo.MongoClient(
                mongo_location,
                username=config_dict['mongo_user'],
                password=config_dict['mongo_password'],
                authSource=config_dict['mongo_database'],
                authMechanism='SCRAM-SHA-256')[config_dict['mongo_database']]
    return database


def init_kafka(kafka_location):
    """
    Initialize kafka process.
    :param kafka_location:
    :return: None
    """
    return KafkaProducer(bootstrap_servers=[kafka_location])


def cam_init(_url):
    """
    Initialize connection to camera.
    :param _url:
    :return:
    """
    try:
        if 'youtu' in _url:
            video_pafy = pafy.new(_url)
            play = video_pafy.getbest(preftype='mp4')
            vidcap = cv2.VideoCapture(play.url)
        else:
            vidcap = cv2.VideoCapture(_url)
    except Exception as exception:
        logging.error("Problem occured during establishing connection to camera\n%s", exception.args)
        return None

    return vidcap


def test_connection(_url):
    """
    Test connection.
    :param _url: tested url
    :return:
    """
    try:
        vidcap = cam_init(_url)
    except Exception:
        return "vidcap initialization problem"

    if vidcap is None:
        return "empty vidcap object"

    success, image = vidcap.read()
    if not success or image is None:
        return "can not get frame from stream"
    return "passed"


class StreamingScraper:
    """
    Class to catch stream, cut frame and send it to database.
    """
    def __init__(self, mongo_location="mongo1:27017", kafka_location='kafka:9093'):
        """

        :param mongo_location: mongo address
        :param kafka_location: kafka address
        """
        self.database = init_mongo(mongo_location)
        try:
            self.database.list_collections()
        except Exception as e:
            logging.error("Problem with connection to MongoDB\n%s", e.args)
            sys.exit(2)
        self.collection = self.database[config_dict['collection']]
        self.sample_period = 1/config_dict['sample_freq_Hz']
        self.producer = init_kafka(kafka_location)

    def start(self, _url, lock, threads):
        """

        :param _url:
        :param lock:
        :param threads:
        :return:
        """
        capture_time = time.time()
        while _url in threads:
            if capture_time < time.time():
                timestamp = round(time.time(), 2)
                vidcap = cam_init(_url)
                if vidcap is None:
                    logging.error("Can not establish connection %s", _url)
                    continue
                success, image = vidcap.read()
                if success:
                    image = cv2.resize(image, (1280, 720))
                    img_id = str(int(timestamp))+f'_{np.random.randint(999):0=3d}'
                    msg = pickle.dumps((img_id, timestamp, _url))
                    with lock:
                        self.collection.insert({'id': img_id, 'timestamp': timestamp, 'photo': pickle.dumps(image)})
                        self.producer.send('topictest', msg)
                    logging.info('Frame captured and sent %s from %s', img_id, _url)
                capture_time = self.sample_period+time.time()
            time.sleep(0.5)

    def start_manager(self):
        """

        :return:
        """
        lock = threading.Lock()
        settings = self.database["app_settings"]
        threads = {}
        while True:
            logging.info("running threads %s", *threads.keys())
            links = [*settings.find()]
            urls = [i["url"] for i in links]
            current_run_urls = [*threads.keys()]
            for i in current_run_urls:
                if i not in urls:
                    temp = threads[i]
                    del threads[i]
                    temp.join()
            current_run_urls = [*threads.keys()]
            for i in urls:
                logging.info("checking urls from database")
                if i not in current_run_urls:
                    if test_connection(i) == "passed":
                        threads[i] = threading.Thread(target=self.start, args=(i, lock, threads))
                        threads[i].start()
                        settings.update({"url": i}, {"$set": {"Status": "Up"}})
                    else:
                        settings.delete_many({"url": i})
            time.sleep(10)


if __name__ == "__main__":
    streaming_scraper = StreamingScraper()
    streaming_scraper.start_manager()
