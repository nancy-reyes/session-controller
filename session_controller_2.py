from datetime import datetime, timedelta


class SessionController(object):
    """ Session Controller class """

    swipe_timeout = 3
    touch_timeout = 1
    sessions = {}
    session_count = 1  # Session number

    def __init__(self):
        """ Creates session trackers for Session Controller class """

        self.event_data = {'touch': datetime(1, 1, 1), 'swipe': datetime(1, 1, 1)}  # Track individual session data
        self.check_count = 0

    def event(self, event_type):
        """ Simulation of a touch, swipe or check event """

        now = datetime.now()
        print(self.event_data)

        # Create new session if event_data is blank
        if self.event_data == {'touch': datetime(1, 1, 1), 'swipe': datetime(1, 1, 1)}:
            self.event_data['start'] = now
            print(self.event_data)

        # Keep track of check events
        if event_type == 'check':
            self.check_count += 1

        # When session ends, add start/end to sessions dict & reset event_data
        if (self.check_count % 2 == 0
            and now - self.event_data['swipe'] > timedelta(seconds=self.swipe_timeout)
            and now - self.event_data['touch'] > timedelta(seconds=self.touch_timeout)):

            self.sessions[self.session_count] = {}
            print(self.sessions)
            self.sessions[self.session_count]['start'] = self.event_data['start']
            print(self.sessions)
            self.sessions[self.session_count]['end'] = now
            self.session_count += 1
            self.event_data = {'touch': datetime(1, 1, 1), 'swipe': datetime(1, 1, 1)}
            self.check_count = 0

        # Add event to event_data
        self.event_data[event_type] = now
        print(self.event_data)

    def get_times(self):
        if self.sessions:
            for key, value in self.sessions.items():
                print('Session {}:\nStart: {}\nEnd: {}'.format(key, value['start'], value['end']))