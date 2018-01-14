import unittest
from session_controller_2 import SessionController
import time
from datetime import timedelta, datetime


class TestSessionController(unittest.TestCase):
    """ Testing if SessionController returns expected results """

    def setUp(self):
        """ Initiates session object for each test """

        self.session = SessionController()

    def tearDown(self):
        """ Removes object after test """

        del self.session

    def test_sc_single_session(self):
        """ Test case #1 - single session """

        self.session.event('swipe')
        time.sleep(2)
        self.session.event('touch')
        self.session.event('touch')
        time.sleep(2)  # swipe times out
        self.session.event('touch')
        self.session.event('check')
        time.sleep(3)  # touch times out
        self.session.event('check')

        session_length = (self.session.sessions[0][1].replace(microsecond=0) -
                          self.session.sessions[0][0].replace(microsecond=0))

        self.assertEqual(session_length, timedelta(seconds=7))

    def test_sc_multiple_sessions(self):
        """ Test case #2 - multiple sessions """

        # First session
        self.session.event('swipe')
        time.sleep(2)
        self.session.event('touch')
        self.session.event('touch')
        self.session.event('check')
        time.sleep(3)  # touch/swipe times out
        self.session.event('check')

        # Second session
        self.session.event('check')
        self.session.event('touch')
        time.sleep(3)  # touch times out
        self.session.event('check')
        print(self.session.sessions)

        session_length_1 = (self.session.sessions[0][1].replace(microsecond=0) -
                            self.session.sessions[0][0].replace(microsecond=0))

        session_length_2 = (self.session.sessions[1][1].replace(microsecond=0) -
                            self.session.sessions[1][0].replace(microsecond=0))

        self.assertEqual(session_length_1, timedelta(seconds=5))
        self.assertEqual(session_length_2, timedelta(seconds=3))

    def test_sc_active_check(self):
        """ Test case #3 - active session (unclosed check) """

        self.session.event('swipe')
        time.sleep(2)
        self.session.event('touch')
        self.session.event('check')
        time.sleep(1)  # swipe & touch time out

        self.assertTrue(self.session.in_progress())

    def test_sc_touch(self):
        """ Test case #4 - touch timeout """

        self.session.event('touch')
        self.session.event('touch')
        self.assertTrue(self.session.in_progress())

        self.session.event(' touch')
        time.sleep(2)
        self.assertFalse(self.session.in_progress())

    def test_sc_swipe(self):
        """ Test case #5 - swipe timeout) """

        self.session.event('swipe')
        self.assertTrue(self.session.in_progress())
        self.session.event('swipe')
        time.sleep(5)
        self.assertFalse(self.session.in_progress())

    def test_continuing_touches(self):
        """ Test case #6 - continuing touch events """

        for i in range(10):
            self.session.event('touch')
            time.sleep(0.9)
            self.assertTrue(self.session.in_progress())

        time.sleep(1)
        self.assertFalse(self.session.in_progress())

    def test_sc_mult_active_session(self):
        """ Test case #7 - multiple session w/ active """

        self.session.event('swipe')
        time.sleep(2)
        self.session.event('touch')
        self.session.event('touch')
        time.sleep(2)  # swipe times out
        self.session.event('touch')
        self.session.event('check')
        time.sleep(3)  # touch times out
        self.session.event('check')

        session_length = (self.session.sessions[0][1].replace(microsecond=0) -
                          self.session.sessions[0][0].replace(microsecond=0))

        self.assertEqual(session_length, timedelta(seconds=7))

        self.session.event('swipe')
        self.session.event('touch')
        self.session.event('check')

        self.assertTrue(self.session.in_progress())


if __name__ == '__main__':
    unittest.main(exit=False)
