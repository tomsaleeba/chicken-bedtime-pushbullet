import os
from datetime import datetime as dt
from dateutil import tz
import ephem
import requests

FROM_ZONE = tz.gettz('UTC')
TO_ZONE = tz.gettz('Australia/Adelaide')
ADELAIDE_LAT = '-34.9786554'
ADELAIDE_LONG = '138.5487406'

# FIXME change CRON schedule to run every 5 minutes between times that sunset can happen
# FIXME case input to int
run_frequency = os.getenv('RUN_FREQUENCY', default=5)


def is_closest_time(now_datetime, sunset_datetime):
    # pass sunset as datetime obj
    # create now as datetime obj (with tz)
    # define schedule regularity (5 minutes)
    # create datetime obj for next run
    # check if now and next are either side of sunset, bail if not
    # check if delta between now and sunset is less than next and sunset
    # if now, then push, return
    # check now and previous time
    if now.hour < hour:
        return False
    if now.hour == hour:
        return minute <= 30
    if now.hour == hour + 1:
        return minute > 30
    return False


def now_time_str():
    now = dt.now(tz=TO_ZONE)
    return '%s:%s' % (now.hour, now.minute)


def lambda_handler(event, context):
    adelaide = get_observer()
    ephem_next_sunset = adelaide.next_setting(ephem.Sun())
    zoneless_next_sunset = ephem_next_sunset.datetime()
    next_sunset = zoneless_next_sunset.replace(tzinfo=FROM_ZONE)
    local_next_sunset = next_sunset.astimezone(TO_ZONE)
    decomposed = decompose(local_next_sunset)
    sunset_time_str = '%s:%s' % (decomposed['hour'], decomposed['minute'])
    if not is_closest_hour(decomposed['hour'], decomposed['minute']):
        print('[INFO] now (%s) is not closest hour to sunset (%s), bailing' %
              (now_time_str(), sunset_time_str))
        return 'Done, nothing sent'
    body = 'Sunset is at %s' % sunset_time_str
    print('Sending body=' + body)
    send_push(title='Chickens to bed', body=body)
    return 'Done, sent push'


def send_push(title, body):
    PB_TOKEN = os.getenv('PB_TOKEN')
    if not PB_TOKEN:
        raise KeyError(
            'You must define the PB_TOKEN env var as the PushBullet API token')
    headers = {
        'Access-Token': PB_TOKEN,
    }
    body = {
        'type': 'note',
        'title': title,
        'body': body,
        'channel_tag': 'chicken-bedtime'
    }
    url = 'https://api.pushbullet.com/v2/pushes'
    requests.post(url, json=body, headers=headers)


def get_observer():
    adelaide = ephem.Observer()
    adelaide.lat, adelaide.lon = ADELAIDE_LAT, ADELAIDE_LONG
    return adelaide


def decompose(e):
    return {
        'hour': e.time().hour,
        'minute': e.time().minute,
    }


if __name__ == '__main__':
    lambda_handler(None, None)
