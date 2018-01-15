from datetime import datetime, timedelta


class SessionController(object):
    """ Session Controller Class Object """

    def __init__(self):
        """ Session tracker for Session Controller Class """

        self.sessions = []
        self.event_timeouts = {'touch': 1, 'swipe': 3}
        self.event_untimed = ['check']  # Note: data structure inconsistency?
        self.event_data = {}  # Changing this so that the event start gets added to session

    # TODO: possibly split event types into own method
    def event(self, event_type):
        """ Simulation of an event """

        now = datetime.now()

        # Records beginning of session
        if self.event_data == {}:
            self.sessions.append(now)

        # Records timestamp for timed events
        if event_type in self.event_timeouts:
            self.event_data[event_type] = now + timedelta(seconds=self.event_timeouts[event_type])

        # Removes timestamp if any existing timed events have timed out
        # Note: the runtime on this concerns me
        # TODO: I would rather delete event based on timestamp
        for event in self.event_timeouts:
            if (event in self.event_timeouts and event in self.event_data and now > self.event_data[event]):
                del self.event_data[event]

        # Check event is added if not in dict, otherwise deletes it
        if event_type in self.event_untimed and event_type not in self.event_data:
            self.event_data[event_type] = now
        elif event_type in self.event_untimed and event_type in self.event_data:
            del self.event_data[event_type]

        # Process end of session
        # TODO: record timeout event if final event in session
        if len(self.event_data) == 0:
            start = self.sessions.pop()
            self.sessions.append((start, now))
            self.event_data = {}

    def in_progress(self):
        """ Determines if session is still in progress """

        # TODO: Fix so no hard coding of event types in method
        if ('touch' in self.event_data and
           datetime.now() - self.event_data['touch'] < timedelta(seconds=0) or
           'swipe' in self.event_data and
           datetime.now() - self.event_data['swipe'] < timedelta(seconds=0) or
           'check' in self.event_data):

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
