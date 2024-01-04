"""
Module to iterate over images.
"""


class Pager:
    """
    Class to iterate over images.
    """
    def __init__(self, count):
        self.count = count
        self.current = 0

    @property
    def next(self):
        """

        :return: number of next image
        """
        num = self.current + 1
        if num > self.count-1:
            num -= self.count
        return num

    @property
    def prev(self):
        """

        :return: number of previous image
        """
        num = self.current - 1
        if num < 0:
            num += self.count
        return num
