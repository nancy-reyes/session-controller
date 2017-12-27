import unittest
# from random import choice
from session_controller import SessionController
import time
from datetime import timedelta


class TestSessionController(unittest.TestCase):
    """ Testing if SessionController returns expected simulated session times """

    def setUp(self):
        """ Initiates session object for each test """

        self.session = SessionController()

    def tearDown(self):
        """ Removes object after test """

        del self.session

    def test_sc_1(self):
        """ Test case #1 - valid session """

        self.session.event('swipe')
        time.sleep(4)  # swipe times out
        self.session.event('touch')
        self.session.event('touch')
        time.sleep(2)  # touch times out
        self.session.event('touch')
        self.session.event('check')
        time.sleep(10)  # touch times out
        self.session.event('check')

        session_length = (self.session.times()[1].replace(microsecond=0) -
                          self.session.times()[0].replace(microsecond=0))

        self.assertEqual(session_length, timedelta(seconds=16))

    def test_sc_2(self):
        """ Test case #2 - active session (unclosed check) """

        self.session.event('swipe')
        time.sleep(4)  # swipe times out
        self.session.event('touch')
        self.session.event('touch')
        time.sleep(2)  # touch times out
        self.session.event('touch')
        self.session.event('check')

        self.assertEqual(self.session.times(), 'Session still active')

    def test_sc_3(self):
        """ Test case #3 - active session (touch did not timeout) """

        self.session.event('touch')

        self.assertEqual(self.session.times(), 'Session still active')

    def test_sc_4(self):
        """ Test case #4 - active session (swipe did not timeout) """

        self.session.event('swipe')
        time.sleep(2)

        self.assertEqual(self.session.times(), 'Session still active')

    def test_sc_5(self):
        """ Test case #5 - ghost session """

        self.session.event('swipe')
        time.sleep(4)  # swipe times out and no other events

        self.assertEqual(self.session.times(), 'Ghost session')


if __name__ == '__main__':
    unittest.main(exit=False)
