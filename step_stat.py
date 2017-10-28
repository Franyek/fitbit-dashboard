import configparser
import datetime
import os

import fitbit
from plotly.graph_objs import Scatter
from plotly.offline import plot

from running_object import get_runs

config = configparser.ConfigParser()
folder_name = os.path.dirname(os.path.realpath(__file__))
config.read(folder_name + os.sep + 'fitbit_configs.ini', encoding='UTF-8')

CLIENT = config.get('DEFAULT', 'CLIENT')
SECRET = config.get('DEFAULT', 'SECRET')
ACCESS_TOKEN = config.get('DEFAULT', 'ACCESS_TOKEN')
REFRESH_TOKEN = config.get('DEFAULT', 'REFRESH_TOKEN')
authd_client = fitbit.Fitbit(CLIENT, SECRET,
                             access_token=ACCESS_TOKEN,
                             refresh_token=REFRESH_TOKEN)

activities_steps = authd_client.time_series('activities/steps', period='3m')
#activities_runs = get_runs(authd_client)

holiday_first_date = datetime.date(2017, 8, 21)
invalid_dates = [holiday_first_date + datetime.timedelta(days=x) for x in range(0, 7)]
invalid_dates.append(datetime.date(2017, 9, 21))
invalid_dates.append(datetime.date(2017, 9, 22))
invalid_dates.append(datetime.date(2017, 9, 25))
di = {}
for a in activities_steps['activities-steps']:
    dm = a['dateTime']
    date_parts = dm.split('-')
    today = datetime.date(int(date_parts[0]), int(date_parts[1]), int(date_parts[2]))
    if (today.weekday() < 5) and today not in invalid_dates and int(a['value']) != 0:
        if dm in di:
            di[dm].append(a['value'])
        else:
            di[dm] = [a['value']]
ordered_dates = di.keys()
sorted(ordered_dates)
sepfile = []
for date in ordered_dates:
    l = [int(s) for s in di[date]]
    # l = [s for s in l if (s > 1000) and (s < 14000)]
    avg = sum(l) / float(len(l))
    print("{0}\t{1}".format(date, str(avg).replace(".", ",")))
    # sepfile.append((DT.datetime.strptime(date, "%Y-%m"), avg))
    sepfile.append((date, avg))

x = [date for (date, value) in sepfile]
y = [value for (date, value) in sepfile]

# Create a trace
trace = Scatter(
    x=x,
    y=y,
    mode='lines+markers',
    name='Daily steps'
)

reference_line = Scatter(
    x=x,
    y=[8500] * len(x),
    name='Reference line',
    line=dict(
        color=('rgb(205, 12, 24)'),
        width=5)
)

data = [trace, reference_line]

plot(data, filename='basic-area')
