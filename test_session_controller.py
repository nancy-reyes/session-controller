import unittest
# from random import choice
from session_controller import SessionController
import time
from datetime import timedelta


class TestSessionController(unittest.TestCase):
    """ Testing if SessionController returns expected simulated session times """

    def test_sc_1(self):
        """ Test case #1 - valid session """

        session1 = SessionController()

        session1.event('swipe')
        time.sleep(4)  # swipe times out
        session1.event('touch')
        session1.event('touch')
        time.sleep(2)  # touch times out
        session1.event('touch')
        session1.event('check')
        time.sleep(10)  # touch times out
        session1.event('check')

        session_length = (session1.times()[1].replace(microsecond=0) -
                               session1.times()[0].replace(microsecond=0))

        self.assertEqual(session_length, timedelta(seconds=16))

    def test_sc_2(self):
        """ Test case #2 - active session (unclosed check) """

        session2 = SessionController()

        session2.event('swipe')
        time.sleep(4)  # swipe times out
        session2.event('touch')
        session2.event('touch')
        time.sleep(2)  # touch times out
        session2.event('touch')
        session2.event('check')

        self.assertEqual(session2.times(), 'Session still active')

    def test_sc_3(self):
        """ Test case #3 - active session (touch did not timeout) """

        session3 = SessionController()

        session3.event('touch')
        print('touch not timeout')
        print(session3.event_data)

        self.assertEqual(session3.times(), 'Session still active')

    def test_sc_4(self):
        """ Test case #4 - active session (swipe did not timeout) """

        session4 = SessionController()

        session4.event('swipe')
        time.sleep(2)
        print('swipe not timeout')
        print(session4.event_data)

        self.assertEqual(session4.times(), 'Session still active')

    def test_sc_5(self):
        """ Test case #5 - ghost session """

        session5 = SessionController()

        session5.event('swipe')
        time.sleep(4)  # swipe times out and no other events
        print(session5.event_data)

        self.assertEqual(session5.times(), 'Ghost session')


if __name__ == '__main__':
    unittest.main(exit=False)
