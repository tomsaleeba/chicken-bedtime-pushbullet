import unittest
from src.lambda_function import is_closest_hour


class TestLambdaFunction(unittest.TestCase):
    def test_is_closest_hour01(self):
        """ test if we can tell we're the closest time from before """
        now = # FIXME
        sunset = # FIXME
        result = is_closest_time(now, sunset)
        self.assertEqual('foo'.upper(), 'FOO')

    # test closest after

    # test not closest before
    # test not closest after
