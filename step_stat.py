import configparser
import os

import fitbit
from plotly.graph_objs import Scatter
from plotly.offline import plot


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

response = authd_client.make_request(
    'https://api.fitbit.com/1/user/-/activities/list.json?beforeDate=2017-06-01&offset=0&limit=20&sort=asc')
sleep = authd_client.body_weight_goal()
alma = authd_client.time_series('activities/steps', period='1y', base_date='2017-05-01')
act_list = authd_client.activities_list()
running = authd_client.activity_detail('12030')
di = {}
for a in alma['activities-steps']:
    dm = a['dateTime']
    # print("{0}\t{1}".format(dm, a['value']))
    dm = dm[0:7]
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
    y=y
)

data = [trace]

plot(data, filename='basic-line')
