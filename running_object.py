import datetime
import time
ONE_MILE = 1.609344


def get_runs(authd_client):
    sorting = 'desc'
    offset = 0
    after_date = '2017-06-28'
    runs = []
    response = authd_client.make_request(
        'https://api.fitbit.com/1/user/-/activities/list.json?afterDate={beforeDate}&offset={offset}&limit=20&sort={sorting}'.format(
            offset=offset,
            beforeDate=after_date,
            sorting=sorting))
    for act in response['activities']:
        if (act['activityName'] == 'Run') and (act['logType'] == 'mobile_run'):
            runs.append(Running(act['activeDuration'], act['distance'] * ONE_MILE, act['startTime'][0:10], act['steps']))
    while response['pagination']['next'] != '':
        url = response['pagination']['next']
        response = authd_client.make_request(url)
        for act in response['activities']:
            if (act['activityName'] == 'Run') and (act['logType'] == 'mobile_run'):
                runs.append(Running(act['activeDuration'], act['distance'] * ONE_MILE, act['startTime'][0:10], act['steps']))
    return runs


class Running(object):

    ONE_MILLISEC_IN_HOUR = 0.000000277778

    def __init__(self, duration, distance, date, steps):
        """
        :param str date: Date of running
        :param int duration: in milliseconds
        :param float distance: in kilometer
        :param int steps: step number
        """
        self.step = steps
        self.duration = duration
        self.distance = distance
        date_parts = date.split('-')
        d = datetime.date(int(date_parts[0]), int(date_parts[1]), int(date_parts[2]))
        self.date = d
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
