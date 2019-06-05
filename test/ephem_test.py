""" A quick test to make sure we can get pyephem to do what we want """
import ephem
from dateutil import tz

def doit():
    ''' runs the thingy '''
    from_zone = tz.gettz('UTC')
    to_zone = tz.gettz('Australia/Adelaide')

    bute = ephem.Observer()
    bute_sa_lat = '-33.8393058'
    bute_sa_long = '137.9405358'
    bute.lat, bute.lon = bute_sa_lat, bute_sa_long
    ephem_next_sunrise = bute.next_rising(ephem.Sun())
    next_sunrise = ephem_next_sunrise.datetime()
    next_sunrise = next_sunrise.replace(tzinfo=from_zone)
    next_sunset = bute.next_setting(ephem.Sun()).datetime()
    next_sunset = next_sunset.replace(tzinfo=from_zone)

    local_next_sunrise = next_sunrise.astimezone(to_zone)
    year, month, date, hours, minutes, seconds = ephem_next_sunrise.tuple()

    print 'next sunrise (date string)    = ' + str(local_next_sunrise)
    print 'next sunrise (ms since epoch) = ' + str(float(ephem_next_sunrise))
    print 'next sunrise (tuple)          = year:' + str(year) + ' month:' + str(month) + ' date:' + str(date) + ' hours:' + str(hours) + ' minutes:' + str(minutes) + ' seconds:' + str(seconds)
    print 'next sunset = ' + str(next_sunset.astimezone(to_zone))

doit()
