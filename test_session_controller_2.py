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

    def test_sc_valid_session(self):
        """ Test case #1 - valid session """

        self.session.event('swipe')
        time.sleep(2)
        self.session.event('touch')
        self.session.event('touch')
        time.sleep(2)  # swipe times out
        self.session.event('touch')
        self.session.event('check')
        time.sleep(3)  # touch times out
        self.session.event('check')

        session_length = (self.session.sessions[1]['end'].replace(microsecond=0) -
                          self.session.sessions[1]['start'].replace(microsecond=0))

        self.assertEqual(session_length, timedelta(seconds=9))

    # def test_sc_unclosed_check(self):
    #     """ Test case #2 - active session (unclosed check) """

    #     self.session.event('swipe')
    #     time.sleep(4)  # swipe times out
    #     self.session.event('touch')
    #     self.session.event('touch')
    #     time.sleep(2)  # touch times out
    #     self.session.event('touch')
    #     self.session.event('check')

    #     self.assertEqual(self.session.times(), 'Session still active')

    # def test_sc_touch(self):
    #     """ Test case #3 - testing for touch timeout """

    #     self.session.event('touch')
    #     self.assertTrue(self.session.in_progress())
    #     self.session.event('touch')
    #     time.sleep(2)
    #     self.assertFalse(self.session.in_progress())

    # def test_sc_swipe(self):
    #     """ Test case #4 - active session (swipe did not timeout) """

    #     self.session.event('swipe')
    #     self.assertTrue(self.session.in_progress())
    #     self.session.event('swipe')
    #     time.sleep(5)
    #     self.assertFalse(self.session.in_progress())

    # def test_sc_ghost_session(self):
    #     """ Test case #5 - ghost session """

    #     self.session.event('swipe')
    #     time.sleep(4)  # swipe times out and no other events

    #     self.assertEqual(self.session.times(), 'Ghost session')

    # def test_sc_multiple_sessions(self):
    #     """ Test case #6 - multiple sessions """

    #     self.session.event('swipe')
    #     self.session.event('touch')
    #     time.sleep(1)
    #     self.session.event('touch')
    #     time.sleep(1)
    #     self.session.event('touch')
    #     time.sleep(1)
    #     self.session.event('check')
    #     time.sleep(1)
    #     self.session.event('check')
    #     self.assertFalse(self.session.in_progress())

    #     self.session.event('swipe')
    #     self.session.event('touch')
    #     for i in range(12):
    #         self.session.event('touch')
    #         time.sleep(0.5)
    #     self.assertTrue(self.session.in_progress())


if __name__ == '__main__':
    unittest.main(exit=False)
