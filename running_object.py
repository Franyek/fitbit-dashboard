import time


class Running(object):

    ONE_MILLISEC_IN_HOUR = 0.000000277778

    def __init__(self, duration, distance, date):
        """
        :param str date: Date of running
        :param int duration: in milliseconds
        :param float distance: in kilometer
        """
        self.duration = duration
        self.distance = distance
        self.date = date
        super().__init__()

    def get_speed(self):
        """
        :return: the speed in km/h
        :rtype: float
        """
        return self.distance/(self.duration * self.ONE_MILLISEC_IN_HOUR)

    def get_duration(self):
        """
        Get readable duration
        :return: duration in minutes and seconds
        :rtype: str
        """
        return time.strftime('%H:%M:%S', time.gmtime(self.duration/1000.0))
