from datetime import datetime, timedelta


class SessionController(object):
    """ Session Controller Class Object """


    def __init__(self):
        """ Session tracker for Session Controller Class """

        self.sessions = []
        self.swipe_timeout = 3
        self.touch_timeout = 1
        self.event_data = {'start': None}

    def event(self, event_type):
        """ Simulation of an event """

        now = datetime.now()
        print(now)

        # Records beginning of session
        if self.event_data['start'] is None:
            self.event_data['start'] = now

        # Records timestamp for touch/swipe events
        if event_type == 'touch':
            self.event_data[event_type] = now + timedelta(seconds=self.touch_timeout)
        elif event_type == 'swipe':
            self.event_data[event_type] = now + timedelta(seconds=self.swipe_timeout)

        # Removes timestamp if any existing touch/swipe events have timed out
        if 'touch' in self.event_data and now > self.event_data['touch']:
            del self.event_data['touch']

        if 'swipe' in self.event_data and now > self.event_data['swipe']:
            del self.event_data['swipe']

        # Check event is added if not in dict, otherwise deletes it
        if event_type == 'check' and 'check' not in self.event_data:
            self.event_data[event_type] = now
        elif event_type == 'check' and 'check' in self.event_data:
            del self.event_data['check']

        # Process end of session
        if len(self.event_data) == 1:
            self.sessions.append((self.event_data['start'], now))
            self.event_data = {'start': None}

        print(self.event_data)

    def in_progress(self):
        """ Determines if session is still in progress """

        if ('touch' in self.event_data and datetime.now() - self.event_data['touch'] < timedelta(seconds=0) or
           'swipe' in self.event_data and datetime.now() - self.event_data['swipe'] < timedelta(seconds=0) or
           'check' in self.event_data):
            return True
        else:
            return False

    def session_times(self):
        """ Prints session times & status """

        session_count = 1
        for session in self.sessions:
            print('Session {}:\nSession start: {}\nSession end: {}'.format(session_count, self.sessions[session_count-1][0], self.sessions[session_count-1][1]))
            session_count += 1

        if self.in_progress():
            print('Session {} is still in progress'.format(session_count))
