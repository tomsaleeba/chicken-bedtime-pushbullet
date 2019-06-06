import os
from datetime import datetime as dt, timedelta
from dateutil import tz
import ephem
import requests

TIME_FORMAT_STR = '%02d:%02d'
FROM_ZONE = tz.gettz('UTC')
TO_ZONE = tz.gettz('Australia/Adelaide')
ADELAIDE_LAT = '-34.9786554'
ADELAIDE_LONG = '138.5487406'

try:
    run_frequency_minutes = int(os.getenv('RUN_FREQUENCY', default=5))
except ValueError as e:
    print('[ERROR] RUN_FREQUENCY env var was not an int')
    raise e


def is_closest_time(now_datetime, sunset_datetime):
    diff_now_seconds = abs((sunset_datetime - now_datetime).total_seconds())
    run_frequency_seconds = run_frequency_minutes * 60
    now_is_not_within_run_frequency_of_sunset = abs(
        diff_now_seconds) > run_frequency_seconds
    if now_is_not_within_run_frequency_of_sunset:
        print('Now (%s) is more than %d minutes away from sunset (%s)' %
              (str(now_datetime), run_frequency_minutes, str(sunset_datetime)))
        return False
    run_freq_minutes_delta = timedelta(minutes=run_frequency_minutes)

    def before_sunset_strategy():
        next_check_datetime = now_datetime + run_freq_minutes_delta
        diff_next_seconds = abs(
            (next_check_datetime - sunset_datetime).total_seconds())
        now_is_closer_than_next = diff_now_seconds <= diff_next_seconds
        return now_is_closer_than_next

    def after_sunset_strategy():
        prev_check_datetime = now_datetime - run_freq_minutes_delta
        diff_prev_seconds = abs(
            (sunset_datetime - prev_check_datetime).total_seconds())
        now_is_closer_than_prev = diff_now_seconds < diff_prev_seconds
        return now_is_closer_than_prev

    is_before_sunset = now_datetime < sunset_datetime
    if is_before_sunset:
        return before_sunset_strategy()
    return after_sunset_strategy()


def now_time_str():
    now = dt.now(tz=TO_ZONE)
    return TIME_FORMAT_STR % (now.hour, now.minute)


def lambda_handler(event, context):
    adelaide = get_observer()
    # FIXME is next setting actually *next* or today?
    ephem_next_sunset = adelaide.next_setting(ephem.Sun())
    zoneless_next_sunset = ephem_next_sunset.datetime()
    next_sunset = zoneless_next_sunset.replace(tzinfo=FROM_ZONE)
    local_next_sunset = next_sunset.astimezone(TO_ZONE)
    decomposed = decompose(local_next_sunset)
    sunset_time_str = TIME_FORMAT_STR % (decomposed['hour'],
                                         decomposed['minute'])
    if not is_closest_time(dt.now(tz=TO_ZONE), local_next_sunset):
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
