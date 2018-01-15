from datetime import datetime, timedelta


class SessionController(object):
    """ Session Controller Class Object """

    def __init__(self):
        """ Session tracker for Session Controller Class """

        self.sessions = []
        self.timeout_events = {'touch': 1, 'swipe': 3}
        self.untimed_events = ['check', 'blah']
        self.event_data = {}

    def event(self, event_type):
        """ Simulation of an event """

        now = datetime.now()

        # Records beginning of session
        if self.event_data == {}:
            self.sessions.append(now)

        # Records timestamp for timed events
        if event_type in self.timeout_events:
            self.event_data[event_type] = now + timedelta(seconds=self.timeout_events[event_type])

        # Removes timestamp if any existing timed events have timed out
        # NOTE: Try deleting key by value
        for event in self.timeout_events:
            if (event in self.timeout_events and event in self.event_data and now > self.event_data[event]):
                del self.event_data[event]

        # Check event is added if not in dict, otherwise deletes it
        if event_type in self.untimed_events and event_type not in self.event_data:
            self.event_data[event_type] = now
        elif event_type in self.untimed_events and event_type in self.event_data:
            del self.event_data[event_type]

        # Process end of session. This assumes a 2nd check event closes the session.
        # Subsequent timed events are ignored.
        if len(self.event_data) == 0:
            start = self.sessions.pop()
            self.sessions.append((start, now))
            self.event_data = {}

    def in_progress(self):
        """ Determines if session is still in progress """

        if any(datetime.now() - self.event_data[event] < timedelta(seconds=0) or
               event in self.untimed_events for event in self.event_data.keys()):

            return True
        else:
            return False

    def session_times(self):
        """ Prints session times & status """

        session_count = 1

        for session in self.sessions:
            print('Session {}:\nStart: {}\nEnd: {}'.format(session_count,
                                                           self.sessions[session_count-1][0],
                                                           self.sessions[session_count-1][1]))
            session_count += 1

        if self.in_progress():
            print('Session {} is still in progress'.format(session_count))
