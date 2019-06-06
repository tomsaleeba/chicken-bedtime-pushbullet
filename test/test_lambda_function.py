import unittest
from datetime import datetime as dt

from src.lambda_function import is_closest_time, TO_ZONE


class TestLambdaFunction(unittest.TestCase):
    def test_is_closest_hour01(self):
        """ can tell we're the closest time from before """
        now = dt(2019, 1, 25, 19, 35, 0, 0, TO_ZONE)
        sunset = dt(2019, 1, 25, 19, 37, 0, 0, TO_ZONE)
        result = is_closest_time(now, sunset)
        self.assertTrue(result, 'Should be considered closest "before" time')

    def test_is_closest_hour02(self):
        """ can tell we're NOT the closest time from after """
        now = dt(2019, 1, 25, 19, 40, 0, 0, TO_ZONE)
        sunset = dt(2019, 1, 25, 19, 37, 0, 0, TO_ZONE)
        result = is_closest_time(now, sunset)
        self.assertFalse(result,
                         'Should NOT be considered closest "after" time')

    def test_is_closest_hour03(self):
        """ can tell we're the closest time from after """
        now = dt(2019, 1, 25, 19, 40, 0, 0, TO_ZONE)
        sunset = dt(2019, 1, 25, 19, 38, 0, 0, TO_ZONE)
        result = is_closest_time(now, sunset)
        self.assertTrue(result, 'Should be considered closest "after" time')

    def test_is_closest_hour04(self):
        """ can tell we're NOT the closest time from before """
        now = dt(2019, 1, 25, 19, 35, 0, 0, TO_ZONE)
        sunset = dt(2019, 1, 25, 19, 38, 0, 0, TO_ZONE)
        result = is_closest_time(now, sunset)
        self.assertFalse(result,
                         'Should NOT be considered closest "before" time')

    def test_is_closest_hour05(self):
        """ can tell we're more than one run away on the before side """
        now = dt(2019, 1, 25, 19, 30, 0, 0, TO_ZONE)
        sunset = dt(2019, 1, 25, 19, 38, 0, 0, TO_ZONE)
        result = is_closest_time(now, sunset)
        self.assertFalse(result, 'Should be considered too far away')

    def test_is_closest_hour06(self):
        """ can tell we're more than one run away on the after side """
        now = dt(2019, 1, 25, 19, 45, 0, 0, TO_ZONE)
        sunset = dt(2019, 1, 25, 19, 38, 0, 0, TO_ZONE)
        result = is_closest_time(now, sunset)
        self.assertFalse(result, 'Should be considered too far away')

    def test_is_closest_hour07(self):
        """ can we deal with an equal diff from before """
        now = dt(2019, 1, 25, 19, 35, 0, 0, TO_ZONE)
        sunset = dt(2019, 1, 25, 19, 37, 30, 0, TO_ZONE)
        result = is_closest_time(now, sunset)
        self.assertTrue(
            result,
            'Should be considered the closest (favour before in equal diff)')

    def test_is_closest_hour08(self):
        """ can we deal with an equal diff from after """
        now = dt(2019, 1, 25, 19, 40, 0, 0, TO_ZONE)
        sunset = dt(2019, 1, 25, 19, 37, 30, 0, TO_ZONE)
        result = is_closest_time(now, sunset)
        self.assertFalse(result, 'Should NOT be considered the closest')
