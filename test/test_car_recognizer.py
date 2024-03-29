import unittest
import sys
import os

my_path = os.path.dirname(os.path.realpath(__file__))
path_to_streaming_project = os.path.dirname(my_path)
sys.path.append(path_to_streaming_project)
sys.path.append(os.path.join(path_to_streaming_project, 'car_recognizer', 'app'))

from car_recognizer.app.car_rec import *

img_1 = os.path.join(my_path, "test_car_recognizer_images/104.jpeg")
img_2 = os.path.join(my_path, "test_car_recognizer_images/103.jpeg")
img_3 = os.path.join(my_path, "test_car_recognizer_images/101.jpeg")
image1 = cv2.imread(img_1)
image2 = cv2.imread(img_2)
image3 = cv2.imread(img_3)


class MyTest(unittest.TestCase):
    def testing_single_car(self):
        self.assertEqual(car_rec(image1), [[63, 89, 395, 197, 'car', 'Koenigsegg', 'Regera']])

    def testing_single_car_confidence(self):
        self.assertEqual(car_rec(image1, 0.8), [[63, 89, 395, 197, 'car', 'Koenigsegg', 'Regera']])

    def testing_single_car_confidence_and_threshold(self):
        self.assertEqual(car_rec(image1, 0.8), [[63, 89, 395, 197, 'car', 'Koenigsegg', 'Regera']])

    def testing_multiple_cars_pic1(self):
        self.assertEqual(car_rec(image2),
                         [[1035, 460, 158, 115, 'car', 'Honda', 'Civic'], [195, 438, 156, 142, 'car', 'Honda', 'CR-V'],
                          [721, 486, 210, 180, 'car', 'Toyota', 'Sequoia'],
                          [514, 365, 141, 98, 'car', 'Subaru', 'Impreza'],
                          [-1, 438, 111, 108, 'car', 'Ford', 'Mustang'],
                          [229, 381, 158, 105, 'car', 'Chevrolet', 'Camaro'],
                          [287, 594, 203, 74, 'car', 'Porsche', 'Cayenne'],
                          [462, 477, 169, 155, 'car', 'Dodge', 'Dakota'], [1086, 196, 81, 54, 'car', 'Ford', 'Mustang'],
                          [860, 198, 76, 48, 'car', 'Honda', 'Civic'], [0, 359, 131, 113, 'car', 'Mini', 'Cooper'],
                          [552, 289, 86, 50, 'car', 'Ford', 'Mustang'], [299, 315, 126, 77, 'car', 'Ford', 'Mustang'],
                          [809, 105, 69, 39, 'car', 'Jeep', 'Wrangler'], [385, 254, 91, 68, 'car', 'BMW', '3 Series'],
                          [157, 286, 106, 72, 'car', 'Toyota', 'Corolla'],
                          [57, 327, 113, 87, 'car', 'Volkswagen', 'Golf'],
                          [1127, 132, 64, 52, 'car', 'Jeep', 'Wrangler'],
                          [722, 378, 150, 106, 'car', 'Land-Rover', 'Range Rover'],
                          [1076, 103, 55, 41, 'car', 'Subaru', 'WRX'], [982, 66, 41, 33, 'car', 'Ford', 'Mustang'],
                          [848, 158, 76, 34, 'car', 'BMW', '7 Series'],
                          [575, 237, 81, 58, 'car', 'Lamborghini', 'Aventador'],
                          [200, 247, 84, 61, 'car', 'Honda', 'Civic'], [459, 170, 63, 53, 'car', 'Jeep', 'Wrangler'],
                          [542, 100, 45, 40, 'car', 'Ford', 'Mustang'], [360, 147, 70, 47, 'car', 'Ford', 'Mustang'],
                          [731, 198, 80, 54, 'car', 'Porsche', '911'], [586, 207, 69, 33, 'car', 'Honda', 'Civic'],
                          [1172, 174, 27, 43, 'car', 'Nissan', 'Skyline'], [923, 296, 114, 84, 'car', 'Nissan', 'Leaf'],
                          [726, 160, 81, 51, 'car', 'Ford', 'Mustang'], [298, 184, 86, 61, 'truck'],
                          [610, 143, 53, 33, 'car', 'Lamborghini', 'Aventador'],
                          [733, 296, 116, 93, 'car', 'Scion', 'xB'], [727, 136, 56, 20, 'car', 'Ford', 'Mustang'],
                          [807, 77, 57, 36, 'car', 'Ford', 'Mustang'], [493, 67, 51, 35, 'car', 'Subaru', 'Impreza'],
                          [253, 207, 87, 69, 'car', 'Land-Rover', 'Discovery'],
                          [415, 195, 78, 35, 'car', 'Jeep', 'Wrangler'],
                          [500, 126, 67, 64, 'car', 'Lamborghini', 'Aventador'],
                          [410, 220, 86, 60, 'car', 'Lamborghini', 'Aventador'],
                          [615, 118, 53, 30, 'car', 'Porsche', '911'],
                          [442, 102, 51, 35, 'car', 'Lamborghini', 'Aventador'],
                          [891, 233, 114, 87, 'car', 'Mini', 'Cooper'],
                          [597, 183, 58, 31, 'car', 'Porsche', '911'], [513, 335, 108, 57, 'car', 'Ford', 'Mustang'],
                          [636, 97, 40, 22, 'car', 'Honda', 'CR-V'], [719, 64, 48, 36, 'car', 'Pagani', 'Huayra']])

    def testing_multiple_cars_confidence_pic1(self):
        self.assertEqual(car_rec(image2, 0.8),
                         [[1035, 460, 158, 115, 'car', 'Honda', 'Civic'], [195, 438, 156, 142, 'car', 'Honda', 'CR-V'],
                          [721, 486, 210, 180, 'car', 'Toyota', 'Sequoia'],
                          [514, 365, 141, 98, 'car', 'Subaru', 'Impreza'],
                          [-1, 438, 111, 108, 'car', 'Ford', 'Mustang'],
                          [229, 381, 158, 105, 'car', 'Chevrolet', 'Camaro'],
                          [287, 594, 203, 74, 'car', 'Porsche', 'Cayenne'],
                          [462, 477, 169, 155, 'car', 'Dodge', 'Dakota'], [1086, 196, 81, 54, 'car', 'Ford', 'Mustang'],
                          [860, 198, 76, 48, 'car', 'Honda', 'Civic'], [0, 359, 131, 113, 'car', 'Mini', 'Cooper'],
                          [552, 289, 86, 50, 'car', 'Ford', 'Mustang'], [299, 315, 126, 77, 'car', 'Ford', 'Mustang'],
                          [809, 105, 69, 39, 'car', 'Jeep', 'Wrangler'], [385, 254, 91, 68, 'car', 'BMW', '3 Series'],
                          [157, 286, 106, 72, 'car', 'Toyota', 'Corolla'],
                          [57, 327, 113, 87, 'car', 'Volkswagen', 'Golf'],
                          [1127, 132, 64, 52, 'car', 'Jeep', 'Wrangler'],
                          [722, 378, 150, 106, 'car', 'Land-Rover', 'Range Rover'],
                          [1076, 103, 55, 41, 'car', 'Subaru', 'WRX'], [982, 66, 41, 33, 'car', 'Ford', 'Mustang'],
                          [848, 158, 76, 34, 'car', 'BMW', '7 Series'],
                          [575, 237, 81, 58, 'car', 'Lamborghini', 'Aventador'],
                          [200, 247, 84, 61, 'car', 'Honda', 'Civic'], [459, 170, 63, 53, 'car', 'Jeep', 'Wrangler']])

    def testing_multiple_cars_confidence_and_threshold_pic1_01(self):
        self.assertEqual(car_rec(image2, 0.8, 0.5),
                         [[1035, 460, 158, 115, 'car', 'Honda', 'Civic'], [195, 438, 156, 142, 'car', 'Honda', 'CR-V'],
                          [721, 486, 210, 180, 'car', 'Toyota', 'Sequoia'],
                          [514, 365, 141, 98, 'car', 'Subaru', 'Impreza'],
                          [-1, 438, 111, 108, 'car', 'Ford', 'Mustang'],
                          [229, 381, 158, 105, 'car', 'Chevrolet', 'Camaro'],
                          [287, 594, 203, 74, 'car', 'Porsche', 'Cayenne'],
                          [462, 477, 169, 155, 'car', 'Dodge', 'Dakota'], [1086, 196, 81, 54, 'car', 'Ford', 'Mustang'],
                          [860, 198, 76, 48, 'car', 'Honda', 'Civic'], [0, 359, 131, 113, 'car', 'Mini', 'Cooper'],
                          [552, 289, 86, 50, 'car', 'Ford', 'Mustang'], [299, 315, 126, 77, 'car', 'Ford', 'Mustang'],
                          [809, 105, 69, 39, 'car', 'Jeep', 'Wrangler'], [385, 254, 91, 68, 'car', 'BMW', '3 Series'],
                          [157, 286, 106, 72, 'car', 'Toyota', 'Corolla'],
                          [57, 327, 113, 87, 'car', 'Volkswagen', 'Golf'],
                          [1127, 132, 64, 52, 'car', 'Jeep', 'Wrangler'],
                          [722, 378, 150, 106, 'car', 'Land-Rover', 'Range Rover'],
                          [1076, 103, 55, 41, 'car', 'Subaru', 'WRX'], [982, 66, 41, 33, 'car', 'Ford', 'Mustang'],
                          [848, 158, 76, 34, 'car', 'BMW', '7 Series'],
                          [575, 237, 81, 58, 'car', 'Lamborghini', 'Aventador'],
                          [200, 247, 84, 61, 'car', 'Honda', 'Civic'], [459, 170, 63, 53, 'car', 'Jeep', 'Wrangler']])

    def testing_multiple_cars_confidence_and_threshold_pic1_02(self):
        self.assertEqual(car_rec(image2, 0.9, 0.7),
                         [[1035, 460, 158, 115, 'car', 'Honda', 'Civic'], [195, 438, 156, 142, 'car', 'Honda', 'CR-V'],
                          [721, 486, 210, 180, 'car', 'Toyota', 'Sequoia'],
                          [514, 365, 141, 98, 'car', 'Subaru', 'Impreza'],
                          [-1, 438, 111, 108, 'car', 'Ford', 'Mustang'],
                          [229, 381, 158, 105, 'car', 'Chevrolet', 'Camaro'],
                          [287, 594, 203, 74, 'car', 'Porsche', 'Cayenne'],
                          [462, 477, 169, 155, 'car', 'Dodge', 'Dakota'], [1086, 196, 81, 54, 'car', 'Ford', 'Mustang'],
                          [860, 198, 76, 48, 'car', 'Honda', 'Civic'],
                          [0, 359, 131, 113, 'car', 'Mini', 'Cooper'], [552, 289, 86, 50, 'car', 'Ford', 'Mustang'],
                          [299, 315, 126, 77, 'car', 'Ford', 'Mustang'], [809, 105, 69, 39, 'car', 'Jeep', 'Wrangler'],
                          [385, 254, 91, 68, 'car', 'BMW', '3 Series']])

    def testing_multiple_cars_pic2(self):
        self.assertEqual(car_rec(image3), [[352, 831, 617, 203, 'car', 'Volkswagen', 'Golf'],
                                           [1088, 834, 539, 227, 'car', 'Ford', 'Mustang'],
                                           [2146, 1009, 1015, 463, 'car', 'Porsche', '718 Cayman'],
                                           [2151, 726, 420, 117, 'car', 'Chevrolet', 'Malibu'],
                                           [1634, 733, 247, 121, 'car', 'BMW', 'M2'],
                                           [1913, 835, 520, 222, 'car', 'Honda', 'Civic'],
                                           [959, 741, 387, 102, 'car', 'Mercedes-Benz', 'E-Class'],
                                           [2486, 833, 646, 193, 'car', 'Chevrolet', 'Corvette'],
                                           [478, 1115, 826, 424, 'car', 'Mazda', 'Miata'],
                                           [1389, 1071, 674, 569, 'car', 'Genesis', 'G70']])

    def testing_multiple_cars_confidence_pic2(self):
        self.assertEqual(car_rec(image3, 0.9), [[352, 831, 617, 203, 'car', 'Volkswagen', 'Golf'],
                                                [1088, 834, 539, 227, 'car', 'Ford', 'Mustang'],
                                                [2146, 1009, 1015, 463, 'car', 'Porsche', '718 Cayman'],
                                                [2151, 726, 420, 117, 'car', 'Chevrolet', 'Malibu'],
                                                [1634, 733, 247, 121, 'car', 'BMW', 'M2'],
                                                [1913, 835, 520, 222, 'car', 'Honda', 'Civic'],
                                                [959, 741, 387, 102, 'car', 'Mercedes-Benz', 'E-Class'],
                                                [2486, 833, 646, 193, 'car', 'Chevrolet', 'Corvette'],
                                                [478, 1115, 826, 424, 'car', 'Mazda', 'Miata'],
                                                [1389, 1071, 674, 569, 'car', 'Genesis', 'G70']])

    def testing_multiple_cars_confidence_and_threshold_pic2(self):
        self.assertEqual(car_rec(image3, 0.9, 0.7), [[352, 831, 617, 203, 'car', 'Volkswagen', 'Golf'],
                                                     [1088, 834, 539, 227, 'car', 'Ford', 'Mustang'],
                                                     [2146, 1009, 1015, 463, 'car', 'Porsche', '718 Cayman'],
                                                     [2151, 726, 420, 117, 'car', 'Chevrolet', 'Malibu'],
                                                     [1634, 733, 247, 121, 'car', 'BMW', 'M2'],
                                                     [1913, 835, 520, 222, 'car', 'Honda', 'Civic'],
                                                     [959, 741, 387, 102, 'car', 'Mercedes-Benz', 'E-Class'],
                                                     [2486, 833, 646, 193, 'car', 'Chevrolet', 'Corvette'],
                                                     [478, 1115, 826, 424, 'car', 'Mazda', 'Miata'],
                                                     [1389, 1071, 674, 569, 'car', 'Genesis', 'G70']])

    def testing_single_selected_cars(self):
        self.assertIn([2146, 1009, 1015, 463, 'car', 'Porsche', '718 Cayman'], car_rec(image3))

    def testing_single_selected_cars_confidence(self):
        self.assertIn([2146, 1009, 1015, 463, 'car', 'Porsche', '718 Cayman'], car_rec(image3, 0.8))

    def testing_single_selected_cars_confidence_and_threshold(self):
        self.assertIn([2146, 1009, 1015, 463, 'car', 'Porsche', '718 Cayman'], car_rec(image3, 0.8, 0.5))

    def test_object_car(self):
        self.assertIn('car', car_rec(image3)[0][4])

    def test_object_person(self):
        self.assertNotIn('person', car_rec(image3)[0][4])


if __name__ == '__main__':
    unittest.main()
